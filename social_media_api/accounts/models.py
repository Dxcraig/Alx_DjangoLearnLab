from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Additional fields:
    - bio: User's biography or description
    - profile_picture: URL or path to user's profile picture
    - followers: Many-to-many relationship with other users (asymmetric)
    """
    bio = models.TextField(max_length=500, blank=True, null=True, help_text="User biography")
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text="User profile picture"
    )
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
        help_text="Users who follow this user"
    )
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
    
    def get_followers_count(self):
        """Return the number of followers."""
        return self.followers.count()
    
    def get_following_count(self):
        """Return the number of users this user follows."""
        return self.following.count()
