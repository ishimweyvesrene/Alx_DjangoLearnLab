# /tests.py
from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class AccountsTests(TestCase):
    def test_register(self):
        resp = self.client.post(reverse('accounts:register'), {
            'username': 'testuser',
            'email': 't@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        })
        # redirect to profile
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())
