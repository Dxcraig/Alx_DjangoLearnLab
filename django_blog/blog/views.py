from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm
from .models import Post, Comment


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


# Blog Post CRUD Views

class PostListView(ListView):
    """
    List view for displaying all blog posts.
    
    - Displays all posts ordered by publication date (newest first)
    - Accessible to all users (no authentication required)
    - Uses pagination (10 posts per page)
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-published_date']


class PostDetailView(DetailView):
    """
    Detail view for displaying a single blog post.
    
    - Shows complete post content including title, content, author, and date
    - Accessible to all users (no authentication required)
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for adding new blog posts.
    
    - Requires user authentication (LoginRequiredMixin)
    - Automatically sets the author to the logged-in user
    - Redirects to post detail page on success
    """
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('posts')
    
    def form_valid(self, form):
        """
        Set the author to the current logged-in user before saving.
        """
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
        Add context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Post'
        context['button_text'] = 'Create Post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update view for editing existing blog posts.
    
    - Requires user authentication (LoginRequiredMixin)
    - Only the post author can edit (UserPassesTestMixin)
    - Redirects to post detail page on success
    """
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """
        Add success message on valid form submission.
        """
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """
        Test that the current user is the author of the post.
        """
        post = self.get_object()
        return self.request.user == post.author
    
    def get_context_data(self, **kwargs):
        """
        Add context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Post'
        context['button_text'] = 'Update Post'
        return context
    
    def get_success_url(self):
        """
        Redirect to the post detail page after successful update.
        """
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete view for removing blog posts.
    
    - Requires user authentication (LoginRequiredMixin)
    - Only the post author can delete (UserPassesTestMixin)
    - Redirects to post list page on success
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts')
    context_object_name = 'post'
    
    def delete(self, request, *args, **kwargs):
        """
        Add success message on deletion.
        """
        messages.success(request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """
        Test that the current user is the author of the post.
        """
        post = self.get_object()
        return self.request.user == post.author
