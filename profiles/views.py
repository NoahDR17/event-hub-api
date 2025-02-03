from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from proj_api.permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .models import Profile
from events.models import Event
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
    Deletes all events owned by the user if their role changes from 'organiser'.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        events_count=Count('owner__event', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer

    def get_serializer_class(self):
        # For edit/update requests, check the role in the incoming data.
        if self.request.method == 'PUT':
            if self.request.data.get('role') == 'musician':
                return ProfileSerializer
            else:
                # Otherwise, use a serializer without musician-specific fields.
                class NonMusicianProfileSerializer(ProfileSerializer):
                    class Meta(ProfileSerializer.Meta):
                        fields = [
                            field for field in ProfileSerializer.Meta.fields
                            if field not in ['genres', 'instruments']
                        ]
                return NonMusicianProfileSerializer

        # For GET requests, use the current profile role to determine which serializer to use.
        profile = self.get_object()
        if profile.role != 'musician':
            class NonMusicianProfileSerializer(ProfileSerializer):
                class Meta(ProfileSerializer.Meta):
                    fields = [
                        field for field in ProfileSerializer.Meta.fields
                        if field not in ['genres', 'instruments']
                    ]
            return NonMusicianProfileSerializer
        return ProfileSerializer


    def perform_update(self, serializer):
        """
        Override to check if the user's role has changed and handle event deletion.
        """
        user_profile = self.get_object()
        previous_role = user_profile.role
        new_role = serializer.validated_data.get('role', previous_role)
        serializer.save()
