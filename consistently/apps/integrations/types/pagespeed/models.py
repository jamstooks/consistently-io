from django.db import models

from ...models import Integration
from .utils import get_pagespeed_score


class PageSpeed(Integration):
    """
    Custom settings for the GooglePageSpeed Integrations
    """
    url = models.URLField(blank=True, null=True)
    deployment_delay = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="How long before the app is live?")

    class Meta:
        verbose_name = 'Google PageSpeed Insights'

    @property
    def description(self):
        return "**PageSpeed Insights** - service provided by [Google](https://developers.google.com/speed/pagespeed/insights/)"

    def get_serializer_class(self):
        from .serializer import PageSpeedSerializer
        return PageSpeedSerializer

    def run(self, integration_status):
        """
        Receives the IntegrationStatus when triggered by the worker
        """
        return get_pagespeed_score(integration_status)

    def get_task_delay(self):
        return self.deployment_delay * 1.33
