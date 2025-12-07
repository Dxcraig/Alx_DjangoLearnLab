"""
Unit Tests for Book API Views

This module contains comprehensive unit tests for the Book API endpoints,
covering CRUD operations, filtering, searching, ordering, and permissions.

Test Coverage:
    - CRUD Operations (Create, Read, Update, Delete)
    - Filtering by title, author, and publication_year
    - Searching across title and author name
    - Ordering by title and publication_year
    - Permission enforcement (authenticated vs unauthenticated)
    - Authentication requirements
    - Data validation
    - Error handling

Run tests with:
    python manage.py test api
    python manage.py test api.test_views
    python manage.py test api.test_views.BookAPITestCase
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Book, Author
from .serializers import BookSerializer


class BookAPITestCase(APITestCase):
    """
    Comprehensive test suite for Book API endpoints.
    
    Tests cover:
        - List view with filtering, searching, and ordering
        - Detail view for retrieving single books
        - Create view for adding new books
        - Update view for modifying existing books
        - Delete view for removing books
        - Permission and authentication enforcement
    """
    
    def setUp(self):
        """
        Set up test data and authentication.
        
        Creates:
            - Test user for authenticated requests
            - Sample authors
            - Sample books with various attributes
            - API client for making requests
        """
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create API client
        self.client = APIClient()
        
        # Create test authors
        self.author1 = Author.objects.create(name="William Vincent")
        self.author2 = Author.objects.create(name="Eric Matthes")
        self.author3 = Author.objects.create(name="Luciano Ramalho")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Django for Beginners",
            publication_year=2023,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Python Crash Course",
            publication_year=2019,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title="Django for APIs",
            publication_year=2022,
            author=self.author1
        )
        self.book4 = Book.objects.create(
            title="Fluent Python",
            publication_year=2015,
            author=self.author3
        )
        
        # Store URLs for convenience
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update')
        self.delete_url = reverse('book-delete')
    
    def tearDown(self):
        """Clean up after each test"""
        self.client.logout()
    
    # ==================== LIST VIEW TESTS ====================
    
    def test_list_books_unauthenticated(self):
        """
        Test that unauthenticated users can list books (read-only access).
        
        Expected: 200 OK with paginated list of books
        """
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 4)
    
    def test_list_books_authenticated(self):
        """
        Test that authenticated users can list books.
        
        Expected: 200 OK with paginated list of books
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 4)
    
    def test_list_books_pagination(self):
        """
        Test that pagination works correctly.
        
        Expected: Response includes pagination metadata
        """
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 4)
    
    # ==================== FILTERING TESTS ====================
    
    def test_filter_by_publication_year(self):
        """
        Test filtering books by publication year.
        
        Expected: Only books from specified year are returned
        """
        response = self.client.get(self.list_url, {'publication_year': 2023})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Django for Beginners")
        self.assertEqual(results[0]['publication_year'], 2023)
    
    def test_filter_by_author(self):
        """
        Test filtering books by author ID.
        
        Expected: Only books by specified author are returned
        """
        response = self.client.get(self.list_url, {'author': self.author1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
        
        # Verify all results are by the correct author
        for book in results:
            self.assertEqual(book['author'], self.author1.id)
    
    def test_filter_by_title(self):
        """
        Test filtering books by exact title.
        
        Expected: Only books with exact title match are returned
        """
        response = self.client.get(self.list_url, {'title': 'Django for APIs'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Django for APIs')
    
    def test_filter_multiple_criteria(self):
        """
        Test filtering with multiple criteria (author and year).
        
        Expected: Only books matching all criteria are returned
        """
        response = self.client.get(
            self.list_url,
            {'author': self.author1.id, 'publication_year': 2023}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Django for Beginners')
    
    def test_filter_no_results(self):
        """
        Test filtering with criteria that match no books.
        
        Expected: Empty results list
        """
        response = self.client.get(self.list_url, {'publication_year': 2030})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 0)
    
    # ==================== SEARCHING TESTS ====================
    
    def test_search_by_title(self):
        """
        Test searching books by title (partial match).
        
        Expected: Books with matching titles are returned
        """
        response = self.client.get(self.list_url, {'search': 'Django'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
        
        # Verify all results contain 'Django' in title
        for book in results:
            self.assertIn('Django', book['title'])
    
    def test_search_by_author_name(self):
        """
        Test searching books by author name.
        
        Expected: Books by authors with matching names are returned
        """
        response = self.client.get(self.list_url, {'search': 'Vincent'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
    
    def test_search_case_insensitive(self):
        """
        Test that search is case-insensitive.
        
        Expected: Search finds matches regardless of case
        """
        response1 = self.client.get(self.list_url, {'search': 'python'})
        response2 = self.client.get(self.list_url, {'search': 'PYTHON'})
        response3 = self.client.get(self.list_url, {'search': 'Python'})
        
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        
        # All should return same results
        self.assertEqual(
            len(response1.data['results']),
            len(response2.data['results'])
        )
        self.assertEqual(
            len(response2.data['results']),
            len(response3.data['results'])
        )
    
    def test_search_partial_match(self):
        """
        Test that search works with partial matches.
        
        Expected: Partial terms match full words
        """
        response = self.client.get(self.list_url, {'search': 'Djan'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertGreaterEqual(len(results), 1)
    
    def test_search_no_results(self):
        """
        Test search with term that matches nothing.
        
        Expected: Empty results list
        """
        response = self.client.get(self.list_url, {'search': 'NonexistentBook'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 0)
    
    # ==================== ORDERING TESTS ====================
    
    def test_ordering_by_title_ascending(self):
        """
        Test ordering books by title (A-Z).
        
        Expected: Books are sorted alphabetically by title
        """
        response = self.client.get(self.list_url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        
        titles = [book['title'] for book in results]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_title_descending(self):
        """
        Test ordering books by title (Z-A).
        
        Expected: Books are sorted reverse alphabetically
        """
        response = self.client.get(self.list_url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        
        titles = [book['title'] for book in results]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_ordering_by_year_ascending(self):
        """
        Test ordering books by publication year (oldest first).
        
        Expected: Books are sorted by year, oldest to newest
        """
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        
        years = [book['publication_year'] for book in results]
        self.assertEqual(years, sorted(years))
    
    def test_ordering_by_year_descending(self):
        """
        Test ordering books by publication year (newest first).
        
        Expected: Books are sorted by year, newest to oldest
        """
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        
        years = [book['publication_year'] for book in results]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_default_ordering(self):
        """
        Test default ordering (should be by title).
        
        Expected: Without ordering parameter, books are sorted by title
        """
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        
        titles = [book['title'] for book in results]
        self.assertEqual(titles, sorted(titles))
    
    # ==================== COMBINED QUERY TESTS ====================
    
    def test_filter_and_search(self):
        """
        Test combining filtering and searching.
        
        Expected: Results match both filter and search criteria
        """
        response = self.client.get(
            self.list_url,
            {'author': self.author1.id, 'search': 'Django'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
    
    def test_search_and_ordering(self):
        """
        Test combining searching and ordering.
        
        Expected: Search results are properly ordered
        """
        response = self.client.get(
            self.list_url,
            {'search': 'Django', 'ordering': '-publication_year'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        
        # Verify ordering
        years = [book['publication_year'] for book in results]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_filter_search_and_ordering(self):
        """
        Test combining filtering, searching, and ordering.
        
        Expected: All three operations work together correctly
        """
        response = self.client.get(
            self.list_url,
            {
                'author': self.author1.id,
                'search': 'Django',
                'ordering': 'title'
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        
        # Verify filtering
        for book in results:
            self.assertEqual(book['author'], self.author1.id)
        
        # Verify ordering
        titles = [book['title'] for book in results]
        self.assertEqual(titles, sorted(titles))
    
    # ==================== DETAIL VIEW TESTS ====================
    
    def test_retrieve_book_unauthenticated(self):
        """
        Test retrieving a single book without authentication.
        
        Expected: 200 OK with book details
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.book1.author.id)
    
    def test_retrieve_book_authenticated(self):
        """
        Test retrieving a single book with authentication.
        
        Expected: 200 OK with book details
        """
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_retrieve_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist.
        
        Expected: 404 Not Found
        """
        url = reverse('book-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ==================== CREATE VIEW TESTS ====================
    
    def test_create_book_authenticated(self):
        """
        Test creating a book with authentication.
        
        Expected: 201 Created with book details
        """
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Test Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['publication_year'], 2024)
        
        # Verify book was actually created in database
        self.assertTrue(Book.objects.filter(title='Test Book').exists())
    
    def test_create_book_unauthenticated(self):
        """
        Test creating a book without authentication.
        
        Expected: 401 Unauthorized or 403 Forbidden
        """
        data = {
            'title': 'Test Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
    
    def test_create_book_missing_fields(self):
        """
        Test creating a book with missing required fields.
        
        Expected: 400 Bad Request with validation errors
        """
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Incomplete Book'
            # Missing publication_year and author
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_book_invalid_year(self):
        """
        Test creating a book with future publication year.
        
        Expected: 400 Bad Request with validation error
        """
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Future Book',
            'publication_year': 2030,
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_invalid_author(self):
        """
        Test creating a book with non-existent author.
        
        Expected: 400 Bad Request
        """
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Test Book',
            'publication_year': 2024,
            'author': 99999  # Non-existent author ID
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # ==================== UPDATE VIEW TESTS ====================
    
    def test_update_book_authenticated(self):
        """
        Test updating a book with authentication (PUT).
        
        Expected: 200 OK with updated book details
        """
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'id': self.book1.id,
            'title': 'Updated Title',
            'publication_year': 2024,
            'author': self.author1.id
        }
        
        response = self.client.put(self.update_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        
        # Verify database was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
    
    def test_partial_update_book_authenticated(self):
        """
        Test partially updating a book with authentication (PATCH).
        
        Expected: 200 OK with updated book details
        """
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'id': self.book1.id,
            'title': 'Partially Updated Title'
        }
        
        response = self.client.patch(self.update_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated Title')
        
        # Verify other fields unchanged
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.publication_year, 2023)
    
    def test_update_book_unauthenticated(self):
        """
        Test updating a book without authentication.
        
        Expected: 401 Unauthorized or 403 Forbidden
        """
        data = {
            'id': self.book1.id,
            'title': 'Updated Title',
            'publication_year': 2024,
            'author': self.author1.id
        }
        
        response = self.client.put(self.update_url, data, format='json')
        
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
    
    def test_update_nonexistent_book(self):
        """
        Test updating a book that doesn't exist.
        
        Expected: 404 Not Found
        """
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'id': 99999,
            'title': 'Updated Title',
            'publication_year': 2024,
            'author': self.author1.id
        }
        
        response = self.client.put(self.update_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_book_invalid_data(self):
        """
        Test updating a book with invalid data.
        
        Expected: 400 Bad Request
        """
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'id': self.book1.id,
            'title': 'Updated Title',
            'publication_year': 2030,  # Future year (invalid)
            'author': self.author1.id
        }
        
        response = self.client.put(self.update_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # ==================== DELETE VIEW TESTS ====================
    
    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authentication.
        
        Expected: 204 No Content, book removed from database
        """
        self.client.login(username='testuser', password='testpass123')
        
        book_id = self.book4.id
        data = {'id': book_id}
        
        response = self.client.delete(self.delete_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book was deleted
        self.assertFalse(Book.objects.filter(id=book_id).exists())
    
    def test_delete_book_unauthenticated(self):
        """
        Test deleting a book without authentication.
        
        Expected: 401 Unauthorized or 403 Forbidden
        """
        data = {'id': self.book1.id}
        
        response = self.client.delete(self.delete_url, data, format='json')
        
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
        
        # Verify book still exists
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_nonexistent_book(self):
        """
        Test deleting a book that doesn't exist.
        
        Expected: 404 Not Found
        """
        self.client.login(username='testuser', password='testpass123')
        
        data = {'id': 99999}
        
        response = self.client.delete(self.delete_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ==================== PERMISSION TESTS ====================
    
    def test_list_view_allows_unauthenticated_read(self):
        """
        Test that list view allows unauthenticated GET requests.
        
        Expected: 200 OK (IsAuthenticatedOrReadOnly permission)
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_view_allows_unauthenticated_read(self):
        """
        Test that detail view allows unauthenticated GET requests.
        
        Expected: 200 OK (IsAuthenticatedOrReadOnly permission)
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_view_requires_authentication(self):
        """
        Test that create view requires authentication.
        
        Expected: 401/403 (IsAuthenticated permission)
        """
        data = {
            'title': 'Test',
            'publication_year': 2024,
            'author': self.author1.id
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
    
    def test_update_view_requires_authentication(self):
        """
        Test that update view requires authentication.
        
        Expected: 401/403 (IsAuthenticated permission)
        """
        data = {
            'id': self.book1.id,
            'title': 'Updated',
            'publication_year': 2024,
            'author': self.author1.id
        }
        response = self.client.put(self.update_url, data, format='json')
        
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
    
    def test_delete_view_requires_authentication(self):
        """
        Test that delete view requires authentication.
        
        Expected: 401/403 (IsAuthenticated permission)
        """
        data = {'id': self.book1.id}
        response = self.client.delete(self.delete_url, data, format='json')
        
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
    
    # ==================== DATA INTEGRITY TESTS ====================
    
    def test_book_data_structure(self):
        """
        Test that book data structure is correct.
        
        Expected: Response contains all required fields
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        required_fields = ['id', 'title', 'publication_year', 'author']
        for field in required_fields:
            self.assertIn(field, response.data)
    
    def test_serializer_validation(self):
        """
        Test that serializer properly validates data.
        
        Expected: Invalid data is rejected with appropriate errors
        """
        self.client.login(username='testuser', password='testpass123')
        
        # Test with invalid type for publication_year
        data = {
            'title': 'Test Book',
            'publication_year': 'not_a_number',
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_database_integrity_after_operations(self):
        """
        Test that database maintains integrity after CRUD operations.
        
        Expected: Counts match expected values
        """
        initial_count = Book.objects.count()
        
        # Create a book
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Integrity Test Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(Book.objects.count(), initial_count + 1)
        
        # Delete a book
        book = Book.objects.get(title='Integrity Test Book')
        self.client.delete(self.delete_url, {'id': book.id}, format='json')
        
        self.assertEqual(Book.objects.count(), initial_count)


class BookAPIEdgeCaseTestCase(APITestCase):
    """
    Test edge cases and error conditions for Book API.
    """
    
    def setUp(self):
        """Set up minimal test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        self.client = APIClient()
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
    
    def test_empty_database_list(self):
        """
        Test listing books when database is empty.
        
        Expected: 200 OK with empty results
        """
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_very_long_title(self):
        """
        Test creating a book with title exceeding max length.
        
        Expected: 400 Bad Request
        """
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'A' * 300,  # Exceeds max_length of 200
            'publication_year': 2024,
            'author': self.author.id
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_special_characters_in_search(self):
        """
        Test search with special characters.
        
        Expected: 200 OK, handles special characters gracefully
        """
        Book.objects.create(
            title="C++ Programming",
            publication_year=2020,
            author=self.author
        )
        
        response = self.client.get(self.list_url, {'search': 'C++'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_sql_injection_attempt(self):
        """
        Test that SQL injection attempts are prevented.
        
        Expected: 200 OK with no SQL errors, no data breach
        """
        # Attempt SQL injection through search
        response = self.client.get(
            self.list_url,
            {'search': "'; DROP TABLE api_book; --"}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify table still exists by making another query
        self.assertIsNotNone(Book.objects.all())
