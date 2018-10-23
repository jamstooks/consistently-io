from consistently.tests.base import BaseTestCase
from consistently.tests.utils import MockRequest
from .models import PageSpeed
from .serializer import PageSpeedSerializer
from ...models import IntegrationStatus

from unittest import mock


class PageSpeedCase(BaseTestCase):

    def test_integration_type_assignment(self):
        ps = PageSpeed.objects.create(
            repo=self.repo,
            is_active=False,
            url="http://www.example.com",
            deployment_delay="1"
        )
        self.assertEqual(ps.integration_type, 'pagespeed')


class SerializerTestCase(BaseTestCase):

    def test_object_serialization(self):

        serializer = PageSpeedSerializer(instance=self.repo)
        self.assertCountEqual(
            serializer.data.keys(),
            ['is_active', 'url',  'deployment_delay'])

    def test_validation(self):

        serializer_data = {
            'is_active': False,
            'deployment_delay': 1
        }

        # data is always valid when `is_active` is False
        serializer = PageSpeedSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())

        # when `is_active` is True then `url` is required
        serializer_data['is_active'] = True
        serializer = PageSpeedSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['url'][0]),
            'Required when active.')

        # 'url' must be a valid URL
        serializer_data['url'] = "abc"
        serializer = PageSpeedSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['url'][0]),
            'Enter a valid URL.')

        # Valid url should validate when `is_active` is True
        serializer_data['url'] = "http://www.example.com"
        serializer = PageSpeedSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())


# Mock request.get for the worker tests
def fake_get(*args, **kwargs):

    url = kwargs['params']['url']

    if 'error.site' in url:
        return MockRequest(
            status_code=200, json_data={'error': {'errors': ['ERROR']}})
    elif 'broken.site' in url:
        return MockRequest(status_code=500)
    elif 'fail.site' in url:
        return MockRequest(
            status_code=200,
            json_data={'pageStats': 'stats', 'ruleGroups': {'SPEED': {'score': 74}}})
    else:
        return MockRequest(
            status_code=200,
            json_data={'pageStats': 'stats', 'ruleGroups': {'SPEED': {'score': 91}}})


@mock.patch('requests.get', fake_get)
class WorkerTestCase(BaseTestCase):

    def setUp(self):
        super(WorkerTestCase, self).setUp()
        self.ps = PageSpeed.objects.create(
            repo=self.repo,
            is_active=False,
            url="https://valid.site/",
            deployment_delay="1"
        )

    def test_run(self):

        status = IntegrationStatus.objects.create(
            integration=self.ps,
            commit=self.commit,
            with_settings='[{"fields": {"url": "https://error.site"}}]')

        # when google returns errors
        self.ps.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.failed)
        self.assertEqual(status.value, "Failed")
        self.assertRegex(status.details, 'ERROR')

        # test with a passing site
        status.with_settings = '[{"fields": {"url": "https://passing.site"}}]'
        status.save()
        self.ps.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.passed)
        self.assertEqual(status.value, "91 / 100")

        # test with a failing site
        status.with_settings = '[{"fields": {"url": "https://fail.site"}}]'
        status.save()
        self.ps.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.failed)
        self.assertEqual(status.value, "74 / 100")

        # test with a connection error to google
        status.with_settings = '[{"fields": {"url": "https://broken.site"}}]'
        status.save()
        self.ps.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.failed)
