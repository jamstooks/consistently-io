from django.http import Http404
from django.urls import reverse

from .base import BaseTestCase


class RepoListTestCase(BaseTestCase):

    def setUp(self):
        """
            Set the url
        """
        super(RepoListTestCase, self).setUp()
        self.url = reverse('repos:prefix-repo-list',
                           kwargs={'prefix': self.user.username})

    def test_list(self):
        """
            We should have a list of connected repositories
        """
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['repo_list']), 1)

        # when there are no repos, raise 404
        url = reverse('repos:prefix-repo-list', kwargs={'prefix': 'django'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class RepoDetailTestCase(BaseTestCase):

    def setUp(self):
        """
            Set the url
        """
        super(RepoDetailTestCase, self).setUp()
        self.url = reverse('repos:repo-detail',
                           kwargs={
                               'prefix': self.user.username,
                               'name': self.repo.name
                           })

    def test_list(self):
        """
            We should have a list of connected repositories
        """
        response = self.client.get(self.url)
        self.assertEqual(response.context['repo'], self.repo)

        # test inactive repo for 404
        url = reverse(
            'repos:repo-detail',
            kwargs={
                'prefix': self.user.username,
                'name': self.private_repo.name
            })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ProfileTestCase(BaseTestCase):

    def setUp(self):
        """
            Set the url
        """
        super(ProfileTestCase, self).setUp()
        self.url = reverse('repos:profile')

    def test_auth_req(self):

        # confirm a user who isn't authenticated gets redirected to login
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        login_url = reverse('social:begin', args=['github', ])
        self.assertIn(login_url, response.url)

        self.login_client()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
