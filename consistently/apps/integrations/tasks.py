from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

from django.core import serializers

from .models import IntegrationStatus


class NeedsToRetry(Exception):
    """
    When an integration's `run` method needs to wait longer, it can
    raise this exception.raise

    This works in conjunction with the kwargs from `get_task_kwargs`
    and retry_delay.
    """
    pass


def queue_integration_tasks(commit):
    """
    Starts all integration tasks for a commit
    """

    # create `IntegrationStatus` objects for each integration
    integrations = commit.repo.integration_set.filter(is_active=True)
    for integration in integrations:

        i = integration.type_instance

        data = serializers.serialize('json', [i, ])
        status = IntegrationStatus.objects.create(
            integration=i, commit=commit, with_settings=data)

        #  queue up worker for each IntegrationStatus
        countdown = i.get_task_delay()
        task_kwargs = i.get_task_kwargs()

        print("queuing task for %s" % i)
        print("with countdown=%d" % countdown)
        print("with kwargs=")
        print(task_kwargs)
        print("with settings")
        print(data)
        print('\n')

        task = run_integration.apply_async(
            args=(status.id,), kwargs=task_kwargs, countdown=countdown)

        # store the task id on the status object
        # but only update the task_id in case the
        # task has already modified the status
        status.task_id = task.id
        status.save(update_fields=["task_id"])


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
        print("restarting task for %s" % status)
        raise self.retry(
            exc=exc, max_retries=max_retries, countdown=countdown)
