from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class ActorSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying actor (user who performed action) information.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']
        read_only_fields = ['id', 'username', 'profile_picture']


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    
    Handles displaying notification information with actor details.
    """
    actor = ActorSerializer(read_only=True)
    target_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'verb', 'target_type',
            'target_object_id', 'timestamp', 'read'
        ]
        read_only_fields = ['id', 'recipient', 'actor', 'verb', 'target_type', 
                            'target_object_id', 'timestamp']
    
    def get_target_type(self, obj):
        """Return the type of the target object."""
        if obj.target_content_type:
            return obj.target_content_type.model
        return None
