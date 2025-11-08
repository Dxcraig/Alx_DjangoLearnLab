from django.shortcuts import render
from django.views.generic.detail import DetailView
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
