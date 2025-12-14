from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from taggit.models import Tag
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm, PostForm
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
    - Displays all comments associated with the post
    - Provides a form for authenticated users to add new comments
    - Accessible to all users (no authentication required)
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """
        Add comments and comment form to the context.
        """
        context = super().get_context_data(**kwargs)
        # Get all comments for this post, ordered by creation date
        context['comments'] = self.object.comments.all().order_by('created_at')
        # Add comment form for authenticated users
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for adding new blog posts.
    
    - Requires user authentication (LoginRequiredMixin)
    - Automatically sets the author to the logged-in user
    - Redirects to post detail page on success
    """
    model = Post
    form_class = PostForm
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
    form_class = PostForm
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


# Comment CRUD Views

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for adding new comments to blog posts.
    
    - Requires user authentication (LoginRequiredMixin)
    - Automatically sets the author to the logged-in user
    - Associates the comment with the specified post
    - Redirects to post detail page on success
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """
        Set the author to the current logged-in user and associate with the post.
        """
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        messages.success(self.request, 'Your comment has been added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Redirect to the post detail page after successful comment creation.
        """
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        """
        Add the post to the context for display in the template.
        """
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update view for editing existing comments.
    
    - Requires user authentication (LoginRequiredMixin)
    - Only the comment author can edit (UserPassesTestMixin)
    - Redirects to post detail page on success
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """
        Add success message on valid form submission.
        """
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """
        Test that the current user is the author of the comment.
        """
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        """
        Redirect to the post detail page after successful update.
        """
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    
    def get_context_data(self, **kwargs):
        """
        Add context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        context['is_edit'] = True
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete view for removing comments.
    
    - Requires user authentication (LoginRequiredMixin)
    - Only the comment author can delete (UserPassesTestMixin)
    - Redirects to post detail page on success
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        """
        Add success message on deletion.
        """
        messages.success(request, 'Your comment has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """
        Test that the current user is the author of the comment.
        """
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        """
        Redirect to the post detail page after successful deletion.
        """
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    
    def get_context_data(self, **kwargs):
        """
        Add context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        return context


def search_posts(request):
    """
    Search view for finding blog posts based on title, content, or tags.
    
    Uses Django's Q objects for complex query lookups to filter posts by:
    - Title (case-insensitive contains)
    - Content (case-insensitive contains)
    - Tags (tag name contains)
    
    Accessible via GET parameter 'q' for the search query.
    """
    query = request.GET.get('q', '')
    results = Post.objects.none()
    
    if query:
        # Use Q objects for complex lookups across multiple fields
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-published_date')
    
    context = {
        'query': query,
        'results': results,
        'result_count': results.count()
    }
    
    return render(request, 'blog/search_results.html', context)


class PostByTagListView(ListView):
    """
    List view for displaying blog posts filtered by a specific tag.
    
    - Displays all posts with the specified tag
    - Ordered by publication date (newest first)
    - Uses pagination (10 posts per page)
    - Accessible to all users
    """
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Filter posts by the tag slug from the URL.
        """
        tag_slug = self.kwargs.get('tag_slug')
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags__in=[self.tag]).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        """
        Add the current tag to the context.
        """
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context
