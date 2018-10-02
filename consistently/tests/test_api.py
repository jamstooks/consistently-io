from json import loads
from django.urls import reverse
from rest_framework.test import APIClient

from .base import BaseTestCase
from consistently.apps.repos.models import Repository, Commit
from consistently.apps.integrations.models import Integration, INTEGRATION_TYPES
from consistently.apps.integrations.types.html.models import HTMLValidation


class BaseAPITestCase(BaseTestCase):
    """
    Only authenticated users have access to the api
    """

    def setUp(self):
        super(BaseAPITestCase, self).setUp()
        self.client = APIClient()
        self.login_client()
        self.restricted_methods = [self.client.get]

    def test_auth(self):
        """
            only authenticated users have access
        """
        self.client.logout()
        if hasattr(self, 'url'):
            response = self.client.get(self.url, format='json')
            self.assertEqual(response.status_code, 403)
            data = loads(response.content)
            self.assertEqual(
                data['detail'], 'Authentication credentials were not provided.')

    def test_permissions(self):
        """
        API requests for private repos or repos that don't belong
        to a user should be denied
        """
        if hasattr(self, 'private_url'):
            for m in self.restricted_methods:
                response = m(self.private_url, format='json')
                self.assertEqual(response.status_code, 403)

        if hasattr(self, 'restricted_url'):
            for m in self.restricted_methods:
                response = m(self.restricted_url, format='json')
                self.assertEqual(response.status_code, 403)


class GithubReposTestCase(BaseAPITestCase):
    """
    Test the view that provides a user's github repos
    """

    def setUp(self):
        """
            Set the url and api client
        """
        super(GithubReposTestCase, self).setUp()
        self.url = reverse('api:profile-repos')

    def test_list(self):

        self.login_client()
        response = self.client.get(self.url, format='json')
        data = loads(response.content)
        self.assertGreater(len(data), 0)
        self.assertTrue('prefix' in data[0])
        self.assertTrue('url' in data[0])
        self.assertTrue('id' in data[0])

        # this assumes that two of the three test repos belong to the
        # authenticated user, but one is private
        self.assertEqual(len(data) + 2, Repository.objects.count())
        # print(data)

        # make sure the private repo wasn't returned
        for r in data:
            self.assertNotEqual(r['github_id'], self.private_repo.github_id)


class ToggleRepoTestCase(BaseAPITestCase):
    """
    Test the view that toggles `is_active` status for each repo
    """

    def setUp(self):
        """
            Set the url and api client
        """
        super(ToggleRepoTestCase, self).setUp()
        self.url = reverse(
            'api:toggle-repo',
            kwargs={'github_id': self.repo.github_id})
        self.private_url = reverse(
            'api:toggle-repo',
            kwargs={'github_id': self.private_repo.github_id})
        self.restricted_url = reverse(
            'api:toggle-repo',
            kwargs={'github_id': self.restricted_repo.github_id})

        self.restricted_methods = [self.client.patch, self.client.put]

    def test_activate(self):

        self.repo.refresh_from_db()
        self.assertTrue(self.repo.is_active)

        # Deactivate
        response = self.client.patch(
            self.url, {'is_active': False}, format='json')
        data = loads(response.content)
        self.repo.refresh_from_db()
        self.assertFalse(self.repo.is_active)

        # Reactivate
        response = self.client.patch(
            self.url, {'is_active': True}, format='json')
        data = loads(response.content)
        self.repo.refresh_from_db()
        self.assertTrue(self.repo.is_active)

        # test with PUT
        response = self.client.put(
            self.url, {'is_active': False}, format='json')
        data = loads(response.content)
        self.repo.refresh_from_db()
        self.assertFalse(self.repo.is_active)


