from django.db import models
from model_utils.models import TimeStampedModel


class Repository(TimeStampedModel):
    """
    This represents a linked github repository.
    
    Design question: is it worth using a property like `is_connected`
    to retain details about a repository after it gets disconnected?
    ... or should disconnection remove the repo altogether?
    """
    github_id = models.PositiveIntegerField(unique=True)
    last_commit = models.DateTimeField(blank=True, null=True)
    last_commit_name = models.CharField(max_length=40, blank=True, null=True)
    
    # The name and username are stored for quick lookup
    # but changing a name or switching users shouldn't break the system
    # @todo they should be updated frequently
    # on commits? nightly? on user `refresh` actions? tbd...
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=64, unique=True)
    
    class Meta:
        index_together = ["name", "username"]
        unique_together = (("name", "username"),)
