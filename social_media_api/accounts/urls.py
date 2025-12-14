from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserLogoutView,
    FollowUserView,
    UnfollowUserView,
    FollowingListView,
    FollowersListView
)

app_name = 'accounts'

urlpatterns = [
    # User registration endpoint
    path('register/', UserRegistrationView.as_view(), name='register'),
    
    # User login endpoint
    path('login/', UserLoginView.as_view(), name='login'),
    
    # User logout endpoint
    path('logout/', UserLogoutView.as_view(), name='logout'),
    
    # User profile endpoint (view and update)
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Follow management endpoints
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    
    # Following/Followers list endpoints
    path('following/', FollowingListView.as_view(), name='following-list'),
    path('followers/', FollowersListView.as_view(), name='followers-list'),
]
