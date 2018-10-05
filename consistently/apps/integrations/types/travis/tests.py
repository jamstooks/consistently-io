from consistently.tests.base import BaseTestCase
from .models import Travis
from .utils import (
    get_travis_state, CANCELED, CREATED, ERRORED, FAILED, PASSED,
    QUEUED, READY, STARTED)
from ...models import IntegrationStatus
from ...tasks import NeedsToRetry


from unittest import mock


class TravisTestCase(BaseTestCase):

    def test_create(self):
        travis = Travis.objects.create(repo=self.repo, is_active=False)
        self.assertEqual(travis.integration_type, 'travis')


class MockRequest:
    def __init__(self, status_code=200, json_data={}):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


class WorkerTestCase(BaseTestCase):

    def setUp(self):
        super(WorkerTestCase, self).setUp()
        self.travis = Travis.objects.create(
            repo=self.repo,
            is_active=False,
            build_time="1"
        )
        self.status = IntegrationStatus.objects.create(
            integration=self.travis,
            commit=self.commit,
            with_settings='[{}]')

    def test_get_travis_state(self):

        # network error should return None
        with mock.patch(
                'requests.get', return_value=MockRequest(status_code=500)):
            state = get_travis_state(self.commit)
            self.assertIsNone(state)

        base_response = {
            '@pagination': {
                'count': 10
            },
            'builds': [{
                'commit': {
                    'sha': self.commit.sha
                }
            }]
        }

        for state in [
                CANCELED, CREATED, ERRORED, FAILED, PASSED, QUEUED, READY, STARTED]:

            base_response['builds'][0]['state'] = state
            with mock.patch(
                    'requests.get',
                    return_value=MockRequest(
                        status_code=200, json_data=base_response)):

                s = get_travis_state(self.commit)
                self.assertEqual(s, state)

    def test_run(self):

        target = 'consistently.apps.integrations.types.travis.utils.get_travis_state'

        # any of these states should raise NeedsToRetry
        retry_states = [CREATED, QUEUED, READY, STARTED, None]
        for state in retry_states:
            with mock.patch(target, return_value=state):
                with self.assertRaises(NeedsToRetry):
                    self.travis.run(self.status)
                self.status.refresh_from_db()
                self.assertEqual(self.status.value, state)
                self.assertEqual(self.status.status,
                                 IntegrationStatus.STATUS_CHOICES.waiting)

        # any of these states should result in failure
        failure_states = [CANCELED, ERRORED, FAILED]
        for state in failure_states:
            with mock.patch(target, return_value=state):
                self.travis.run(self.status)
                self.status.refresh_from_db()
                self.assertEqual(self.status.value, state)
                self.assertEqual(self.status.status,
                                 IntegrationStatus.STATUS_CHOICES.failed)

        # success
        with mock.patch(target, return_value=PASSED):
            self.travis.run(self.status)
            self.status.refresh_from_db()
            self.assertEqual(self.status.value, PASSED)
            self.assertEqual(self.status.status,
                             IntegrationStatus.STATUS_CHOICES.passed)
