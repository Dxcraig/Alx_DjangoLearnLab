from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model.
    
    Extends Django's UserAdmin to include custom fields.
    """
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_followers_count', 'get_following_count']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('bio', 'profile_picture', 'following')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('bio', 'profile_picture')
        }),
    )
    
    filter_horizontal = ['following', 'groups', 'user_permissions']
    
    def get_followers_count(self, obj):
        """Display follower count in admin list."""
        return obj.get_followers_count()
    get_followers_count.short_description = 'Followers'
    
    def get_following_count(self, obj):
        """Display following count in admin list."""
        return obj.get_following_count()
    get_following_count.short_description = 'Following'


admin.site.register(CustomUser, CustomUserAdmin)
