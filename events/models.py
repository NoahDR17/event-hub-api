from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.utils import timezone

class Tag(models.Model):
    """
    A simple model for categorizing events.
    Each Tag can be associated with multiple Events.
    Each Event can be associated with multiple Tags.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    musicians = models.ManyToManyField(User, related_name="musician_events", blank=True)
    title = models.CharField(
        max_length=200,
        blank=False,
    )
    description = models.TextField(
        max_length=400,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_ohnagj'
    )
    location = models.CharField(
        max_length=255,
    )
    EVENT_TYPE_CHOICES = [
        ('ORCHESTRA', 'Orchestra'),
        ('FESTIVAL', 'Festival'),
        ('GIG', 'Gig'),
        ('PARTY', 'Party'),
        ('OTHER', 'Other'),
    ]
    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPE_CHOICES,
        default='OTHER'
    )
    event_date = models.DateTimeField(
        help_text="Date and time when the event will take place."
    )
    # A many-to-many relationship with Tag
    tags = models.ManyToManyField(
        Tag,
        related_name='events',
        blank=True,
        help_text="Categories or tags associated with this event."
    )

    def clean(self):
            super().clean()
            if self.event_date < timezone.now():
                raise ValidationError("Event date/time cannot be in the past.")
                
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """
        Returns a string with the event's title, date, and tags.
        Example output:
        "Tech Meetup (2025-01-09) [Tech, Workshop]"
        """
        # Convert the ManyToMany tags to a list of tag names
        tags_list = [tag.name for tag in self.tags.all()]
        # Join them into a comma-separated string
        tags_str = ', '.join(tags_list)

        return f"{self.title} ({self.event_date.strftime('%Y-%m-%d')}) [{tags_str}]"
