import unittest

from django.test import TestCase, Client
from django.contrib.auth.models import User

class APITestCase(TestCase):
    def riders_api_render(self):
        response = self.client.get('/api/riders')
        self.assertEqual(response.status_code, 200)

    def communities_api_render(self):
        response = self.client.get('/api/communities')
        self.assertEqual(response.status_code, 200)

    def rideshares_api_render(self):
        response = self.client.get('/api/rideshares')
        self.assertEqual(response.status_code, 200)
