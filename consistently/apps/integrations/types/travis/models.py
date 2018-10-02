from django.db import models

from ...models import Integration
from .utils import get_status

# https://docs.travis-ci.com/user/developer/


class Travis(Integration):
    """
    This integration doesn't actually require any settings for open source

    when we add private repos, we'll need some auth tools here
    """

    class Meta:
        verbose_name = 'TravisCI'

    @property
    def description(self):
        return "**Travis** - CI provided by [travis-ci.org](https://travis-ci.org/)"

    @property
    def link(self):
        return "https://travis-ci.org/"

    def run(self, status):
        """
        Receives the IntegrationStatus when triggered by the worker
        """
        get_status(status)
