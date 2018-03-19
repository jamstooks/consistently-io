from django.urls import reverse

from .base import BaseTestCase


class RepoListTestCase(BaseTestCase):

    def setUp(self):
        """
            Set the url
        """
        super(RepoListTestCase, self).setUp()
        self.url = reverse('repos:user-repo-list', args=(self.user.username, ))

    def test_other_user(self):
        """
            Other or anon users should see just a list
            of public connected repos for the user.
        """
        # @todo - test with one logged in user on another user.
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['unconnected_repos']), 0)
        self.assertEqual(len(response.context['connected_repos']), 1)

    def test_current_user(self):
        """
            An authenticated user should see his/her own repo
        """
        self.login_client()
        response = self.client.get(self.url)
        self.assertEqual(
            response.context['unconnected_repos'].__class__.__name__,
            'PaginatedList')