class IntegrationListTestCase(BaseAPITestCase):
    """
        Test listing and editing Integrations
    """

    def setUp(self):
        """
            Set the url and api client
        """
        super(IntegrationListTestCase, self).setUp()
        self.url = reverse(
            'api:integration-list',
            kwargs={'github_id': self.repo.github_id})

    def test_list(self):

        # integrations should be created as necessary
        Integration.objects.all().delete()
        self.assertEqual(Integration.objects.count(), 0)
        response = self.client.get(self.url)
        data = loads(response.content)
        self.assertEqual(len(data), len(INTEGRATION_TYPES))
        self.assertEqual(Integration.objects.count(), len(INTEGRATION_TYPES))


class IntegrationDetailTestCase(BaseAPITestCase):
    """
        Test listing and editing Integrations
    """

    def setUp(self):
        """
            Set the url and api client
        """
        super(IntegrationDetailTestCase, self).setUp()
        self.html = HTMLValidation.objects.create(repo=self.repo)
        self.url = reverse(
            'api:integration-detail',
            kwargs={'github_id': self.repo.github_id, 'pk': self.html.pk})
        self.private_url = reverse(
            'api:integration-detail',
            kwargs={
                'github_id': self.private_repo.github_id,
                'pk': self.private_html.pk
            })
        self.restricted_url = reverse(
            'api:integration-detail',
            kwargs={
                'github_id': self.restricted_repo.github_id,
                'pk': self.restricted_html.pk
            })

        self.restricted_methods = [self.client.patch]

    def test_detail(self):

        response = self.client.get(self.url)
        data = loads(response.content)
        self.assertTrue('is_active' in data)
        self.assertTrue('url_to_validate' in data)
        self.assertTrue('deployment_delay' in data)

    def test_not_found(self):

        url = reverse(
            'api:integration-detail',
            kwargs={'github_id': 12222, 'pk': 19999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update(self):

        valid_url = 'http://www.google.com'
        response = self.client.patch(
            self.url,
            {
                'is_active': False,
                'url_to_validate': valid_url,
                'deployment_delay': None
            },
            format='json')
        data = loads(response.content)
        self.html.refresh_from_db()
        self.assertEqual(self.html.url_to_validate, valid_url)
        self.assertFalse(self.html.is_active)

        # validation
        response = self.client.patch(
            self.url,
            {
                'is_active': True,
                'url_to_validate': None,
                'deployment_delay': None
            },
            format='json')
        data = loads(response.content)
        self.assertEqual(
            data['url_to_validate'], ['Required when active.'])

        self.html.refresh_from_db()
        self.assertFalse(self.html.is_active)

        # additional validation
        response = self.client.patch(
            self.url,
            {
                'is_active': True,
                'url_to_validate': "",
                'deployment_delay': None
            },
            format='json')
        data = loads(response.content)
        self.assertEqual(
            data['url_to_validate'], ['Required when active.'])

        self.html.refresh_from_db()
        self.assertFalse(self.html.is_active)

        # valid
        response = self.client.patch(
            self.url,
            {
                'is_active': True,
                'url_to_validate': valid_url,
                'deployment_delay': None
            },
            format='json')
        self.html.refresh_from_db()
        self.assertEqual(self.html.url_to_validate, valid_url)
        self.assertTrue(self.html.is_active)


class GithubWebhookTestCase(BaseAPITestCase):
    """
    Test handling of the github webhook
    """

    def setUp(self):
        """
            Set the url and api client
        """
        super(GithubWebhookTestCase, self).setUp()
        self.initial_commit_count = Commit.objects.count()

    def test_list(self):

        url = reverse('api:github-webhook')

        good_payload = {
            "ref": "refs/heads/master",
            "head_commit": {
                "id": "121212",
                "message": "test commit",
                "timestamp": "2018-10-02T16:01:56-04:00"
            },
            "repository": {
                "id": self.repo.github_id
            }
        }

        response = self.client.post(
            url, good_payload, format='json')
        data = loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], "ACCEPTED")
        self.assertEqual(Commit.objects.count(), self.initial_commit_count + 1)
