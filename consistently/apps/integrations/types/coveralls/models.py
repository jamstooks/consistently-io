from django.db import models

from ...models import Integration
from .utils import get_status

# https://docs.coveralls.io/api-introduction


class Coveralls(Integration):
    """
    Coveralls.io
    """
    build_time = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Coveralls'

    @property
    def description(self):
        return "**Coveralls** - Coverage provided by [coveralls.io](https://coveralls.io/)"

    @property
    def notes(self):
        return """
Build Time is an *optional* rough estimate of how many seconds it takes
to run your tests and send coverage details to coveralls. We will retry, but
if your build time is consistently over 5 minutes, we recommend setting
this to avoid timeouts."""

    def get_serializer_class(self):
        from .serializer import CoverallsSerializer
        return CoverallsSerializer

    def get_task_delay(self):
        """
        How long to wait before starting task initially

        defaults to 2 minutes, but sets a minimum of 16 seconds
        """
        start = self.build_time if self.build_time != None else 120
        if start < 16:
            start = 16
        return start

    def get_task_kwargs(self):
        """
        This just mimics Travis + 30 seconds for now
        """
        start = self.get_task_delay() + 30
        delay = start / 4.0 if start else 0

        return {'max_retries': 10, 'countdown': delay}

    def run(self, status):
        get_status(status)
