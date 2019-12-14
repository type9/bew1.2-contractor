import unittest

from django.test import TestCase, Client
from django.contrib.auth.models import User
from rideshare.models import Community, Rider

class CommunityTestCase(TestCase):
    def test_community_slugify_on_save(self):
        """ Tests the slug generated when saving a Page. """
        user = Rider()
        user.save()

        community = Community(title="Test Community", description="test", owner=user)
        community.save()

        self.assertEqual(community.slug, "test-community")

class CommunityDetailViewTests(TestCase):
    def test_view_community(self):
        user = Rider()
        user.save()
        
        community = Community.objects.create(title="Test Community", description="test", owner=user)
        community.save()

        response = self.client.get('/cm/test-community')

        self.assertEqual(response.status_code, 301)