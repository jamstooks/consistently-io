from django.db import models
from django.urls import reverse

from model_utils.models import TimeStampedModel
from model_utils import Choices
from logging import getLogger
from collections import OrderedDict

from consistently.apps.repos.models import Repository, Commit


logger = getLogger(__name__)


class Integration(TimeStampedModel):
    """
    The base Integration model.
    """

    integration_type = models.CharField(max_length=40)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.repo, self.integration_type)

    def save(self, *args, **kwargs):

        if not self.integration_type:
            key_list = list(INTEGRATION_TYPES.keys())
            value_list = list(INTEGRATION_TYPES.values())
            self.integration_type = key_list[value_list.index(self.__class__)]

        return super(Integration, self).save(*args, **kwargs)

    def has_settings(self):
        """
        Some integrations my not have additional properties. If that's the
        case, then this can return False.

        @note - This isn't used yet, but might be for one-click activation.

        @todo - implmenent
        """
        raise NotImplementedError

    """
        Methods to override
    """

    @property
    def description(self):
        "short description, can include markdown"
        raise NotImplementedError

    @property
    def notes(self):
        raise NotImplementedError

    def get_serializer_class(self):
        from consistently.apps.api.serializers import BasicIntegrationSerializer
        return BasicIntegrationSerializer

    def run(self, commit):
        raise NotImplementedError

    def get_task_delay(self):
        """
        How long to wait before starting task initially
        """
        return 60

    def get_task_kwargs(self):
        """
        These are the kwargs supplied to the celery task itself
        that is, `integrations.tasks.run_integration`
        """
        return {}

    @property
    def type_instance(self):
        return getattr(
            self,
            INTEGRATION_TYPES[self.integration_type].__name__.lower())


class IntegrationStatus(TimeStampedModel):
    """

    @todo - document this
    @todo - unique together for integration and commit
    """

    STATUS_CHOICES = Choices(
        ('waiting', 'Waiting...'),
        ('passed', 'Passed'),
        ('failed', 'Failed')
    )

    integration = models.ForeignKey(
        Integration, on_delete=models.CASCADE)
    commit = models.ForeignKey(
        Commit, on_delete=models.CASCADE)
    task_id = models.CharField(
        max_length=50, unique=True, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.waiting)
    with_settings = models.TextField(
        blank=True, null=True,
        help_text="Archives the settings used to evaluate the integration")
    value = models.CharField(max_length=64, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s (%s)[%s]" % (
            self._meta.verbose_name.title(),
            self.commit,
            self.status)


"""
    Imported down here to avoid recursive imports
"""
from .types.html.models import HTMLValidation
from .types.travis.models import Travis

INTEGRATION_TYPES = OrderedDict()
INTEGRATION_TYPES['html'] = HTMLValidation
INTEGRATION_TYPES['travis'] = Travis
