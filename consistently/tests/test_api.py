from json import loads
from django.urls import reverse
from rest_framework.test import APIClient

from .base import BaseTestCase, TEST_GITHUB_REPO_ID
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

        self.login_client()

        response = self.client.post(
            self.url,
            {'github_id': TEST_GITHUB_REPO_ID, },
            format='json')
        data = loads(response.content)
        self.assertEqual(data['github_id'], TEST_GITHUB_REPO_ID)

        response = self.client.get(self.url, format='json')
        data = loads(response.content)
        self.assertEqual(len(data), 2)

        repo = Repository.objects.get(github_id=TEST_GITHUB_REPO_ID)

        del_url = reverse('api:repository-detail', args=[repo.id])
        response = self.client.delete(del_url, format='json')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(self.url, format='json')
        data = loads(response.content)
        self.assertEqual(len(data), 1)

        # test invalid repo
        response = self.client.post(
            self.url,
            {'github_id': '0'},
            format='json')
        data = loads(response.content)
        self.assertEqual(
            data['non_field_errors'], ['No matching repo on Github'])


class GithubReposTestCase(BaseTestCase):
    """
    Test the view that shows a user's github repos
    """

    def setUp(self):
        """
            Set the url and api client
        """
        super(GithubReposTestCase, self).setUp()

        self.client = APIClient()
        self.url = reverse('api:unconnected-repos')

    def test_perms(self):
        """
            only authenticated users have access
        """
        response = self.client.get(self.url, format='json')
        data = loads(response.content)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data['detail'], 'Authentication credentials were not provided.')

    def test_list(self):

        self.login_client()
        response = self.client.get(self.url, format='json')
        data = loads(response.content)
        self.assertGreater(len(data), 0)
        self.assertTrue('full_name' in data[0])
