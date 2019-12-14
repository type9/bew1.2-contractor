import unittest

from django.test import TestCase, Client
from django.contrib.auth.models import User
# Create your tests here.

class UserTestCase(TestCase):
    def test_user_creation(self):
        user = User(username='johnny')
        user.save()

        self.assertEqual(user.username, 'johnny')

    def test_signup_render(self):
        response = self.client.get('/accounts/signup')
        self.assertEqual(response.status_code, 301)