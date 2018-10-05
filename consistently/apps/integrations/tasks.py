from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

from .models import IntegrationStatus


class NeedsToRetry(Exception):
    """
    When an integration's `run` method needs to wait longer, it can
    raise this exception.raise

    This works in conjunction with the kwargs from `get_task_kwargs`
    and retry_delay.
    """
    pass


@shared_task(bind=True)
def run_integration(self, id, max_retries=0, countdown=60):
    """
    Passes the status to the integration's `run` method

    Accepts an `IntegrationStatus` `id`

    @todo - handle max retries exceeded
    https://stackoverflow.com/questions/6499952/recover-from-task-failed-beyond-max-retries
    """

    status = IntegrationStatus.objects.get(pk=id)
    status.task_id = self.request.id  # useful for tasks that might retry
    status.save()
    integration = status.integration.type_instance

    print("starting %s task for repo: %s (%s)" % (
        integration.integration_type,
        status.commit.repo,
        status.commit))

    try:
        i = integration.run(status)
        return
    except NeedsToRetry as exc:
        raise self.retry(
            exc=exc, max_retries=max_retries, countdown=countdown)
