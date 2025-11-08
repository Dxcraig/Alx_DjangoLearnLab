from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Book
from .models import Library

# Create your views here.

def list_books(request):
    """
    Function-based view that lists all books stored in the database.
    Displays book titles and their authors.
    """
    # Query all books from the database
    books = Book.objects.all()
    
    # Pass the books to the template context
    context = {
        'books': books
    }
    
    # Render the template with the book list
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library.
    Shows the library name and lists all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        """
        Add additional context data to include all books in the library.
        """
        context = super().get_context_data(**kwargs)
        # The library object is already available as self.object or context['library']
        # The books are accessible through the ManyToMany relationship
        return context


# User Authentication Views

def register(request):
    """
    Handle user registration.
    Uses Django's built-in UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('list_books')  # Redirect to books list after successful registration
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})


@login_required
def user_logout(request):
    """
    Handle user logout.
    Requires user to be logged in.
    """
    logout(request)
    return render(request, 'relationship_app/logout.html')


def user_login(request):
    """
    Handle user login using Django's authentication system.
    This view is typically handled by Django's built-in LoginView,
    but we define it here for URL routing purposes.
    """
    return render(request, 'relationship_app/login.html')
