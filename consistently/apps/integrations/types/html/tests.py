from consistently.tests.base import BaseTestCase
from .models import HTMLValidation
from .serializer import HTMLValidationSerializer
from ...models import IntegrationStatus


class HTMLTestCase(BaseTestCase):

    def test_create(self):
        html = HTMLValidation(
            repo=self.repo,
            is_active=False,
            url_to_validate="http://www.example.com",
            deployment_delay="1"
        )
        html.save()

        self.assertEqual(html.integration_type, 'html')


class SerializerTestCase(BaseTestCase):

    def test_object_serialization(self):

        serializer = HTMLValidationSerializer(instance=self.repo)
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
            'This field is required when active.')

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


class WorkerTestCase(BaseTestCase):

    def setUp(self):
        super(WorkerTestCase, self).setUp()

    def test_run(self):
        html = HTMLValidation(
            repo=self.repo,
            is_active=False,
            url_to_validate="http://www.example.com",
            deployment_delay="1"
        )
        html.save()

        status = IntegrationStatus(integration=html, commit=self.commit)
        status.save()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.waiting)

        html.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.failed)
        self.assertEqual(status.value, "Failed")
        self.assertRegex(status.details, "\d+ Errors, \d+ Warnings")

        html.url_to_validate = "https://validator.w3.org/"
        html.save()

        html.run(status)
        status.refresh_from_db()
        self.assertEqual(
            status.status, IntegrationStatus.STATUS_CHOICES.passed)
