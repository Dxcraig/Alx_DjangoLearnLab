from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Post(models.Model):
    """
    Blog Post model.
    
    Represents a blog post with title, content, publication date, and author.
    Each post is associated with a user (author) who can have multiple posts.
    Posts can be tagged using django-taggit for categorization.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager()  # Tagging functionality using django-taggit
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Comment model for blog posts.
    
    Represents a comment on a blog post with content, author, and timestamps.
    Each comment is associated with a post and a user (author).
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text='The blog post this comment belongs to'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text='The user who wrote this comment'
    )
    content = models.TextField(
        help_text='The comment text content'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='The date and time when the comment was created'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='The date and time when the comment was last updated'
    )
    
    class Meta:
        ordering = ['created_at']  # Show oldest comments first
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
