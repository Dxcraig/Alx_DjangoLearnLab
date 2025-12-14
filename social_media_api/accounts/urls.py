from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserLogoutView
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
]
