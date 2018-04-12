from django.urls import reverse

from .base import BaseTestCase


class RepoListTestCase(BaseTestCase):

    def setUp(self):
        """
            Set the url
        """
        super(RepoListTestCase, self).setUp()
        self.url = reverse('repos:user-repo-list', args=(self.user.username, ))

    def test_list(self):
        """
            We should have a list of connected repositories
        """
        # @todo - test with one logged in user on another user.
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['connected_repos']), 1)


class ProfileTestCase(BaseTestCase):

    def setUp(self):
        """
            Set the url
        """
        super(ProfileTestCase, self).setUp()
        self.url = reverse('repos:profile', args=(self.user.username, ))

    def test_list(self):
        """
            We should have a list of githu repositories
        """
        self.login_client()
        # @todo - test permissions
        response = self.client.get(self.url)
        # self.assertEqual(len(response.context['connected_repos']), 1)
