from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Handles user creation with username, email, password, bio, and profile_picture.
    Returns authentication token upon successful registration.
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text="Password must be at least 8 characters long"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Confirm your password"
    )
    token = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'bio', 'profile_picture', 'token']
        extra_kwargs = {
            'email': {'required': True},
            'bio': {'required': False},
            'profile_picture': {'required': False},
        }
    
    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        """Ensure username is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def validate(self, data):
        """Ensure passwords match."""
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        """Create user and generate authentication token."""
        # Remove password_confirm as it's not needed for user creation
        validated_data.pop('password_confirm')
        
        # Extract password to hash it properly
        password = validated_data.pop('password')
        
        # Create user using get_user_model().objects.create_user
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        
        # Create authentication token
        Token.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Accepts username and password, returns authentication token.
    """
    username = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    
    Displays user details including followers and following counts.
    """
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'bio', 'profile_picture',
            'followers_count', 'following_count', 'date_joined'
        ]
        read_only_fields = ['id', 'username', 'date_joined']
    
    def get_followers_count(self, obj):
        """Return the number of followers."""
        return obj.get_followers_count()
    
    def get_following_count(self, obj):
        """Return the number of users being followed."""
        return obj.get_following_count()


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    
    Allows users to update their bio and profile picture.
    """
    class Meta:
        model = User
        fields = ['bio', 'profile_picture']
    
    def update(self, instance, validated_data):
        """Update user profile fields."""
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance
