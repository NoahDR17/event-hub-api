from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from proj_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.annotate(
        events_count=Count('owner__event', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = [
        'role',
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]

    ordering_fields = [
        'events_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
        'role',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        events_count=Count('owner__event', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
