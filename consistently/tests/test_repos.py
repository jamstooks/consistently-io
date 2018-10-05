from django.http import Http404
from django.urls import reverse

from .base import BaseTestCase
from consistently.apps.repos import permissions
from consistently.apps.integrations.types.html.models import HTMLValidation


class CommitSaveTestCase(BaseTestCase):

    def setUp(self):

        super(CommitSaveTestCase, self).setUp()

        from consistently.apps.integrations.models import IntegrationStatus

        self.html = HTMLValidation.objects.create(repo=self.repo)
        self.status = IntegrationStatus.objects.create(
            commit=self.commit,
            integration=self.html,
            status=IntegrationStatus.STATUS_CHOICES.waiting)

    def test_get_counts(self):

        self.assertIsNone(self.commit.waiting_count)
        self.assertIsNone(self.commit.pass_count)
        self.assertIsNone(self.commit.fail_count)

        self.commit.get_counts()
        self.commit.refresh_from_db()
        self.assertEqual(self.commit.waiting_count, 1)
        self.assertEqual(self.commit.pass_count, 0)
        self.assertEqual(self.commit.fail_count, 0)


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


class RepoSettingsTestCase(BaseTestCase):

    def setUp(self):
        """
            Set the url
        """
        super(RepoSettingsTestCase, self).setUp()
        self.url = reverse(
            'repos:repo-settings',
            args=[self.repo.prefix, self.repo.name])
        self.private_url = reverse(
            'repos:repo-settings',
            args=[self.private_repo.prefix, self.private_repo.name])
        self.restricted_url = reverse(
            'repos:repo-settings',
            args=[self.restricted_repo.prefix, self.restricted_repo.name])
        self.restricted_repo.is_active = True
        self.restricted_repo.save()

    def tearDown(self):
        self.restricted_repo.is_active = False
        self.restricted_repo.save()

    def test_admin_required(self):

        # confirm a user who isn't authenticated gets redirected to login
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        # login_url = reverse('social:begin', args=['github', ])
        # self.assertIn(login_url, response.url)

        # assert that a user can access their repos
        self.login_client()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # but can't access the restricted repo
        response = self.client.get(self.restricted_url)
        self.assertEqual(response.status_code, 403)

        # and can't access the private repo
        response = self.client.get(self.private_url)
        self.assertEqual(response.status_code, 404)


class PermissionsTestCase(BaseTestCase):

    def test_user_is_repo_admin(self):

        # The base user has access to the base repo
        self.assertTrue(permissions.user_is_repo_admin(
            self.user, self.repo))

        # The base user does not have access to the restricted repo
        self.assertFalse(permissions.user_is_repo_admin(
            self.user, self.restricted_repo))

    def test_repo_is_public(self):

        # public repo
        self.assertTrue(permissions.repo_is_public(self.repo))

        # private repo
        self.assertFalse(permissions.repo_is_public(self.private_repo))
