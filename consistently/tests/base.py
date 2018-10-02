import datetime
import os

from django.contrib.auth.models import User
from django.test import Client, TestCase
from social_django.models import UserSocialAuth

from consistently.apps.repos.models import Repository, Commit
from consistently.apps.integrations.types.html.models import HTMLValidation


TEST_USERNAME = os.environ.get('TEST_GITHUB_USERNAME', 'jamstooks')
TEST_GITHUB_TOKEN = os.environ.get('TEST_GITHUB_TOKEN')

# public repo the user has access too
TEST_REPO_ID = os.environ.get('TEST_REPO_ID', 4876788)
TEST_REPO_PREFIX = os.environ.get('TEST_REPO_PREFIX', TEST_USERNAME)
TEST_REPO_NAME = os.environ.get('TEST_REPO_NAME', 'django-s3-folder-storage')

# private repo the user has access too
PRIVATE_REPO_ID = os.environ.get('TEST_REPO_ID', 95119441)
PRIVATE_REPO_PREFIX = os.environ.get('TEST_REPO_PREFIX', TEST_USERNAME)
PRIVATE_REPO_NAME = os.environ.get('TEST_REPO_NAME', 'camera-trap')

# public repo the user does not have access too
RESTRICTED_REPO_ID = os.environ.get('TEST_REPO_ID', 4164482)
RESTRICTED_REPO_PREFIX = os.environ.get('TEST_REPO_PREFIX', 'django')
RESTRICTED_REPO_NAME = os.environ.get('TEST_REPO_NAME', 'django')


class BaseTestCase(TestCase):

    def setUp(self):
        """
            Create a test repo and a user.
        """

        self.user = User.objects.create(
            username=TEST_USERNAME, password='secret',)
        self.user.set_password('secret')
        self.user.save()

        self.repo = Repository.objects.create(
            github_id=TEST_REPO_ID,
            is_active=True,
            prefix=TEST_REPO_PREFIX,
            name=TEST_REPO_NAME,
            activated_by=self.user)

        self.private_repo = Repository.objects.create(
            github_id=PRIVATE_REPO_ID,
            is_active=False,
            prefix=PRIVATE_REPO_PREFIX,
            name=PRIVATE_REPO_NAME,
            activated_by=self.user)

        self.restricted_repo = Repository.objects.create(
            github_id=RESTRICTED_REPO_ID,
            is_active=False,
            prefix=RESTRICTED_REPO_PREFIX,
            name=RESTRICTED_REPO_NAME,
            activated_by=self.user)

        self.private_html = HTMLValidation.objects.create(
            repo=self.private_repo)
        self.restricted_html = HTMLValidation.objects.create(
            repo=self.restricted_repo)

        self.commit = Commit.objects.create(
            repo=self.repo,
            sha="bogus-sha",
            message="commit message",
            github_timestamp=datetime.datetime.now(datetime.timezone.utc))

        self.repo.latest_commit = self.commit
        self.repo.save()

        auth = UserSocialAuth.objects.create(
            user=self.user,
            provider='github',
            uid='',
            extra_data={
                'access_token': TEST_GITHUB_TOKEN})

        self.client = Client()

    def login_client(self):
        self.client.login(username=TEST_USERNAME, password='secret')
