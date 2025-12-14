from django.urls import path
from .views import (
    NotificationListView,
    UnreadNotificationListView,
    mark_notification_as_read,
    mark_all_notifications_as_read
)

app_name = 'notifications'

urlpatterns = [
    # List all notifications
    path('', NotificationListView.as_view(), name='notification-list'),
    
    # List unread notifications
    path('unread/', UnreadNotificationListView.as_view(), name='unread-notifications'),
    
    # Mark specific notification as read
    path('<int:notification_id>/read/', mark_notification_as_read, name='mark-as-read'),
    
    # Mark all notifications as read
    path('read-all/', mark_all_notifications_as_read, name='mark-all-as-read'),
]
