from django.db import models
from events.models import Event
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.timezone import now

ROLE_CHOICES = [
    ('basic', 'Basic User'),
    ('organiser', 'Event Organiser'),
    ('musician', 'Musician/Band'),
]

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_wl0tew'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='basic'
    )
    # Musician Specific Fields:
    genres = models.TextField(blank=True, null=True)
    instruments = models.TextField(blank=True, null=True) 
    # Organiser Specific Fields 

    # Combined Musician + Organiser past and upcoming events
    @property
    def upcoming_events(self):
        """
        Get upcoming events based on the user's role.
        """
        if self.role == 'musician':
            # Events where the user is included as a musician
            return Event.objects.filter(
                musicians=self.owner, event_date__gte=now()
            ).order_by('event_date')
        elif self.role == 'organiser':
            # Events where the user is the organiser
            return Event.objects.filter(
                owner=self.owner, event_date__gte=now()
            ).order_by('event_date')
        return Event.objects.none()

    @property
    def past_events(self):
        """
        Get past events based on the user's role.
        """
        if self.role == 'musician':
            # Events where the user is included as a musician
            return Event.objects.filter(
                musicians=self.owner, event_date__lt=now()
            ).order_by('-event_date')
        elif self.role == 'organiser':
            # Events where the user is the organiser
            return Event.objects.filter(
                owner=self.owner, event_date__lt=now()
            ).order_by('-event_date')
        return Event.objects.none()

    

    @property
    def upcoming_events(self):
        """
        Get upcoming events where this organiser is the owner.
        """
        if self.role == 'organiser':
            return Event.objects.filter(
                owner=self.owner, event_date__gte=now()
            ).order_by('event_date')
        return Event.objects.none()

    @property
    def past_events(self):
        """
        Get past events where this organiser is the owner.
        """
        if self.role == 'organiser':
            return Event.objects.filter(
                owner=self.owner, event_date__lt=now()
            ).order_by('-event_date')
        return Event.objects.none()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)