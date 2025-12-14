from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from .serializers import (
    PostSerializer,
    PostListSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    LikeSerializer
)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing posts.
    
    Provides CRUD operations for posts with the following features:
    - List all posts (GET /api/posts/)
    - Create a new post (POST /api/posts/)
    - Retrieve a specific post (GET /api/posts/{id}/)
    - Update a post (PUT/PATCH /api/posts/{id}/)
    - Delete a post (DELETE /api/posts/{id}/)
    - Search and filter posts by title or content
    - Pagination support
    
    Permissions:
    - Authenticated users can create posts
    - Only authors can update or delete their own posts
    - Anyone can view posts
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        Use different serializers for list and detail views.
        """
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        """
        Set the post author to the current user when creating a post.
        """
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        """
        Optionally filter posts by search query.
        """
        queryset = Post.objects.all()
        
        # Filter by search query parameter
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )
        
        # Filter by author
        author_id = self.request.query_params.get('author', None)
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_posts(self, request):
        """
        Retrieve posts created by the current user.
        GET /api/posts/my_posts/
        """
        posts = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(posts)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        Like a post.
        POST /api/posts/{id}/like/
        """
        # Get the post using generics.get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)
        
        # Use get_or_create to handle like creation
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            return Response({
                'error': 'You have already liked this post'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create notification for post author (if not liking own post)
        if post.author != request.user:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id
            )
        
        return Response({
            'message': 'Post liked successfully',
            'likes_count': post.get_likes_count()
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        """
        Unlike a post.
        POST /api/posts/{id}/unlike/
        """
        # Get the post using generics.get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)
        
        # Check if user has liked the post
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            
            return Response({
                'message': 'Post unliked successfully',
                'likes_count': post.get_likes_count()
            }, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({
                'error': 'You have not liked this post'
            }, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments.
    
    Provides CRUD operations for comments with the following features:
    - List all comments (GET /api/comments/)
    - Create a new comment (POST /api/comments/)
    - Retrieve a specific comment (GET /api/comments/{id}/)
    - Update a comment (PUT/PATCH /api/comments/{id}/)
    - Delete a comment (DELETE /api/comments/{id}/)
    - Filter comments by post
    
    Permissions:
    - Authenticated users can create comments
    - Only authors can update or delete their own comments
    - Anyone can view comments
    """
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    
    def get_serializer_class(self):
        """
        Use different serializers for create and other actions.
        """
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        """
        Set the comment author to the current user when creating a comment.
        Create notification for post author.
        """
        comment = serializer.save(author=self.request.user)
        
        # Create notification for post author (if not commenting on own post)
        if comment.post.author != self.request.user:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on your post',
                target_content_type=ContentType.objects.get_for_model(comment.post),
                target_object_id=comment.post.id
            )
    
    def get_queryset(self):
        """
        Optionally filter comments by post.
        """
        queryset = Comment.objects.all()
        
        # Filter by post ID
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        
        # Filter by author
        author_id = self.request.query_params.get('author', None)
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_comments(self, request):
        """
        Retrieve comments created by the current user.
        GET /api/comments/my_comments/
        """
        comments = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(comments)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)


class FeedView(generics.ListAPIView):
    """
    API endpoint for viewing the user's personalized feed.
    
    GET /api/posts/feed/
    
    Returns posts from users that the authenticated user follows,
    ordered by creation date (most recent first).
    
    Features:
    - Paginated results
    - Only shows posts from followed users
    - Ordered by most recent first
    
    Response:
    [
        {
            "id": int,
            "author": {
                "id": int,
                "username": "string"
            },
            "title": "string",
            "content": "string",
            "created_at": "datetime",
            "updated_at": "datetime",
            "comments_count": int
        }
    ]
    """
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return posts from users that the current user follows.
        """
        # Get the list of users that the current user follows
        following_users = self.request.user.following.all()
        
        # Return posts from those users, ordered by creation date
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
