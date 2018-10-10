from django.db import models

from ...models import Integration
from .utils import get_status

# https://docs.travis-ci.com/user/developer/


class Travis(Integration):
    """
    This integration doesn't actually require any settings for open source

    when we add private repos, we'll need some auth tools here
    """
    build_time = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'TravisCI'

    @property
    def description(self):
        return "**Travis** - CI provided by [travis-ci.org](https://travis-ci.org/)"

    @property
    def notes(self):
        return """
Build Time is an *optional* rough estimate of how many seconds it takes
to run your tests. We will retry, but
if your build time is consistently over 5 minutes, we recommend setting
this to avoid timeouts."""

    def get_serializer_class(self):
        from .serializer import TravisSerializer
        return TravisSerializer

    def get_task_delay(self):
        """
        How long to wait before starting task initially
        """
        start = self.build_time if self.build_time != None else 120
        if start < 16:
            start = 16
        return start

    def get_task_kwargs(self):
        """
        Travis builds can take time, so we need to allow for retries.

        If a user doesn't provide the estimated `build_time`, we'll start
        with two minutes and go up in increments of 25% of that each time
        up to 10 minutes.

        This also enforces a minimum delay of 4 seconds

        @todo - consider an upper limit on this
        """
        start = self.get_task_delay()
        delay = start / 4.0 if start else 0

        return {'max_retries': 10, 'countdown': delay}

    def run(self, status):
        """
        Receives the IntegrationStatus when triggered by the worker
        """
        get_status(status)
