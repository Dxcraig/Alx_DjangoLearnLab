from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer
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

