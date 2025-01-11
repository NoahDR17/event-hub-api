from rest_framework import serializers
from .models import Event, Tag

class TagSerializer(serializers.ModelSerializer):
    """
    A serializer for the Tag model.
    Handles the creation and listing of tags.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']


class EventSerializer(serializers.ModelSerializer):
    """
    A serializer for the Event model.
    Shows how tags can be listed and updated by their primary keys.
    Automatically sets the owner to the request.user (using perform_create in the view).
    """   
    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False
    )

    class Meta:
        model = Event
        fields = [
            'id', 'owner', 'title', 'description', 
            'created_at', 'updated_at', 'image', 'location',
            'event_type', 'event_date', 'tags'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']

    # Validate event_date is not in the past (currently got logic in the models.py to handle it)
    # def validate_event_date(self, value):
    #     from django.utils import timezone
    #     if value < timezone.now():
    #         raise serializers.ValidationError(
    #             "Event date/time cannot be in the past."
    #         )
    #     return value
