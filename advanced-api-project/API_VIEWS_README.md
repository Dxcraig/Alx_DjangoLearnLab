# API Views Documentation

## Overview

This document provides comprehensive documentation for the Book API views implemented using Django REST Framework's generic views. The API provides full CRUD (Create, Read, Update, Delete) functionality for managing books in the system.

## Table of Contents

- [Architecture](#architecture)
- [View Configurations](#view-configurations)
- [Permissions](#permissions)
- [Custom Hooks and Extensions](#custom-hooks-and-extensions)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)

## Architecture

### Technology Stack

- **Django REST Framework**: Provides the generic view classes and serialization
- **Generic Views**: Built-in DRF views that handle common patterns
- **Permissions**: DRF permission classes for access control
- **Filters**: DRF filter backends for search and ordering

### View Hierarchy

All views inherit from Django REST Framework's generic views:

```
generics.GenericAPIView (base)
├── generics.ListAPIView → BookListView
├── generics.RetrieveAPIView → BookDetailView
├── generics.CreateAPIView → BookCreateView
├── generics.UpdateAPIView → BookUpdateView
└── generics.DestroyAPIView → BookDeleteView
```

## View Configurations

### 1. BookListView

**Purpose**: Retrieve all books with filtering and search capabilities

**Generic Class**: `generics.ListAPIView`

**Configuration**:
```python
queryset = Book.objects.all()
serializer_class = BookSerializer
permission_classes = [IsAuthenticatedOrReadOnly]
filter_backends = [filters.SearchFilter, filters.OrderingFilter]
search_fields = ['title', 'author__name']
ordering_fields = ['title', 'publication_year']
ordering = ['title']
```

**Custom Settings**:
- **filter_backends**: Enables search and ordering functionality
  - `SearchFilter`: Allows text-based searching across specified fields
  - `OrderingFilter`: Enables result ordering by specified fields
  
- **search_fields**: Defines which fields are searchable
  - `title`: Direct field on Book model
  - `author__name`: Related field (follows ForeignKey relationship)
  
- **ordering_fields**: Fields available for ordering results
  - Clients can order by `title` or `publication_year`
  - Supports ascending (default) and descending (prefix with `-`)
  
- **ordering**: Default ordering applied if not specified by client
  - Books are sorted alphabetically by title

**HTTP Methods**: GET

**Returns**: List of book objects (200 OK)

---

### 2. BookDetailView

**Purpose**: Retrieve a single book by its ID

**Generic Class**: `generics.RetrieveAPIView`

**Configuration**:
```python
queryset = Book.objects.all()
serializer_class = BookSerializer
permission_classes = [IsAuthenticatedOrReadOnly]
```

**Custom Settings**:
- No custom behavior beyond standard retrieval
- Uses primary key (pk) from URL to fetch specific book

**HTTP Methods**: GET

**Returns**: Single book object (200 OK) or 404 if not found

---

### 3. BookCreateView

**Purpose**: Create a new book in the system

**Generic Class**: `generics.CreateAPIView`

**Configuration**:
```python
queryset = Book.objects.all()
serializer_class = BookSerializer
permission_classes = [IsAuthenticated]
```

**Custom Settings**:
- **permission_classes**: Restricted to authenticated users only
- **perform_create() hook**: Custom method for additional logic during creation

**Custom Hook Details**:
```python
def perform_create(self, serializer):
    """
    Called after validation, before saving the instance.
    Allows injection of custom business logic.
    """
    # Add custom logic here (logging, notifications, etc.)
    serializer.save()
```

**Use Cases for Custom Hook**:
- Audit logging (track who created the book and when)
- Sending notifications to administrators
- Updating related models or counters
- Setting additional fields based on request context

**HTTP Methods**: POST

**Returns**: Created book object (201 Created) or validation errors (400 Bad Request)

---

### 4. BookUpdateView

**Purpose**: Update an existing book

**Generic Class**: `generics.UpdateAPIView`

**Configuration**:
```python
queryset = Book.objects.all()
serializer_class = BookSerializer
permission_classes = [IsAuthenticated]
```

**Custom Settings**:
- **permission_classes**: Restricted to authenticated users only
- **perform_update() hook**: Custom method for additional logic during updates
- Supports both full updates (PUT) and partial updates (PATCH)

**Custom Hook Details**:
```python
def perform_update(self, serializer):
    """
    Called after validation, before saving changes.
    Allows injection of custom business logic.
    Access original instance via serializer.instance
    Access new data via serializer.validated_data
    """
    # Add custom logic here
    serializer.save()
```

**Use Cases for Custom Hook**:
- Audit logging (track changes and who made them)
- Version control (save previous state before updating)
- Cascade updates to related objects
- Custom validation based on current state vs. new state
- Updating timestamps or metadata

**HTTP Methods**: PUT (full update), PATCH (partial update)

**Returns**: Updated book object (200 OK) or errors (400/401/404)

---

### 5. BookDeleteView

**Purpose**: Delete a book from the system

**Generic Class**: `generics.DestroyAPIView`

**Configuration**:
```python
queryset = Book.objects.all()
serializer_class = BookSerializer
permission_classes = [IsAuthenticated]
```

**Custom Settings**:
- **permission_classes**: Restricted to authenticated users only
- Performs hard delete (permanent removal from database)

**HTTP Methods**: DELETE

**Returns**: No content (204 No Content) or errors (401/404)

---

## Permissions

### Permission Classes Used

#### 1. IsAuthenticatedOrReadOnly

**Applied to**: BookListView, BookDetailView

**Behavior**:
- **Unauthenticated users**: Read-only access (GET requests allowed)
- **Authenticated users**: Full access (GET and write operations)

**Purpose**: 
- Allows public browsing of books
- Protects against unauthorized modifications

#### 2. IsAuthenticated

**Applied to**: BookCreateView, BookUpdateView, BookDeleteView

**Behavior**:
- **Unauthenticated users**: Access denied (401 Unauthorized)
- **Authenticated users**: Full access granted

**Purpose**:
- Ensures only registered users can modify data
- Protects against anonymous spam or vandalism

### Authentication Methods

The API supports standard DRF authentication methods (configured in settings.py):
- Session Authentication (for browsable API)
- Token Authentication (for programmatic access)
- Basic Authentication (for testing)

### Customizing Permissions

To add custom permissions, extend the views:

```python
from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission: only book author can edit/delete
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.author == request.user

# Apply to view
class BookUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
```

---

## Custom Hooks and Extensions

### perform_create() Hook

**Location**: BookCreateView

**Execution Flow**:
1. Client sends POST request with data
2. DRF validates request format
3. Serializer validates data (field types, constraints)
4. **perform_create() is called** ← Custom logic here
5. Instance is saved to database
6. Response is returned to client

**Extension Examples**:

```python
def perform_create(self, serializer):
    # Example 1: Set fields from request context
    serializer.save(created_by=self.request.user)
    
    # Example 2: Send notification
    book = serializer.save()
    send_notification(f"New book added: {book.title}")
    
    # Example 3: Update related models
    author = serializer.validated_data['author']
    author.book_count += 1
    author.save()
    serializer.save()
```

### perform_update() Hook

**Location**: BookUpdateView

**Execution Flow**:
1. Client sends PUT/PATCH request with data
2. DRF validates request format
3. Existing instance is retrieved
4. Serializer validates new data
5. **perform_update() is called** ← Custom logic here
6. Changes are saved to database
7. Response is returned to client

**Extension Examples**:

```python
def perform_update(self, serializer):
    # Example 1: Audit logging
    old_instance = serializer.instance
    new_data = serializer.validated_data
    log_change(old_instance, new_data, self.request.user)
    serializer.save()
    
    # Example 2: Version control
    create_version_snapshot(serializer.instance)
    serializer.save(last_modified_by=self.request.user)
    
    # Example 3: Conditional updates
    if 'publication_year' in new_data:
        # Trigger reindexing or cache invalidation
        invalidate_cache(f"book_{serializer.instance.id}")
    serializer.save()
```

### Overriding Default Behavior

You can override additional methods for more control:

```python
class BookCreateView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        """Override the entire create process"""
        # Pre-processing
        modified_data = self.preprocess_data(request.data)
        
        # Standard create logic
        serializer = self.get_serializer(data=modified_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Post-processing
        self.post_create_actions(serializer.instance)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
```

---

## API Endpoints

### Base URL

All endpoints are prefixed with `/api/`

### Endpoint Summary

| Endpoint | Method | View | Authentication | Description |
|----------|--------|------|----------------|-------------|
| `/api/books/` | GET | BookListView | Optional | List all books |
| `/api/books/<int:pk>/` | GET | BookDetailView | Optional | Get single book |
| `/api/books/create/` | POST | BookCreateView | Required | Create new book |
| `/api/books/update/` | PUT/PATCH | BookUpdateView | Required | Update existing book |
| `/api/books/delete/` | DELETE | BookDeleteView | Required | Delete book |

### URL Configuration

**File**: `api/urls.py`

```python
from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/', BookDeleteView.as_view(), name='book-delete'),
]
```

**Main URLs**: Include in project's main `urls.py`:
```python
urlpatterns = [
    path('api/', include('api.urls')),
]
```

---

## Usage Examples

### 1. List All Books

**Request**:
```bash
GET /api/books/
```

**Response** (200 OK):
```json
[
    {
        "id": 1,
        "title": "Django for Beginners",
        "publication_year": 2023,
        "author": 1
    },
    {
        "id": 2,
        "title": "Python Crash Course",
        "publication_year": 2022,
        "author": 2
    }
]
```

### 2. Search Books

**Request**:
```bash
GET /api/books/?search=Django
```

**Response** (200 OK):
```json
[
    {
        "id": 1,
        "title": "Django for Beginners",
        "publication_year": 2023,
        "author": 1
    }
]
```

### 3. Order Books

**Request**:
```bash
GET /api/books/?ordering=-publication_year
```

**Response**: Books ordered by publication year (newest first)

### 4. Get Single Book

**Request**:
```bash
GET /api/books/1/
```

**Response** (200 OK):
```json
{
    "id": 1,
    "title": "Django for Beginners",
    "publication_year": 2023,
    "author": 1
}
```

### 5. Create New Book

**Request**:
```bash
POST /api/books/create/
Content-Type: application/json
Authorization: Token <your-token>

{
    "title": "Advanced Django",
    "publication_year": 2024,
    "author": 1
}
```

**Response** (201 Created):
```json
{
    "id": 3,
    "title": "Advanced Django",
    "publication_year": 2024,
    "author": 1
}
```

### 6. Update Book (Full)

**Request**:
```bash
PUT /api/books/update/
Content-Type: application/json
Authorization: Token <your-token>

{
    "id": 3,
    "title": "Advanced Django - Updated",
    "publication_year": 2024,
    "author": 1
}
```

**Response** (200 OK): Updated book object

### 7. Update Book (Partial)

**Request**:
```bash
PATCH /api/books/update/
Content-Type: application/json
Authorization: Token <your-token>

{
    "id": 3,
    "title": "Advanced Django - New Title"
}
```

**Response** (200 OK): Updated book object

### 8. Delete Book

**Request**:
```bash
DELETE /api/books/delete/
Content-Type: application/json
Authorization: Token <your-token>

{
    "id": 3
}
```

**Response** (204 No Content): Empty response

---

## Error Handling

### Common Error Responses

#### 400 Bad Request

**Cause**: Validation errors, invalid data format

**Example Response**:
```json
{
    "publication_year": [
        "Publication year cannot be in the future."
    ]
}
```

#### 401 Unauthorized

**Cause**: Missing or invalid authentication credentials

**Example Response**:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

#### 403 Forbidden

**Cause**: Authenticated but lacking permission

**Example Response**:
```json
{
    "detail": "You do not have permission to perform this action."
}
```

#### 404 Not Found

**Cause**: Requested resource doesn't exist

**Example Response**:
```json
{
    "detail": "Not found."
}
```

### Validation Rules

**Book Model Validation** (enforced by BookSerializer):

1. **title**: Required, max 200 characters
2. **publication_year**: 
   - Required
   - Must be an integer
   - Cannot be in the future (custom validation)
3. **author**: 
   - Required
   - Must reference existing Author instance
   - Foreign key constraint enforced

---

## Testing the API

### Using cURL

```bash
# List books
curl http://localhost:8000/api/books/

# Get single book
curl http://localhost:8000/api/books/1/

# Create book (with authentication)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title":"New Book","publication_year":2024,"author":1}'
```

### Using Python requests

```python
import requests

# List books
response = requests.get('http://localhost:8000/api/books/')
books = response.json()

# Create book
headers = {
    'Authorization': 'Token YOUR_TOKEN',
    'Content-Type': 'application/json'
}
data = {
    'title': 'New Book',
    'publication_year': 2024,
    'author': 1
}
response = requests.post(
    'http://localhost:8000/api/books/create/',
    json=data,
    headers=headers
)
```

### Using DRF Browsable API

1. Navigate to `http://localhost:8000/api/books/` in your browser
2. Use the built-in forms to test CRUD operations
3. Login via the browsable API interface for authenticated operations

---

## Best Practices

### 1. Always Use HTTPS in Production

Protect authentication tokens and sensitive data by using HTTPS in production environments.

### 2. Implement Rate Limiting

Add throttling to prevent abuse:

```python
from rest_framework.throttling import UserRateThrottle

class BookCreateView(generics.CreateAPIView):
    throttle_classes = [UserRateThrottle]
```

### 3. Add Pagination

For large datasets, enable pagination in settings:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

### 4. Use Versioning

Implement API versioning for future changes:

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning'
}
```

### 5. Log Important Actions

Add logging to custom hooks:

```python
import logging
logger = logging.getLogger(__name__)

def perform_create(self, serializer):
    book = serializer.save()
    logger.info(f"Book created: {book.id} by {self.request.user}")
```

---

## Troubleshooting

### Issue: 401 Unauthorized on authenticated requests

**Solution**: Ensure token is included in Authorization header:
```
Authorization: Token <your-token-here>
```

### Issue: Search not working

**Solution**: Verify search fields are properly indexed and exist on the model

### Issue: Validation errors on create/update

**Solution**: Check serializer validation rules and ensure data matches expected format

### Issue: 404 on update/delete

**Solution**: For these endpoints, include the book ID in the request body, not the URL

---

## Future Enhancements

Potential improvements to consider:

1. **Soft Deletes**: Implement soft deletion instead of hard deletes
2. **Bulk Operations**: Add endpoints for bulk create/update/delete
3. **Advanced Filtering**: Integrate django-filter for complex queries
4. **Export Functionality**: Add CSV/PDF export options
5. **Caching**: Implement Redis caching for frequently accessed data
6. **Webhooks**: Send notifications on CRUD operations
7. **API Documentation**: Auto-generate docs using drf-spectacular or Swagger

---

## Support

For questions or issues:
- Review Django REST Framework documentation: https://www.django-rest-framework.org/
- Check the project's issue tracker
- Contact the development team

---

**Last Updated**: December 7, 2025  
**Version**: 1.0  
**Author**: Development Team
