from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from rest_auth.models import TokenModel
import sys  

class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image'
        )

class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = UserDetailsSerializer(many=False, read_only=True) 
    sys.stdout.flush()

    class Meta:
        model = TokenModel
        fields = ('key', 'user')