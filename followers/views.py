from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from proj_api.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer


class FollowerList(generics.ListCreateAPIView):
    """
    List all followers, i.e. all instances of a user
    following another user.
    Create a follower, i.e. follow a user if logged in.
    perform_create: associate the current logged in user with a follower,
    ensuring a user cannot follow themselves.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        # Check if the user is trying to follow themselves
        if serializer.validated_data.get('followed') == self.request.user:
            raise ValidationError("You cannot follow yourself.")
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a follower
    No Update view, as we either follow or unfollow users
    Destroy a follower, i.e. unfollow someone if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
