from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@silv.io'
        password = 'Password123'
        # nome = 'test nome'
        # cognome = 'test cognome'
        user = get_user_model().objects.create_user(
			email=email,
			password=password,
            # nome=nome,
            # cognome=cognome
		)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ test the email for a new user i normalized """
        email = 'test@SILV.io'
        password = 'Password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            )
        self.assertEqual(email.lower(), user.email)

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_new_superuser(self):
        """ test createing super user """
        email = 'super@silv.io'
        password = 'admin123'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_staff)

    # def test_nome_invalid(self):
    #     """Test creating user with no email raises error"""
    #     with self.assertRaises(ValueError):
    #         get_user_model().objects.create_user(
    #                         email="super@silv.io",
    #                         password='test123',
    #                         nome="Alessandro123" )
    #
    # def test_user_details_create(self):
    #     """ test creating user details """
    #     user = sampleuser()
    #     telefono = "37375526760"
    #     via = "via e man dal culo 7"
    #     citta = 'Padova`'
    #     details = models.UserDetails.objects.create(
    #         user=user,
    #         telefono=telefono,
    #         indirizzo=via,
    #         citta=citta,
    #         # provincia_ita=citta,
    #         provincia_estero='',
    #         stato='I',
    #         stato_estero=''
    #     )
    #
    #     self.assertEqual(details.user, user)
    #     self.assertEqual(details.telefono, telefono)
    #     self.assertEqual(details.indirizzo, via)
