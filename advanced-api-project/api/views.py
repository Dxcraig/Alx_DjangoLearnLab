from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    View to retrieve all books.
    Supports searching by title and author name.
    Supports ordering by title and publication_year.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book by ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    View to add a new book.
    Requires authentication.
    Validates data before creating a new book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom create method to add additional logic during book creation.
        Validates the serializer data and saves the new book instance.
        """
        # Additional validation or business logic can be added here
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    View to modify an existing book.
    Requires authentication.
    Validates data before updating the book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom update method to add additional logic during book updates.
        Validates the serializer data and updates the book instance.
        """
        # Additional validation or business logic can be added here
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    View to remove a book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]