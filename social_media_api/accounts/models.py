from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Additional fields:
    - bio: User's biography or description
    - profile_picture: URL or path to user's profile picture
    - following: Many-to-many relationship representing users that this user follows
    """
    bio = models.TextField(max_length=500, blank=True, null=True, help_text="User biography")
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text="User profile picture"
    )
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
        help_text="Users that this user follows"
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
