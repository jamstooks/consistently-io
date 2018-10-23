from consistently.tests.base import BaseTestCase
from consistently.tests.utils import MockRequest
from .models import PageSpeed
from .serializer import PageSpeedSerializer
from ...models import IntegrationStatus

from unittest import mock
import json


class PageSpeedBaseCase(BaseTestCase):

    def setUp(self):
        super(PageSpeedBaseCase, self).setUp()

        self.ps = PageSpeed.objects.create(
            repo=self.repo,
            is_active=False,
            url="http://www.example.com",
            deployment_delay="1"
        )


class PageSpeedCase(PageSpeedBaseCase):

    def test_integration_type_assignment(self):

        self.assertEqual(self.ps.integration_type, 'pagespeed')


class SerializerTestCase(PageSpeedBaseCase):

    def test_object_serialization(self):

        serializer = PageSpeedSerializer(instance=self.ps)
        self.assertCountEqual(
            serializer.data.keys(),
            ['is_active', 'url',  'use_mobile_strategy', 'deployment_delay'])

    def test_validation(self):

        serializer_data = {
            'is_active': False,
            'deployment_delay': 10,
        }

        # data is always valid when `is_active` is False
        serializer = PageSpeedSerializer(
            instance=self.ps, data=serializer_data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.ps.refresh_from_db()
        self.assertFalse(self.ps.is_active)
        self.assertEqual(self.ps.deployment_delay, 10)
        self.assertFalse(self.ps.use_mobile_strategy)

        # when `is_active` is True then `url` is required
        serializer_data['is_active'] = True
        serializer = PageSpeedSerializer(
            instance=self.ps, data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['url'][0]),
            'Required when active.')

        # 'url' must be a valid URL
        serializer_data['url'] = "abc"
        serializer = PageSpeedSerializer(
            instance=self.ps, data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['url'][0]),
            'Enter a valid URL.')

        # Valid url should validate when `is_active` is True
        serializer_data['url'] = "http://www.example.com"
        serializer_data['use_mobile_strategy'] = True
        serializer = PageSpeedSerializer(
            instance=self.ps, data=serializer_data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.ps.refresh_from_db()
        self.assertTrue(self.ps.is_active)
        self.assertEqual(self.ps.url, "http://www.example.com")
        self.assertTrue(self.ps.use_mobile_strategy)


# Mock request.get for the worker tests
def fake_get(*args, **kwargs):

    # print(kwargs['params'])
    url = kwargs['params']['url']

    if 'error.site' in url:
        return MockRequest(
            status_code=200,
            json_data={'error': {'errors': ['ERROR']}})
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
class WorkerTestCase(PageSpeedBaseCase):

    def setUp(self):
        super(WorkerTestCase, self).setUp()
        self.ps = PageSpeed.objects.create(
            repo=self.repo,
            is_active=False,
            url="https://valid.site/",
            deployment_delay="1"
        )

    def test_run(self):

        with_settings = [
            {
                'fields': {
                    'url': 'https://error.site',
                    'use_mobile_strategy': False
                }
            }
        ]

        status = IntegrationStatus.objects.create(
            integration=self.ps,
            commit=self.commit,
            with_settings=json.dumps(with_settings))

        # when google returns errors
        self.ps.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.failed)
        self.assertEqual(status.value, "Failed")
        self.assertRegex(status.details, 'ERROR')

        # test with a failing site
        with_settings[0]['fields']['url'] = 'https://fail.site'
        status.with_settings = json.dumps(with_settings)
        status.save()
        self.ps.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.failed)
        self.assertEqual(status.value, "Desktop: 74%")

        # test with a connection error to google
        with_settings[0]['fields']['url'] = 'https://broken.site'
        status.with_settings = json.dumps(with_settings)
        status.save()
        self.ps.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.failed)

        # test with a passing site
        with_settings[0]['fields']['url'] = 'https://pass.site'
        status.with_settings = json.dumps(with_settings)
        status.save()
        self.ps.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.passed)
        self.assertEqual(status.value, "Desktop: 91%")

        # test with a mobile strategy
        with_settings[0]['fields']['url'] = 'https://pass.site'
        with_settings[0]['fields']['use_mobile_strategy'] = True
        status.with_settings = json.dumps(with_settings)
        status.save()
        self.ps.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.passed)
        self.assertEqual(status.value, "Mobile: 91%")
