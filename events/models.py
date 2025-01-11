from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    """
    A simple model for categorizing events.
    Each Tag can be associated with multiple Events.
    Each Event can be associated with multiple Tags.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
