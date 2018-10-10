from django.db import models

from ...models import Integration
from .utils import get_validation_status

# https://validator.w3.org/docs/api.html


class HTMLValidation(Integration):
    """
    Custom settings for the HTMLValidation Integration
    """
    url_to_validate = models.URLField(blank=True, null=True)
    deployment_delay = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="How many seconds to wait after push before validation.")

    class Meta:
        verbose_name = 'HTML Validation'

    @property
    def description(self):
        return "**HTML Validation** - service provided by [W3.org](https://validator.w3.org/)"

    @property
    def notes(self):
        return "Currently we only support one URL per repo."

    def get_serializer_class(self):
        from .serializer import HTMLValidationSerializer
        return HTMLValidationSerializer

    def run(self, integration_status):
        """
        Receives the IntegrationStatus when triggered by the worker
        """
        return get_validation_status(integration_status)

    def get_task_delay(self):

        return self.deployment_delay * 1.5
