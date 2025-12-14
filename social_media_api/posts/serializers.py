from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying author information.
    """
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    
    Handles creating, reading, updating, and deleting comments.
    """
    author = AuthorSerializer(read_only=True)
    author_id = serializers.IntegerField(read_only=True)
    post_id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_id', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 'updated_at', 'post_id']
    
    def validate_content(self, value):
        """Validate comment content."""
        if not value or not value.strip():
            raise serializers.ValidationError("Comment content cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Comment must be at least 3 characters long.")
        if len(value) > 1000:
            raise serializers.ValidationError("Comment cannot exceed 1000 characters.")
        return value.strip()


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    
    Handles creating, reading, updating, and deleting posts.
    Includes nested comments and author information.
    """
    author = AuthorSerializer(read_only=True)
    author_id = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_id', 'title', 'content',
            'created_at', 'updated_at', 'comments', 'comments_count',
            'likes_count', 'is_liked_by_user'
        ]
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        """Return the number of comments on this post."""
        return obj.get_comments_count()
    
    def get_likes_count(self, obj):
        """Return the number of likes on this post."""
        return obj.get_likes_count()
    
    def get_is_liked_by_user(self, obj):
        """Check if the current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def validate_title(self, value):
        """Validate post title."""
        if not value or not value.strip():
            raise serializers.ValidationError("Post title cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        if len(value) > 255:
            raise serializers.ValidationError("Title cannot exceed 255 characters.")
        return value.strip()
    
    def validate_content(self, value):
        """Validate post content."""
        if not value or not value.strip():
            raise serializers.ValidationError("Post content cannot be empty.")
        if len(value) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long.")
        return value.strip()


class PostListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing posts (without nested comments).
    """
    author = AuthorSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 
                  'comments_count', 'likes_count', 'is_liked_by_user']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        """Return the number of comments on this post."""
        return obj.get_comments_count()
    
    def get_likes_count(self, obj):
        """Return the number of likes on this post."""
        return obj.get_likes_count()
    
    def get_is_liked_by_user(self, obj):
        """Check if the current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating comments.
    """
    class Meta:
        model = Comment
        fields = ['post', 'content']
    
    def validate_content(self, value):
        """Validate comment content."""
        if not value or not value.strip():
            raise serializers.ValidationError("Comment content cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Comment must be at least 3 characters long.")
        if len(value) > 1000:
            raise serializers.ValidationError("Comment cannot exceed 1000 characters.")
        return value.strip()


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Like model.
    
    Handles displaying like information.
    """
    user = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
