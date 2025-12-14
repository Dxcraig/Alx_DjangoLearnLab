from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """
    Post model for social media content.
    
    Fields:
    - author: The user who created the post
    - title: Post title
    - content: Post content/body
    - created_at: Timestamp when post was created
    - updated_at: Timestamp when post was last updated
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="User who created this post"
    )
    title = models.CharField(
        max_length=255,
        help_text="Title of the post"
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when post was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when post was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def get_comments_count(self):
        """Return the number of comments on this post."""
        return self.comments.count()


class Comment(models.Model):
    """
    Comment model for post interactions.
    
    Fields:
    - post: The post being commented on
    - author: The user who created the comment
    - content: Comment content
    - created_at: Timestamp when comment was created
    - updated_at: Timestamp when comment was last updated
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Post being commented on"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="User who created this comment"
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when comment was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when comment was last updated"
    )
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
