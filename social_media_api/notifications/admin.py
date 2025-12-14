from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for Notification model.
    """
    list_display = ['id', 'recipient', 'actor', 'verb', 'target_type', 
                    'timestamp', 'read']
    list_filter = ['read', 'timestamp', 'verb']
    search_fields = ['recipient__username', 'actor__username', 'verb']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    
    def target_type(self, obj):
        """Display target type in admin list."""
        if obj.target_content_type:
            return obj.target_content_type.model
        return None
    target_type.short_description = 'Target Type'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read."""
        updated = queryset.update(read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread."""
        updated = queryset.update(read=False)
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = 'Mark selected as unread'
