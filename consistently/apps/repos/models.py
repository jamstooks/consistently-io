from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel
import os

from .utils import get_badge_name


class Repository(TimeStampedModel):
    """
    This represents a linked github repository.

    @todo - github_id to primary key
    @todo - index on prefix/name
    @todo - consider storing a github webhook secret
    """
    github_id = models.PositiveIntegerField(unique=True)
    hook_id = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    prefix = models.CharField(max_length=40)
    name = models.CharField(max_length=100)
    activated_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='repos', blank=True, null=True)
    latest_commit = models.ForeignKey(
        'Commit', blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def full_name(self):
        return "%s/%s" % (self.prefix, self.name)

    def __str__(self):
        return self.full_name

    @property
    def github_url(self):
        return "https://github.com/%s/" % self.full_name

    def get_badge_path(self):
        """
        Returns the badge filename for this repository
        """
        name = get_badge_name(None, None, 1)

        if self.latest_commit:
            counts = self.latest_commit.get_counts()
            name = get_badge_name(**counts)

        return os.path.join('img', 'badges', name)

    def init_integrations(self):
        """
        Creates integration objects for all available integration types
        """
        from consistently.apps.integrations.models import INTEGRATION_TYPES
        for Klass in INTEGRATION_TYPES.values():
            try:
                i = Klass.objects.get(repo=self)
            except Klass.DoesNotExist:
                Klass.objects.create(repo=self)

        return self.integration_set.all()

    def get_active_integrations(self):
        """
        finds all the active integrtaions for this repo

        returns an array of each integration's type instance
        """

        active_integrations = []

        for i in self.integration_set.filter(is_active=True):
            active_integrations.append(i.type_instance)

        return active_integrations


class Commit(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    sha = models.CharField(max_length=40, unique=True)
    message = models.TextField(blank=True, null=True)
    fail_count = models.PositiveIntegerField(blank=True, null=True)
    pass_count = models.PositiveIntegerField(blank=True, null=True)
    waiting_count = models.PositiveIntegerField(blank=True, null=True)
    github_timestamp = models.DateTimeField()

    def __str__(self):
        return "%s (%s)" % (self.short_sha, self.repo)

    @property
    def short_sha(self):
        return self.sha[:6]

    def github_url(self):
        return "%scommit/%s/" % (self.repo.github_url, self.sha)

    def get_counts(self, force_recalculate=False):
        """
        Calculates the count values based on `IntegrationStatus`
        objects tied to it.

        Recalculates and saves if the counts are None or there
        are waiting tasks.

        `recalculate` forces rewrite regardless.

        @todo - if a status is locked in `waiting` mode then this
        will be a performance draw. Maybe consider another way.
        """

        if force_recalculate or self.waiting_count or self.pass_count is None:

            fail_count = pass_count = waiting_count = 0
            for status in self.integrationstatus_set.all():
                if status.status == status.STATUS_CHOICES.failed:
                    fail_count += 1
                elif status.status == status.STATUS_CHOICES.passed:
                    pass_count += 1
                elif status.status == status.STATUS_CHOICES.waiting:
                    waiting_count += 1

            self.pass_count = pass_count
            self.fail_count = fail_count
            self.waiting_count = waiting_count
            self.save()

        return {
            'pass_count': self.pass_count,
            'fail_count': self.fail_count,
            'waiting_count': self.waiting_count
        }
