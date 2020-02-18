from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from django.conf.urls.i18n import i18n_patterns
from core import models
from core.models import Provincia
from django.core.exceptions import ValidationError
from users.serializers import UserDetailSerializer


ADMINUSER_URL = reverse ('adminApi:user-list')
CREATE_USER_URL = reverse('users:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)

def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)

def detail_url(user_id):
    """Return recipe detail URL"""
    return reverse('adminApi:user-detail', args=[user_id])

def sample_provincia(prov):
    p = Provincia.objects.create(nome=prov)
    return p

class PublicIngredientApiTests(TestCase):

    def setUp(self):
        self.user = create_user(
            email='test@silv.io',
            password='pwd12345678',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_login_required(self):
        res = self.client.get(ADMINUSER_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateAdminApiTests(TestCase):

     def setUp(self):
        self.client = APIClient()

        self.superuser = get_user_model().objects.create_superuser(
                'super@silv.io',
                'pwd123456789'
                )
        self.client.force_authenticate(self.superuser)
        self.user = get_user_model().objects.create_superuser(
                'testadmin@silv.io',
                'pwd123456789'
                )

     def test_retrive_users_succesfull(self):
         res = self.client.get(ADMINUSER_URL)
         self.assertEqual(res.status_code, status.HTTP_200_OK)

     def test_view_user_detail(self):
         url = detail_url(self.user.id)
         print (url)
         # res = self.client.get(url)
         # serializer = UserDetailSerializer(self.user)
         # self.assertEqual(res.data, serializer.data)


# class PrivateAdminApi(TestCase):
#
#     def setUp(self):
#         self.client = APIClient()
