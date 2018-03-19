from django.contrib.auth.models import User
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
    # could listen to hooks about repo owner changes
    # @todo they should be updated frequently
    # on commits? nightly? on user `refresh` actions? tbd...
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='repos')
    
    class Meta:
        index_together = ["name", "owner"]
        unique_together = (("name", "owner"),)
