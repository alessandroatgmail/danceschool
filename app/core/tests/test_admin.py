from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@londonappdev.com',
            password='password123',
            # nome='test nome',
            # cognome='test cognome'

        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='password123',
            # nome='nome proprio primo utente',
            # cognome='cognome secondo utente'
        )

    def test_retireve_user_created(self):
        new_user = get_user_model().objects.filter(id=self.user.id)
        self.assertEqual(new_user[0], self.user)

    def test_users_listed(self):
        """Test that users are listed on the user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertContains(res, self.user.cognome)
        self.assertContains(res, self.user.email)
