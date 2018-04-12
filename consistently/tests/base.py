import os
from django.contrib.auth.models import User
from django.test import Client, TestCase
from social_django.models import UserSocialAuth

from consistently.apps.repos.models import Repository


TEST_USERNAME = 'jamstooks'
TEST_GITHUB_TOKEN = os.environ.get('TEST_GITHUB_TOKEN')
TEST_GITHUB_REPO_ID = os.environ.get('TEST_GITHUB_REPO_ID', 14995323)


class BaseTestCase(TestCase):

    def setUp(self):
        """
            Create a test repo and a user.
        """

        self.user = User.objects.create(
            username=TEST_USERNAME, password='secret',)
        self.user.set_password('secret')
        self.user.save()

        self.repo = Repository(
            github_id=1,
            name='test',
            prefix=self.user.username,
            added_by=self.user,
            full_name="%s/%s" % ('test', self.user.username))
        self.repo.save()

        usa = UserSocialAuth(
            user=self.user,
            provider='github',
            uid='',
            extra_data={
                'access_token': TEST_GITHUB_TOKEN})
        usa.save()

        self.client = Client()

    def login_client(self):
        self.client.login(username=TEST_USERNAME, password='secret')
