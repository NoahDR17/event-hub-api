from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Event
from .serializers import EventSerializer
from proj_api.permissions import IsOwnerOrReadOnly

class EventList(generics.ListCreateAPIView):
    """
    List events or create an event if logged in.
    The perform_create method associates the event with the logged-in user.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Event.objects.all().order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__username',
        'tags__name',
        'event_type',
        'location',
    ]
    search_fields = [
        'owner__username',
        'title',
        'description',
        'tags__name',
        'location',
    ]
    ordering_fields = [
        'created_at',
        'event_date',
    ]

    def perform_create(self, serializer):
        """
        Automatically set the event owner to the logged-in user.
        """
        serializer.save(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve an event or edit/delete it if you own it.
    """
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Event.objects.all().order_by('-created_at')
