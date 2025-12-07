"""
API Views for Book Management

This module contains Django REST Framework generic views for handling CRUD operations
on the Book model. Each view is configured with appropriate permissions, filters,
and custom behavior to ensure secure and efficient API operations.

View Classes:
    - BookListView: List all books with filtering, searching, and ordering capabilities
    - BookDetailView: Retrieve a single book by ID
    - BookCreateView: Create a new book (authenticated users only)
    - BookUpdateView: Update an existing book (authenticated users only)
    - BookDeleteView: Delete a book (authenticated users only)

Permissions:
    - Read operations (List, Detail): IsAuthenticatedOrReadOnly
    - Write operations (Create, Update, Delete): IsAuthenticated

Advanced Query Capabilities:
    - Filtering: Filter by title, author, and publication_year
    - Search: Full-text search on title and author name
    - Ordering: Sort by title and publication_year (ascending/descending)
    - Custom validation through perform_create and perform_update hooks
"""

from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    API view to retrieve all books with advanced filtering, searching, and ordering.
    
    Endpoint: GET /api/books/
    
    Permissions:
        - IsAuthenticatedOrReadOnly: Anyone can read, only authenticated users can write
    
    Advanced Query Capabilities:
    
    1. FILTERING:
        Filter books by exact matches on specific fields.
        - Filter by title: ?title=<book_title>
        - Filter by author ID: ?author=<author_id>
        - Filter by publication year: ?publication_year=<year>
        - Combine multiple filters: ?author=1&publication_year=2023
    
    2. SEARCHING:
        Perform text-based searches across multiple fields.
        - Search in title or author name: ?search=<query>
        - Searches are case-insensitive and use partial matching
        - Example: ?search=Django (finds "Django for Beginners", "Advanced Django", etc.)
    
    3. ORDERING:
        Sort results by specified fields.
        - Order by title: ?ordering=title (ascending)
        - Order by publication year: ?ordering=publication_year
        - Reverse order (descending): ?ordering=-publication_year
        - Multiple ordering: ?ordering=publication_year,title
        - Default ordering: title (ascending)
    
    Query Parameters:
        - title (str): Exact match filter for book title
        - author (int): Filter by author ID
        - publication_year (int): Filter by publication year
        - search (str): Search term for title or author name (partial matching)
        - ordering (str): Field name(s) for ordering results (prefix with '-' for descending)
    
    Returns:
        - 200 OK: Paginated list of books matching the filter/search criteria
    
    Examples:
        # Get all books
        GET /api/books/
        
        # Filter by publication year
        GET /api/books/?publication_year=2023
        
        # Filter by author
        GET /api/books/?author=1
        
        # Search for books about Django
        GET /api/books/?search=Django
        
        # Order by publication year (newest first)
        GET /api/books/?ordering=-publication_year
        
        # Combine filtering, searching, and ordering
        GET /api/books/?author=1&search=Python&ordering=-publication_year
        
        # Filter by title and order by publication year
        GET /api/books/?title=Django%20for%20Beginners&ordering=publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filter backends enable filtering, search, and ordering functionality
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # filterset_fields: Fields available for exact match filtering
    # Users can filter by these fields using query parameters
    filterset_fields = ['title', 'author', 'publication_year']
    
    # search_fields: Fields to search through when using ?search=<query>
    # Performs case-insensitive partial matching across these fields
    search_fields = ['title', 'author__name']
    
    # ordering_fields: Fields available for ordering results
    # Users can sort by these fields using ?ordering=<field>
    ordering_fields = ['title', 'publication_year']
    
    # ordering: Default ordering applied to the queryset
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single book by ID.
    
    Endpoint: GET /api/books/<int:pk>/
    
    Permissions:
        - IsAuthenticatedOrReadOnly: Anyone can read book details
    
    URL Parameters:
        - pk (int): Primary key of the book to retrieve
    
    Returns:
        - 200 OK: Book details
        - 404 Not Found: If book with given ID doesn't exist
    
    Examples:
        GET /api/books/1/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    
    Endpoint: POST /api/books/create/
    
    Permissions:
        - IsAuthenticated: Only authenticated users can create books
    
    Request Body:
        {
            "title": "string",
            "publication_year": integer,
            "author": integer (author ID)
        }
    
    Validation:
        - All fields are required
        - publication_year cannot be in the future (validated in serializer)
        - author must reference an existing Author instance
    
    Custom Hooks:
        - perform_create(): Called after validation, before saving the instance
                          Can be extended to add additional business logic
    
    Returns:
        - 201 Created: Book successfully created with book details
        - 400 Bad Request: Validation errors
        - 401 Unauthorized: User is not authenticated
    
    Examples:
        POST /api/books/create/
        {
            "title": "Django for Beginners",
            "publication_year": 2023,
            "author": 1
        }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom hook called during book creation after validation.
        
        This method is invoked after the serializer validates the data
        but before saving the new book instance to the database.
        
        Args:
            serializer: Validated BookSerializer instance
        
        Custom Logic:
            - Additional validation can be added here
            - Business logic such as logging, notifications, or related object updates
            - Default behavior: saves the validated book instance
        
        Note:
            - Serializer validation (including publication_year check) runs before this method
            - Any exceptions raised here will return a 400 Bad Request response
        """
        # Additional validation or business logic can be added here
        # For example: logging, sending notifications, updating related models, etc.
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    
    Endpoint: PUT /api/books/update/ or PATCH /api/books/update/
    
    Permissions:
        - IsAuthenticated: Only authenticated users can update books
    
    HTTP Methods:
        - PUT: Full update (all fields required)
        - PATCH: Partial update (only specified fields updated)
    
    Request Body:
        PUT: All fields required
        {
            "title": "string",
            "publication_year": integer,
            "author": integer
        }
        
        PATCH: Any subset of fields
        {
            "title": "string"  // Only update title
        }
    
    Validation:
        - publication_year cannot be in the future
        - author must reference an existing Author instance
    
    Custom Hooks:
        - perform_update(): Called after validation, before saving changes
                          Can be extended to add additional business logic
    
    Returns:
        - 200 OK: Book successfully updated with updated book details
        - 400 Bad Request: Validation errors
        - 401 Unauthorized: User is not authenticated
        - 404 Not Found: Book with given ID doesn't exist
    
    Examples:
        PUT /api/books/update/
        {
            "id": 1,
            "title": "Django for Professionals",
            "publication_year": 2024,
            "author": 1
        }
        
        PATCH /api/books/update/
        {
            "id": 1,
            "publication_year": 2024
        }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom hook called during book update after validation.
        
        This method is invoked after the serializer validates the data
        but before saving the updated book instance to the database.
        
        Args:
            serializer: Validated BookSerializer instance with updated data
        
        Custom Logic:
            - Additional validation can be added here
            - Business logic such as audit logging, notifications, or cascade updates
            - Default behavior: saves the validated changes to the book instance
        
        Note:
            - Serializer validation runs before this method
            - Any exceptions raised here will return a 400 Bad Request response
            - Access the original instance via serializer.instance
            - Access the validated new data via serializer.validated_data
        """
        # Additional validation or business logic can be added here
        # For example: audit logging, sending notifications, updating timestamps, etc.
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    
    Endpoint: DELETE /api/books/delete/
    
    Permissions:
        - IsAuthenticated: Only authenticated users can delete books
    
    Request Body:
        {
            "id": integer (book ID to delete)
        }
    
    Returns:
        - 204 No Content: Book successfully deleted
        - 401 Unauthorized: User is not authenticated
        - 404 Not Found: Book with given ID doesn't exist
    
    Warning:
        - This is a destructive operation and cannot be undone
        - Consider implementing soft deletes for production applications
    
    Examples:
        DELETE /api/books/delete/
        {
            "id": 1
        }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]