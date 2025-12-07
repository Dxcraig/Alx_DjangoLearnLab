from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Blog Post model.
    
    Represents a blog post with title, content, publication date, and author.
    Each post is associated with a user (author) who can have multiple posts.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title
