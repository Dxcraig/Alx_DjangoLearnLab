from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Notification(models.Model):
    """
    Notification model for tracking user interactions and events.
    
    Uses GenericForeignKey to allow notifications for any model (posts, comments, likes, follows).
    
    Fields:
    - recipient: The user receiving the notification
    - actor: The user who performed the action
    - verb: Description of the action (e.g., "liked your post", "followed you")
    - target_content_type: Content type of the target object
    - target_object_id: ID of the target object
    - target: Generic foreign key to the target object
    - timestamp: When the notification was created
    - read: Whether the notification has been read
    """
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User receiving the notification"
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actions',
        help_text="User who performed the action"
    )
    verb = models.CharField(
        max_length=255,
        help_text="Description of the action"
    )
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Content type of the target object"
    )
    target_object_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="ID of the target object"
    )
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="When the notification was created"
    )
    read = models.BooleanField(
        default=False,
        help_text="Whether the notification has been read"
    )
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['recipient', '-timestamp']),
            models.Index(fields=['recipient', 'read']),
        ]
    
    def __str__(self):
        return f"{self.actor.username} {self.verb} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark this notification as read."""
        if not self.read:
            self.read = True
            self.save()
