from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post model.
    """
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Comment model.
    """
    list_display = ('author', 'post', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
