# API Query Capabilities - Testing and Documentation

## Overview

This document provides comprehensive documentation on the filtering, searching, and ordering capabilities implemented in the Book API. These features enable powerful data retrieval and manipulation through query parameters.

---

## Table of Contents

1. [Filtering](#filtering)
2. [Searching](#searching)
3. [Ordering](#ordering)
4. [Combining Features](#combining-features)
5. [Testing Guide](#testing-guide)
6. [Implementation Details](#implementation-details)

---

## Filtering

### What is Filtering?

Filtering allows you to retrieve only the books that match specific criteria. It uses exact matching on specified fields.

### Available Filter Fields

- `title` - Filter by exact book title
- `author` - Filter by author ID
- `publication_year` - Filter by publication year

### Filtering Syntax

```
GET /api/books/?<field>=<value>
```

### Filtering Examples

#### Filter by Publication Year

```bash
GET /api/books/?publication_year=2023
```

**Returns**: All books published in 2023

**cURL Example**:
```bash
curl "http://localhost:8000/api/books/?publication_year=2023"
```

**Python Example**:
```python
import requests

response = requests.get('http://localhost:8000/api/books/', params={
    'publication_year': 2023
})
books = response.json()
```

#### Filter by Author

```bash
GET /api/books/?author=1
```

**Returns**: All books by author with ID 1

**cURL Example**:
```bash
curl "http://localhost:8000/api/books/?author=1"
```

#### Filter by Title

```bash
GET /api/books/?title=Django for Beginners
```

**Note**: URL encode spaces as `%20`
```bash
GET /api/books/?title=Django%20for%20Beginners
```

**cURL Example**:
```bash
curl "http://localhost:8000/api/books/?title=Django%20for%20Beginners"
```

#### Multiple Filters (AND Logic)

Combine multiple filters to narrow down results:

```bash
GET /api/books/?author=1&publication_year=2023
```

**Returns**: Books by author ID 1 published in 2023

**cURL Example**:
```bash
curl "http://localhost:8000/api/books/?author=1&publication_year=2023"
```

**Python Example**:
```python
response = requests.get('http://localhost:8000/api/books/', params={
    'author': 1,
    'publication_year': 2023
})
```

---

## Searching

### What is Searching?

Searching allows you to perform text-based searches across multiple fields. Unlike filtering (exact match), searching uses partial matching and is case-insensitive.

### Searchable Fields

- `title` - Book title
- `author__name` - Author's name (follows relationship)

### Searching Syntax

```
GET /api/books/?search=<query>
```

### Search Characteristics

- **Case-insensitive**: "django" matches "Django", "DJANGO", etc.
- **Partial matching**: "Djan" matches "Django for Beginners"
- **Multi-field**: Searches both title and author name simultaneously

### Search Examples

#### Basic Search

```bash
GET /api/books/?search=Django
```

**Returns**: All books with "Django" in title OR author name

**cURL Example**:
```bash
curl "http://localhost:8000/api/books/?search=Django"
```

**Python Example**:
```python
response = requests.get('http://localhost:8000/api/books/', params={
    'search': 'Django'
})
```

#### Search by Author Name

```bash
GET /api/books/?search=Smith
```

**Returns**: Books with "Smith" in title or author name

#### Partial Match Search

```bash
GET /api/books/?search=Pyth
```

**Returns**: Matches "Python", "Python3", "Pythonic", etc.

---

## Ordering

### What is Ordering?

Ordering allows you to sort the results by specified fields in ascending or descending order.

### Available Ordering Fields

- `title` - Sort alphabetically by title
- `publication_year` - Sort chronologically by year

### Ordering Syntax

```
GET /api/books/?ordering=<field>        # Ascending
GET /api/books/?ordering=-<field>       # Descending (prefix with -)
```

### Default Ordering

If no ordering is specified, books are sorted by `title` in ascending order.

### Ordering Examples

#### Order by Title (A-Z)

```bash
GET /api/books/?ordering=title
```

**Returns**: Books sorted alphabetically by title

**cURL Example**:
```bash
curl "http://localhost:8000/api/books/?ordering=title"
```

#### Order by Title (Z-A)

```bash
GET /api/books/?ordering=-title
```

**Returns**: Books sorted reverse alphabetically

#### Order by Publication Year (Oldest First)

```bash
GET /api/books/?ordering=publication_year
```

**Returns**: Books sorted by year, oldest to newest

**cURL Example**:
```bash
curl "http://localhost:8000/api/books/?ordering=publication_year"
```

#### Order by Publication Year (Newest First)

```bash
GET /api/books/?ordering=-publication_year
```

**Returns**: Books sorted by year, newest to oldest

**Python Example**:
```python
response = requests.get('http://localhost:8000/api/books/', params={
    'ordering': '-publication_year'
})
```

#### Multiple Ordering Fields

Sort by multiple fields (applied in order):

```bash
GET /api/books/?ordering=publication_year,title
```

**Returns**: Books sorted by year, then by title within each year

**cURL Example**:
```bash
curl "http://localhost:8000/api/books/?ordering=publication_year,title"
```

---

## Combining Features

The real power comes from combining filtering, searching, and ordering together!

### Example 1: Filter + Order

Find all books from 2023, sorted by title:

```bash
GET /api/books/?publication_year=2023&ordering=title
```

**cURL**:
```bash
curl "http://localhost:8000/api/books/?publication_year=2023&ordering=title"
```

**Python**:
```python
response = requests.get('http://localhost:8000/api/books/', params={
    'publication_year': 2023,
    'ordering': 'title'
})
```

### Example 2: Search + Order

Search for Django books, show newest first:

```bash
GET /api/books/?search=Django&ordering=-publication_year
```

**cURL**:
```bash
curl "http://localhost:8000/api/books/?search=Django&ordering=-publication_year"
```

### Example 3: Filter + Search + Order

Books by author 1, containing "Python", newest first:

```bash
GET /api/books/?author=1&search=Python&ordering=-publication_year
```

**cURL**:
```bash
curl "http://localhost:8000/api/books/?author=1&search=Python&ordering=-publication_year"
```

**Python**:
```python
response = requests.get('http://localhost:8000/api/books/', params={
    'author': 1,
    'search': 'Python',
    'ordering': '-publication_year'
})
```

### Example 4: Multiple Filters + Order

Books from 2022-2023, sorted by title:

```bash
# Note: Multiple values for same parameter (requires custom implementation)
# Current setup: Use separate requests or implement custom FilterSet
```

---

## Testing Guide

### Using cURL

#### Test 1: Basic Filtering

```bash
# Windows PowerShell
curl "http://localhost:8000/api/books/?publication_year=2023"

# Windows Command Prompt
curl "http://localhost:8000/api/books/?publication_year=2023"
```

#### Test 2: Search Functionality

```bash
curl "http://localhost:8000/api/books/?search=Django"
```

#### Test 3: Ordering

```bash
curl "http://localhost:8000/api/books/?ordering=-publication_year"
```

#### Test 4: Combined Query

```bash
curl "http://localhost:8000/api/books/?author=1&search=Python&ordering=title"
```

### Using Postman

1. **Setup**:
   - Open Postman
   - Create new GET request to `http://localhost:8000/api/books/`

2. **Test Filtering**:
   - Go to "Params" tab
   - Add key: `publication_year`, value: `2023`
   - Send request

3. **Test Searching**:
   - Clear previous params
   - Add key: `search`, value: `Django`
   - Send request

4. **Test Ordering**:
   - Add key: `ordering`, value: `-publication_year`
   - Send request

5. **Test Combined**:
   - Add multiple parameters:
     - `author`: `1`
     - `search`: `Python`
     - `ordering`: `-publication_year`
   - Send request

### Using Python Requests

Create a test script `test_api_queries.py`:

```python
import requests

BASE_URL = 'http://localhost:8000/api/books/'

def test_filtering():
    """Test filtering by publication year"""
    print("Testing Filtering...")
    response = requests.get(BASE_URL, params={'publication_year': 2023})
    print(f"Status Code: {response.status_code}")
    print(f"Results: {len(response.json()['results'])} books")
    print()

def test_searching():
    """Test search functionality"""
    print("Testing Searching...")
    response = requests.get(BASE_URL, params={'search': 'Django'})
    print(f"Status Code: {response.status_code}")
    print(f"Results: {len(response.json()['results'])} books")
    print()

def test_ordering():
    """Test ordering by publication year"""
    print("Testing Ordering...")
    response = requests.get(BASE_URL, params={'ordering': '-publication_year'})
    print(f"Status Code: {response.status_code}")
    books = response.json()['results']
    print(f"Results: {len(books)} books")
    if books:
        print(f"First book: {books[0]['title']} ({books[0]['publication_year']})")
    print()

def test_combined():
    """Test combining filter, search, and order"""
    print("Testing Combined Query...")
    params = {
        'author': 1,
        'search': 'Python',
        'ordering': '-publication_year'
    }
    response = requests.get(BASE_URL, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Results: {len(response.json()['results'])} books")
    print()

def test_pagination():
    """Test pagination with queries"""
    print("Testing Pagination...")
    response = requests.get(BASE_URL, params={'ordering': 'title', 'page': 1})
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Total Count: {data.get('count', 'N/A')}")
    print(f"Next Page: {data.get('next', 'None')}")
    print(f"Previous Page: {data.get('previous', 'None')}")
    print()

if __name__ == '__main__':
    print("=== API Query Capabilities Test Suite ===\n")
    
    test_filtering()
    test_searching()
    test_ordering()
    test_combined()
    test_pagination()
    
    print("=== All Tests Complete ===")
```

Run the test script:
```bash
python test_api_queries.py
```

### Using Browser (DRF Browsable API)

1. Navigate to `http://localhost:8000/api/books/`
2. Use the "Filters" button in the browsable API
3. Or manually add query parameters to the URL:
   - `http://localhost:8000/api/books/?publication_year=2023`
   - `http://localhost:8000/api/books/?search=Django&ordering=-publication_year`

---

## Implementation Details

### Technology Stack

- **Django REST Framework**: Core API framework
- **django-filter**: Advanced filtering capabilities
- **DRF SearchFilter**: Text-based searching
- **DRF OrderingFilter**: Result ordering

### Backend Configuration

#### 1. Settings Configuration (`settings.py`)

```python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'django_filters',  # Required for DjangoFilterBackend
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

#### 2. View Configuration (`views.py`)

```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Enable all three filter backends
    filter_backends = [
        DjangoFilterBackend,    # Exact match filtering
        filters.SearchFilter,    # Text search
        filters.OrderingFilter,  # Result ordering
    ]
    
    # Configure filtering fields
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Configure searchable fields
    search_fields = ['title', 'author__name']
    
    # Configure orderable fields
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering
```

### Filter Backend Details

#### DjangoFilterBackend

- Provides exact match filtering
- Uses `filterset_fields` attribute
- Generates query parameters automatically
- Supports related fields (e.g., `author__name`)

#### SearchFilter

- Provides text-based searching
- Uses `search_fields` attribute
- Case-insensitive partial matching
- Searches across multiple fields with OR logic
- Query parameter: `?search=<query>`

#### OrderingFilter

- Provides result ordering
- Uses `ordering_fields` attribute
- Supports ascending (default) and descending (prefix `-`)
- Supports multiple field ordering
- Query parameter: `?ordering=<field>`
- Default ordering: `ordering` attribute

### Query Execution Flow

1. **Request arrives** with query parameters
2. **DjangoFilterBackend** applies exact match filters
3. **SearchFilter** applies text search across specified fields
4. **OrderingFilter** sorts the filtered results
5. **Pagination** divides results into pages
6. **Serializer** converts queryset to JSON
7. **Response** returned to client

### Performance Considerations

1. **Database Indexing**: 
   - Add indexes to frequently filtered fields
   - Index `publication_year` for better filter performance
   - Consider composite indexes for common filter combinations

2. **Query Optimization**:
   - Use `select_related()` for foreign key relationships
   - Minimize database queries with proper prefetching

3. **Caching**:
   - Cache frequently accessed filter combinations
   - Use Redis for common queries

### Advanced Customization

#### Custom FilterSet

For more complex filtering (e.g., range filters, custom logic):

```python
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    # Range filter for publication year
    year_min = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    year_max = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    
    # Case-insensitive contains for title
    title_contains = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    
    class Meta:
        model = Book
        fields = ['author']

class BookListView(generics.ListAPIView):
    filterset_class = BookFilter  # Use custom FilterSet
```

Usage:
```bash
GET /api/books/?year_min=2020&year_max=2023
GET /api/books/?title_contains=django
```

---

## Troubleshooting

### Issue: Filtering not working

**Solution**: 
- Verify `django_filters` is installed: `pip install django-filter`
- Check `django_filters` is in `INSTALLED_APPS`
- Ensure `DjangoFilterBackend` is in `filter_backends`

### Issue: Search returns no results

**Solution**:
- Check `search_fields` are correct
- Verify field names match model fields
- For related fields, use double underscore: `author__name`

### Issue: Ordering not applied

**Solution**:
- Check field name is in `ordering_fields`
- Verify spelling of query parameter: `?ordering=title`
- Use `-` prefix for descending: `?ordering=-title`

### Issue: Query parameters ignored

**Solution**:
- Check URL encoding (spaces should be `%20`)
- Verify parameter names match configuration
- Check for typos in field names

---

## Best Practices

1. **Always test with real data**: Use diverse datasets for testing
2. **Document available filters**: Keep API documentation updated
3. **Use pagination**: Essential for large datasets
4. **Add database indexes**: Improve filter performance
5. **Validate inputs**: Ensure type safety for filter values
6. **Monitor performance**: Track slow queries and optimize
7. **Use consistent naming**: Keep parameter names intuitive

---

## Next Steps

### Enhancements to Consider

1. **Advanced Filtering**:
   - Range filters (year between X and Y)
   - Multiple value filters (author in [1, 2, 3])
   - Date range filtering

2. **Custom Search**:
   - Weighted search results
   - Full-text search with PostgreSQL
   - Fuzzy matching

3. **Performance**:
   - Add database indexes
   - Implement caching
   - Query optimization

4. **User Experience**:
   - Auto-complete for search
   - Filter suggestions
   - Saved searches

---

## References

- [Django REST Framework Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
- [django-filter Documentation](https://django-filter.readthedocs.io/)
- [DRF SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)
- [DRF OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)

---

**Last Updated**: December 7, 2025  
**Version**: 1.0  
**Author**: Development Team
