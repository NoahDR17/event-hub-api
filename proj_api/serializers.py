from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from rest_auth.models import TokenModel
import sys  

class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')
    role = serializers.ChoiceField(
        choices=[
            ('basic', 'Basic User'),
            ('organiser', 'Event Organiser'),
            ('musician', 'Musician/Band'),
        ]
    )
    genres = serializers.CharField(allow_blank=True, required=False)
    instruments = serializers.CharField(allow_blank=True, required=False)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image', 'role',
            'genres', 'instruments',
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        role = profile_data.get('role', instance.profile.role)
        genres = profile_data.get('genres', instance.profile.genres)
        instruments = profile_data.get('instruments', instance.profile.instruments)

        # Update the profile fields
        profile = instance.profile
        profile.role = role
        profile.genres = genres
        profile.instruments = instruments
        profile.save()

        return super().update(instance, validated_data)

class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = UserDetailsSerializer(many=False, read_only=True) 
    sys.stdout.flush()

    class Meta:
        model = TokenModel
        fields = ('key', 'user')