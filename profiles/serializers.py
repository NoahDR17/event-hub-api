from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Profile
from followers.models import Follower
from events.serializers import EventSerializer

class CustomRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(
        choices=[
            ('basic', 'Basic User'),
            ('organiser', 'Event Organiser'),
            ('musician', 'Musician/Band'),
        ],
        default='basic',
    )

    def get_cleaned_data(self):
        """
        Extend the cleaned_data to include the role field.
        """
        cleaned_data = super().get_cleaned_data()
        cleaned_data['role'] = self.validated_data.get('role', 'basic')
        return cleaned_data

    def save(self, request):
        """
        Override the save method to handle the role field
        and set it on the Profile during registration.
        """
        user = super().save(request)
        role = self.validated_data.get('role', 'basic')

        Profile.objects.filter(owner=user).update(role=role)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    events_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    upcoming_events = EventSerializer(many=True, read_only=True)
    past_events = EventSerializer(many=True, read_only=True)

    role = serializers.ChoiceField(
        choices=[
            ('basic', 'Basic User'),
            ('organiser', 'Event Organiser'),
            ('musician', 'Musician/Band'),
        ],
        default='basic'
    )

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.role == 'basic':
            # Remove fields not for basic users
            representation.pop('upcoming_events', None)
            representation.pop('past_events', None)
            representation.pop('genres', None)
            representation.pop('instruments', None)
            representation.pop('events_count', None)
        elif instance.role == 'organiser':
            # Remove fields not for organisers
            representation.pop('genres', None)
            representation.pop('instruments', None)
        return representation

    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'name',
            'content',
            'image',
            'is_owner',
            'following_id',
            'events_count',
            'followers_count',
            'following_count',
            'role',
            'genres',
            'instruments',
            'upcoming_events',
            'past_events',
        ]
