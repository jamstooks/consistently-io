from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel


class Repository(TimeStampedModel):
    """
    This represents a linked github repository.

    @todo - github_id to primary key
    @todo - should we store the latest commit on this model for performance?
    @todo - index on prefix/name
    """
    github_id = models.PositiveIntegerField(unique=True)
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


class Commit(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    sha = models.CharField(max_length=40)
    date = models.DateTimeField()

    def __str__(self):
        return self.sha[:6]
