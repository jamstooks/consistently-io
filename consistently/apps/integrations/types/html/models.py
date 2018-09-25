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
        return "service provided by [W3.org](https://validator.w3.org/)"

    @property
    def link(self):
        return "https://validator.w3.org/"

    def get_serializer_class(self):
        from .serializer import HTMLValidationSerializer
        return HTMLValidationSerializer

    def run(self, status):
        """
        Receives the IntegrationStatus when triggered by the worker
        """
        get_validation_status(status)
