from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from django.conf.urls.i18n import i18n_patterns
from core import models
from core.models import Provincia
from django.core.exceptions import ValidationError
# from .serializers import UserDetailSerializer


CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
# API_TOKEN_URL = reverse('users:api_token_auth')
ME_URL = reverse('users:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)

def sample_provincia(prov):
    p = Provincia.objects.create(nome=prov)

    return p

def sample_payload(**params):
    """ create and return a sample recipe """
    prov = sample_provincia('Padova')
    defaults = {'nome':'Alessandro', 'cognome':'Silvestro',
                'telefono':'373526852',
                'indirizzo': 'via rossi 7',
                'citta': 'Rovolon',
                'stato': 'I',
                'stato_estero':'',
                'provincia_ita':prov.id,
                'provincia_estero':''
                }
    defaults.update(params)
    return defaults
    # return Recipe.objects.create(user=user, **defaults)


class PublicUserApiTests(TestCase):
    """ test public user api """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creatng user with payload successful """

        payload = {
            'email': 'test2@silv.io',
            'password': 'testpass12345',
            # 'nome': 'test_name',
            # 'cognome': 'test cognome'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        payload = {
            'email': 'test@silv.io',
            'password': 'testpass',
            'nome': 'test_name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            'email': 'test@silv.io',
            'password': 'tt',
        }
        # create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        # self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ test if the token is create """
        payload = {
            'email': 'test2@silv.io',
            'password': 'testpass12345',
            # 'username': 'test2@silv.io',

        }

        # user=create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(res.data['email'], payload['email'])
        # res = self.client.post(TOKEN_URL, **payload)
        # res = self.client.post(TOKEN_URL, res.data)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
            create_user(email='test@silv.io', password='pwd12345678')
            payload = {
                'email': 'test@silv.io',
                'password': 'wrong',
            }
            res = self.client.post(TOKEN_URL, payload)
            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        payload = {
            'email': 'test@silv.io',
            'password': 'pwd12345678',
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):

        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorize(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApi(TestCase):

    def setUp(self):
        self.user = create_user(
            email='test2@silv.io',
            password='pwd12345678',
            nome='name',
            cognome='cognome'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_retrive_profile_success(self):
        """ test user is retrieve """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['nome'], self.user.nome)
        self.assertEqual(res.data['cognome'], self.user.cognome)

    def test_post_me_is_not_allwowed(self):
        """ tet post method is not allow """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_fields_success(self):
        """ test user is updated """

        payload = sample_payload()
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(res.data['citta'],payload['citta'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_profile_with_no_name(self):

        payload = {'nome':'', 'cognome':'cognome2'}
        payload = sample_payload(nome='')
        old_nome = self.user.nome
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.user.refresh_from_db()
        self.assertEqual(self.user.nome, old_nome)

    def test_update_profile_name_with_numbers(self):
        payload = sample_payload(nome='Alessandro13')
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_profile_surname_with_numbers(self):
        payload = sample_payload(nome='Alessandro', cognome='prova123')

        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_name_and_surname_normalize(self):
        """ test the first letter is capital and the rest is lower case"""
        payload = sample_payload(nome='aLESsandro maRIa',
                                 cognome= "de gASperI")
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data['nome'],'Alessandro Maria')
        self.assertEqual(res.data['cognome'],'De Gasperi')

    def test_update_telefono_success(self):
        """ test  update field telefono success`"""
        payload = sample_payload(telefono='  +356158654')
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['telefono'], '+356158654')

    def  test_update_telefono(self):
        """ test if telefono  is not valid"""
        payload = sample_payload(telefono='  3515 3515')
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        payload = sample_payload(telefono=' 3515asddf3515')
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_address_succes(self):
        """ test if telefono is properly saved """
        payload = sample_payload(indirizzo='via Traquinio Prisco  ')
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(res.data['indirizzo'],
                         self.user.indirizzo.strip().lower())

    def test_missing_field(self):
        payload = sample_payload(indirizzo='', citta='')
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_citta_normalize(self):
        """ test the first letter is capital and the rest is lower case"""
        payload= sample_payload(citta=' caSTelfranco vENEto')
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data['citta'],'Castelfranco Veneto')

    def test_citta_is_valid(self):
        payload = sample_payload(citta='   ')
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stato_estero_normalize(self):
        """ test the first letter is capital and the rest is lower case"""
        payload =sample_payload(stato="E",
                                stato_estero='  cOSTa  rICa  ',
                                provincia_ita="",
                                provincia_estero='San jose')
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data['stato_estero'],'Costa Rica')
    #
    def test_stato_estero_is_invalid(self):
        payload = sample_payload(
                                 nome='A',
                                 stato='E',
                                 stato_estero='   ',
                                 provincia_ita='',
                                 provincia_estero='San Jose')
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #
    def test_provincia_invalid(self):
        """ test if the  provincia is validated whetever
            the country is italian or outside Italy"""
        payload = sample_payload(
            stato='I',
            provincia_estero='',
            provincia_ita='padova'
        )
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #
    def test_provincia_is_coherent_with_country(self):
        payload = sample_payload(
                nome='a',
                stato='I',
                provincia_estero='padova',
                provincia_ita=''
        )
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # payload = { 'nome':'A',
        #             'stato': "E",
        #            'provincia_estero': "Hubei",
        #            'provincia_ita': 5
        #            }
        # res = self.client.patch(ME_URL, payload)
        # self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        #
        # payload = {'stato': "E",
        #            'nome':'A',
        #            'provincia_estero': "",
        #            'provincia_ita': 5
        #            }
        # res = self.client.patch(ME_URL, payload)
        # self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)





    # def test_create_user_with_provincia(self):
    #     payload = {
    #         'email': 'test2@silv.io',
    #         'password': 'testpass12345',
    #         'nome': 'test_name',
    #         'cognome': 'test cognome',
    #         'provincia_ita': '',
    #         'provincia_estero':'',
    #         'stato': 'I',
    #         'stato_estero':''
    #     }
    #     res = self.client.post(CREATE_USER_URL, payload)
