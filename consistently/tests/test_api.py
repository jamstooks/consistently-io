from json import loads
from django.urls import reverse
from rest_framework.test import APIClient

from .base import BaseTestCase, TEST_GITHUB_REPO
from consistently.apps.repos.models import Repository


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

    def test_create_and_delete(self):

        response = self.client.post(
            self.url,
            {'name': TEST_GITHUB_REPO, 'owner': self.user.id},
            format='json')
        data = loads(response.content)
        self.assertEqual(data['name'], TEST_GITHUB_REPO)

        response = self.client.get(self.url, format='json')
        data = loads(response.content)
        self.assertEqual(len(data), 2)
        
        repo = Repository.objects.get(name=TEST_GITHUB_REPO)
        
        del_url = reverse('api:repository-detail', args=[repo.id])
        response = self.client.delete(del_url, format='json')
        self.assertEqual(response.status_code, 204)
        
        response = self.client.get(self.url, format='json')
        data = loads(response.content)
        self.assertEqual(len(data), 1)
        
        # test invalid repo
        response = self.client.post(
            self.url,
            {'name': 'bugus-repo-name', 'owner': self.user.id},
            format='json')
        data = loads(response.content)
        self.assertEqual(
            data['non_field_errors'], ['No matching repo on Github'])
