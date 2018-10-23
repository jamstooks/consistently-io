from consistently.tests.base import BaseTestCase
from .models import HTMLValidation
from .serializer import HTMLValidationSerializer
from ...models import IntegrationStatus

from unittest import mock


class HTMLBaseCase(BaseTestCase):

    def setUp(self):
        super(HTMLBaseCase, self).setUp()
        self.html = HTMLValidation.objects.create(
            repo=self.repo,
            is_active=False,
            url_to_validate="http://www.example.com",
            deployment_delay="1"
        )


class HTMLTestCase(HTMLBaseCase):

    def test_integration_type_assignment(self):
        self.assertEqual(self.html.integration_type, 'html')


class SerializerTestCase(HTMLBaseCase):

    def test_object_serialization(self):

        serializer = HTMLValidationSerializer(instance=self.html)
        self.assertCountEqual(
            serializer.data.keys(),
            ['is_active', 'url_to_validate',  'deployment_delay'])

    def test_validation(self):

        serializer_data = {
            'is_active': False,
            'deployment_delay': 1
        }

        # data is generally valid when `is_active` is False
        serializer = HTMLValidationSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())

        # when `is_active` is True then `url_to_validate` is required
        serializer_data['is_active'] = True
        serializer = HTMLValidationSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['url_to_validate'][0]),
            'Required when active.')

        # 'url_to_validate' must be a valid URL
        serializer_data['url_to_validate'] = "abc"
        serializer = HTMLValidationSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['url_to_validate'][0]),
            'Enter a valid URL.')

        # Valid url should validate when `is_active` is True
        serializer_data['url_to_validate'] = "http://www.google.com"
        serializer = HTMLValidationSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())


# Mock request.get for the worker tests
def fake_get(*args, **kwargs):

    class MockRequest:
        def __init__(self, status_code=200, json_data={}):
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data

    if 'invalid.url' in args[0]:
        return MockRequest(
            status_code=200, json_data={'messages': [{'type': 'error'}]})
    elif 'broken.url' in args[0]:
        return MockRequest(status_code=500)
    else:
        return MockRequest(status_code=200, json_data={'messages': []})


@mock.patch('requests.get', fake_get)
class WorkerTestCase(HTMLBaseCase):

    def test_run(self):

        status = IntegrationStatus.objects.create(
            integration=self.html,
            commit=self.commit,
            with_settings='[{"fields": {"url_to_validate": "https://invalid.url"}}]')

        # test with an invalid url
        self.html.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.failed)
        self.assertEqual(status.value, "Failed")
        self.assertRegex(status.details, "\d+ Errors, \d+ Warnings")

        # test with a valid url
        status.with_settings = '[{"fields": {"url_to_validate": "https://valid.url"}}]'
        status.save()
        self.html.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.passed)

        # test with a connection error
        status.with_settings = '[{"fields": {"url_to_validate": "https://broken.url"}}]'
        status.save()
        self.html.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.failed)
