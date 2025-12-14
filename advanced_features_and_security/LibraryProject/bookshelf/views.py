from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q

from .models import Book
from .forms import BookForm
from .forms import ExampleForm
from django.contrib import messages


@permission_required('bookshelf.can_view', raise_exception=True)
def view_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('bookshelf_view_book', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form, 'action': 'Create'})


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookshelf_view_book', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/form_example.html', {'form': form, 'action': 'Edit'})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('bookshelf_book_list')


def example_form(request):
    """Render and process the small `ExampleForm` used for demos.

    GET: show empty form
    POST: validate and show success message with submitted name
    
    SECURITY NOTE: This view demonstrates secure input handling:
    - Uses Django forms for automatic input validation and sanitization
    - Form.is_valid() validates all fields before processing
    - cleaned_data provides sanitized user input
    - Messages framework safely escapes output by default
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Use cleaned_data to access validated and sanitized input
            # This prevents XSS attacks by ensuring data is properly escaped
            name = form.cleaned_data.get('name')
            messages.success(request, f'Thanks, {name}! Your message was received.')
            return redirect('bookshelf_example_form')
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/example_form.html', {'form': form})


@permission_required('bookshelf.can_view', raise_exception=True)
def search_books(request):
    """Search for books by title or author using secure query methods.
    
    SECURITY MEASURES IMPLEMENTED:
    1. SQL Injection Prevention: Uses Django ORM with parameterized queries
       instead of raw SQL or string formatting
    2. Input Validation: Validates and sanitizes search query
    3. XSS Protection: Django templates auto-escape output by default
    4. Permission Required: Only users with can_view permission can search
    
    ANTI-PATTERN (DO NOT USE):
        # INSECURE: Direct SQL concatenation vulnerable to SQL injection
        # query = "SELECT * FROM books WHERE title LIKE '%%" + search_query + "%%'"
        # Book.objects.raw(query)
    
    SECURE PATTERN (USED HERE):
        # Uses Django ORM with Q objects for safe parameterized queries
        # Django automatically escapes and parameterizes the query
    """
    # Get search query from GET parameters
    search_query = request.GET.get('q', '').strip()
    
    # Initialize empty queryset
    books = Book.objects.none()
    
    if search_query:
        # SECURITY: Input validation - limit query length to prevent abuse
        if len(search_query) > 100:
            messages.warning(request, 'Search query too long. Maximum 100 characters.')
        else:
            # SECURITY: Use Django ORM with Q objects for safe queries
            # This prevents SQL injection by using parameterized queries
            # The icontains lookup is safe and automatically escaped
            books = Book.objects.filter(
                Q(title__icontains=search_query) | 
                Q(author__icontains=search_query)
            )
            
            if not books.exists():
                messages.info(request, f'No books found matching "{search_query}"')
    
    # Pass search query back to template for display
    # Django templates automatically escape this value to prevent XSS
    context = {
        'books': books,
        'search_query': search_query,
    }
    
    return render(request, 'bookshelf/book_search.html', context)
