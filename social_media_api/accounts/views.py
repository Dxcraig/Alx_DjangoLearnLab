from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    UserFollowSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    
    POST /api/accounts/register/
    
    Request body:
    {
        "username": "string",
        "email": "string",
        "password": "string",
        "password_confirm": "string",
        "bio": "string (optional)",
        "profile_picture": "file (optional)"
    }
    
    Response:
    {
        "id": int,
        "username": "string",
        "email": "string",
        "bio": "string",
        "profile_picture": "url",
        "token": "string"
    }
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Get or create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    API endpoint for user login.
    
    POST /api/accounts/login/
    
    Request body:
    {
        "username": "string",
        "password": "string"
    }
    
    Response:
    {
        "token": "string",
        "user_id": int,
        "username": "string",
        "email": "string",
        "message": "string"
    }
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Get or create token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating user profile.
    
    GET /api/accounts/profile/
    Returns the authenticated user's profile information.
    
    PUT/PATCH /api/accounts/profile/
    Updates the authenticated user's profile (bio, profile_picture).
    
    Request body (for update):
    {
        "bio": "string (optional)",
        "profile_picture": "file (optional)"
    }
    
    Response:
    {
        "id": int,
        "username": "string",
        "email": "string",
        "bio": "string",
        "profile_picture": "url",
        "followers_count": int,
        "following_count": int,
        "date_joined": "datetime"
    }
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Return the authenticated user."""
        return self.request.user
    
    def get_serializer_class(self):
        """Use different serializers for GET and PUT/PATCH."""
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserProfileSerializer


class UserLogoutView(APIView):
    """
    API endpoint for user logout.
    
    POST /api/accounts/logout/
    
    Deletes the user's authentication token.
    
    Response:
    {
        "message": "Logged out successfully"
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            # Delete the user's token
            request.user.auth_token.delete()
            return Response({
                'message': 'Logged out successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Something went wrong'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FollowUserView(generics.GenericAPIView):
    """
    API endpoint for following a user.
    
    POST /api/accounts/follow/<int:user_id>/
    
    Allows authenticated users to follow another user.
    Users cannot follow themselves.
    
    Response:
    {
        "message": "You are now following {username}",
        "user": {
            "id": int,
            "username": "string",
            "bio": "string",
            "profile_picture": "url"
        }
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserFollowSerializer
    queryset = User.objects.all()
    
    def post(self, request, user_id):
        # Get the user to follow from all users
        user_to_follow = get_object_or_404(self.queryset, id=user_id)
        
        # Check if trying to follow themselves
        if user_to_follow == request.user:
            return Response({
                'error': 'You cannot follow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already following
        if request.user.following.filter(id=user_id).exists():
            return Response({
                'error': f'You are already following {user_to_follow.username}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Add to following
        request.user.following.add(user_to_follow)
        
        serializer = self.get_serializer(user_to_follow)
        return Response({
            'message': f'You are now following {user_to_follow.username}',
            'user': serializer.data
        }, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    """
    API endpoint for unfollowing a user.
    
    POST /api/accounts/unfollow/<int:user_id>/
    
    Allows authenticated users to unfollow another user.
    
    Response:
    {
        "message": "You have unfollowed {username}"
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    
    def post(self, request, user_id):
        # Get the user to unfollow from all users
        user_to_unfollow = get_object_or_404(self.queryset, id=user_id)
        
        # Check if actually following this user
        if not request.user.following.filter(id=user_id).exists():
            return Response({
                'error': f'You are not following {user_to_unfollow.username}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove from following
        request.user.following.remove(user_to_unfollow)
        
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}'
        }, status=status.HTTP_200_OK)


class FollowingListView(generics.ListAPIView):
    """
    API endpoint to list users that the authenticated user follows.
    
    GET /api/accounts/following/
    
    Response:
    [
        {
            "id": int,
            "username": "string",
            "bio": "string",
            "profile_picture": "url"
        }
    ]
    """
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.request.user.following.all()


class FollowersListView(generics.ListAPIView):
    """
    API endpoint to list users who follow the authenticated user.
    
    GET /api/accounts/followers/
    
    Response:
    [
        {
            "id": int,
            "username": "string",
            "bio": "string",
            "profile_picture": "url"
        }
    ]
    """
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.request.user.followers.all()

