from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    API endpoint for viewing user notifications.
    
    GET /api/notifications/
    
    Returns all notifications for the authenticated user,
    ordered by timestamp (most recent first).
    Unread notifications are shown first.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return notifications for the current user.
        Unread notifications first, then by timestamp.
        """
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('read', '-timestamp')


class UnreadNotificationListView(generics.ListAPIView):
    """
    API endpoint for viewing unread notifications.
    
    GET /api/notifications/unread/
    
    Returns only unread notifications for the authenticated user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only unread notifications for the current user."""
        return Notification.objects.filter(
            recipient=self.request.user,
            read=False
        ).order_by('-timestamp')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_as_read(request, notification_id):
    """
    Mark a specific notification as read.
    
    POST /api/notifications/{notification_id}/read/
    """
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.mark_as_read()
        
        return Response({
            'message': 'Notification marked as read'
        }, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({
            'error': 'Notification not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_as_read(request):
    """
    Mark all notifications as read for the authenticated user.
    
    POST /api/notifications/read-all/
    """
    notifications = Notification.objects.filter(
        recipient=request.user,
        read=False
    )
    count = notifications.update(read=True)
    
    return Response({
        'message': f'{count} notifications marked as read'
    }, status=status.HTTP_200_OK)
