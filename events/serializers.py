from rest_framework import serializers
from .models import Event, Tag
from likes.models import Like
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    """
    A serializer for the Tag model.
    Handles the creation and listing of tags.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']

class MusicianSerializer(serializers.ModelSerializer):
    """
    Serializer to display musician details.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'profile']

class EventSerializer(serializers.ModelSerializer):
    """
    Handles validation and assignment of the musician field.
    Automatically sets the owner to the request.user.
    """
    musicians = MusicianSerializer(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False
    )

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError('Image height larger than 4096px!')
        if value.image.width > 4096:
            raise serializers.ValidationError('Image width larger than 4096px!')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, event=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Event
        fields = [
            'id',
            'owner',
            'title',
            'description',
            'created_at',
            'updated_at',
            'image',
            'location',
            'event_type',
            'event_date',
            'tags',
            'is_owner',
            'profile_id',
            'profile_image',
            'like_id',
            'likes_count',
            'comments_count',
            'musicians',
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']
