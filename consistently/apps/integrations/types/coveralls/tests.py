from consistently.tests.base import BaseTestCase
from consistently.tests.utils import MockRequest
from .models import Coveralls
from .serializer import CoverallsSerializer
from ...models import IntegrationStatus
from ...tasks import NeedsToRetry


from unittest import mock


class CoverallsTestCase(BaseTestCase):

    def test_create(self):
        i = Coveralls.objects.create(repo=self.repo, is_active=False)
        self.assertEqual(i.integration_type, 'coveralls')


class WorkerTestCase(BaseTestCase):

    def setUp(self):
        super(WorkerTestCase, self).setUp()
        self.coveralls = Coveralls.objects.create(
            repo=self.repo,
            is_active=False,
            build_time="1"
        )
        self.status = IntegrationStatus.objects.create(
            integration=self.coveralls,
            commit=self.commit,
            with_settings='[{}]')

    def test_run(self):

        # network error should return None
        with mock.patch(
                'requests.get', return_value=MockRequest(status_code=500)):
            with self.assertRaises(NeedsToRetry):
                self.coveralls.run(self.status)

        base_response = {
            "created_at": "2018-10-10T16:30:47Z",
            "commit_sha": self.commit.sha,
            "repo_name": "jamstooks/consistently-io",
            "covered_percent": 91.31}

        # mimic a passing result
        with mock.patch(
            'requests.get', return_value=MockRequest(
                status_code=200, json_data=base_response)):

            self.coveralls.run(self.status)
            self.status.refresh_from_db()
            self.assertEqual(
                self.status.status,
                IntegrationStatus.STATUS_CHOICES.passed)
            self.assertEqual(self.status.value, "91% Coverage")

        # mimic a failing result
        base_response['covered_percent'] = 0
        with mock.patch(
            'requests.get', return_value=MockRequest(
                status_code=200, json_data=base_response)):

            self.coveralls.run(self.status)
            self.status.refresh_from_db()
            self.assertEqual(
                self.status.status,
                IntegrationStatus.STATUS_CHOICES.failed)
            self.assertEqual(self.status.value, "0% Coverage")

        # mimic null result (should retry)
        with mock.patch(
            'requests.get', return_value=MockRequest(
                status_code=200, json_data=None)):

            with self.assertRaises(NeedsToRetry):
                self.coveralls.run(self.status)


class SerializerTestCase(BaseTestCase):

    def test_object_serialization(self):

        serializer = CoverallsSerializer(instance=self.repo)
        self.assertCountEqual(
            serializer.data.keys(),
            ['is_active', 'build_time'])
