from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserUpdateForm


def register(request):
    """
    User registration view.
    
    Handles GET and POST requests for user registration.
    - GET: Display registration form
    - POST: Process registration form and create new user
    
    After successful registration, user is automatically logged in
    and redirected to the profile page.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful registration
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    """
    User login view.
    
    Handles GET and POST requests for user authentication.
    - GET: Display login form
    - POST: Authenticate user credentials and log them in
    
    Redirects to profile page on successful login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # Redirect to the page user was trying to access or profile
            next_page = request.GET.get('next', 'profile')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'blog/login.html')


def user_logout(request):
    """
    User logout view.
    
    Logs out the current user and redirects to home page.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """
    User profile view.
    
    Allows authenticated users to view and edit their profile.
    - GET: Display profile with user information and edit form
    - POST: Process profile updates
    
    Requires authentication (login_required decorator).
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    
    return render(request, 'blog/profile.html', context)


def home(request):
    """
    Home page view.
    
    Displays the blog home page.
    """
    return render(request, 'blog/home.html')
