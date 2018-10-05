from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel


class Repository(TimeStampedModel):
    """
    This represents a linked github repository.

    @todo - github_id to primary key
    @todo - should we store the latest commit on this model for performance?
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


class Commit(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    sha = models.CharField(max_length=40, unique=True)
    message = models.TextField(blank=True, null=True)
    fail_count = models.PositiveIntegerField(blank=True, null=True)
    pass_count = models.PositiveIntegerField(blank=True, null=True)
    waiting_count = models.PositiveIntegerField(blank=True, null=True)
    github_timestamp = models.DateTimeField()

    def __str__(self):
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
