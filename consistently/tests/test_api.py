from json import loads
from django.urls import reverse
from rest_framework.test import APIClient

from .base import BaseTestCase, TEST_GITHUB_REPO


class RepoListTestCase(BaseTestCase):

    def setUp(self):
        """
            Set the url and api client
        """
        super(RepoListTestCase, self).setUp()

        self.client = APIClient()
        self.url = reverse('api:repository-list')

    def test_list(self):

        response = self.client.get(self.url, format='json')
        data = loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'test')

    def test_create(self):

        response = self.client.post(
            self.url,
            {'name': TEST_GITHUB_REPO, 'owner': self.user.id},
            format='json')
        data = loads(response.content)
        self.assertEqual(data['name'], TEST_GITHUB_REPO)

        response = self.client.get(self.url, format='json')
        data = loads(response.content)
        self.assertEqual(len(data), 2)
