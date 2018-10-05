"""
Testing base integrations and tasks

Individual integrations need their own tests

Note: CELERY_TASK_ALWAYS_EAGER should be True in settings
for tests to pass, but we're overriding it here just to be sure
"""

from django.test import override_settings
from unittest import mock

from .base import BaseTestCase
from consistently.apps.integrations.models import IntegrationStatus
from consistently.apps.integrations.tasks import run_integration, NeedsToRetry
from consistently.apps.integrations.types.html.models import HTMLValidation

RUN_METHOD = 'consistently.apps.integrations.types.html.models.HTMLValidation.run'


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
# @override_settings(CELERY_TASK_EAGER_PROPAGATES=True)
class RepoListTestCase(BaseTestCase):

    def setUp(self):
        super(RepoListTestCase, self).setUp()

        # add an active HTMLIntegration for the current repo
        self.html = HTMLValidation.objects.create(
            repo=self.repo,
            url_to_validate="http://www.aashe.org",
            deployment_delay=1,
            is_active=True)
        self.status = IntegrationStatus.objects.create(
            commit=self.commit, integration=self.html)

    @mock.patch(RUN_METHOD)
    def test_basic_execution(self, fake_run):
        """
        Just basic task execution
        """
        kwargs = {}
        task = run_integration.apply_async((self.status.id,), **kwargs)
        self.assertEqual(fake_run.call_count, 1)

    @mock.patch(RUN_METHOD, side_effect=NeedsToRetry())
    def test_retry_execution(self, fake_run):
        """
        Just basic task execution
        """
        kwargs = {'max_retries': 5, 'countdown': 0.2}
        self.assertEqual(fake_run.call_count, 0)
        task = run_integration.apply_async(
            args=(self.status.id,), kwargs=kwargs)
        self.assertEqual(fake_run.call_count, 6)
