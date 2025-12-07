# Testing Documentation - Book API

## Overview

This document provides comprehensive documentation for the unit tests implemented for the Book API. The tests ensure the integrity, correctness, and security of all API endpoints.

---

## Table of Contents

1. [Testing Strategy](#testing-strategy)
2. [Test Coverage](#test-coverage)
3. [Running Tests](#running-tests)
4. [Test Cases](#test-cases)
5. [Interpreting Results](#interpreting-results)
6. [Continuous Integration](#continuous-integration)
7. [Best Practices](#best-practices)

---

## Testing Strategy

### Approach

Our testing strategy follows a comprehensive approach to ensure API reliability:

1. **Unit Testing**: Each endpoint is tested independently
2. **Integration Testing**: Query parameters and features are tested in combination
3. **Permission Testing**: Authentication and authorization are verified
4. **Edge Case Testing**: Boundary conditions and error scenarios are covered
5. **Data Integrity Testing**: Database operations are validated

### Testing Framework

- **Framework**: Django's built-in test framework (based on Python's `unittest`)
- **API Testing**: Django REST Framework's `APITestCase`
- **Client**: `APIClient` for simulating HTTP requests
- **Database**: Separate test database (automatically created and destroyed)

### Test Database

- Tests use a separate SQLite database (`test_db.sqlite3`)
- Database is created before tests run
- Database is destroyed after tests complete
- No impact on development or production data

---

## Test Coverage

### Endpoints Covered

| Endpoint | Methods | Test Coverage |
|----------|---------|---------------|
| `/api/books/` | GET | ✓ List, Filter, Search, Order |
| `/api/books/<pk>/` | GET | ✓ Retrieve single book |
| `/api/books/create/` | POST | ✓ Create with validation |
| `/api/books/update/` | PUT, PATCH | ✓ Full and partial updates |
| `/api/books/delete/` | DELETE | ✓ Delete operations |

### Feature Coverage

#### CRUD Operations
- ✓ Create books with valid data
- ✓ Read single and multiple books
- ✓ Update books (full and partial)
- ✓ Delete books
- ✓ Handle non-existent resources

#### Filtering
- ✓ Filter by publication_year
- ✓ Filter by author
- ✓ Filter by title
- ✓ Combine multiple filters
- ✓ Handle empty results

#### Searching
- ✓ Search by title
- ✓ Search by author name
- ✓ Case-insensitive search
- ✓ Partial match search
- ✓ Handle no results

#### Ordering
- ✓ Order by title (ascending/descending)
- ✓ Order by publication_year (ascending/descending)
- ✓ Default ordering
- ✓ Verify sort correctness

#### Permissions & Authentication
- ✓ Unauthenticated read access (list/detail)
- ✓ Authenticated write access (create/update/delete)
- ✓ Reject unauthenticated write attempts
- ✓ IsAuthenticatedOrReadOnly enforcement
- ✓ IsAuthenticated enforcement

#### Data Validation
- ✓ Required fields validation
- ✓ Publication year validation (no future dates)
- ✓ Author foreign key validation
- ✓ Field type validation
- ✓ Maximum length validation

#### Edge Cases
- ✓ Empty database
- ✓ Invalid data types
- ✓ Non-existent resources
- ✓ Special characters
- ✓ SQL injection prevention
- ✓ Long strings

---

## Running Tests

### Run All Tests

```bash
# Run all tests in the project
python manage.py test

# Run only API tests
python manage.py test api

# Run specific test file
python manage.py test api.test_views

# Run specific test class
python manage.py test api.test_views.BookAPITestCase

# Run specific test method
python manage.py test api.test_views.BookAPITestCase.test_list_books_authenticated
```

### Run with Verbosity

```bash
# Minimal output
python manage.py test api --verbosity=0

# Normal output (default)
python manage.py test api --verbosity=1

# Detailed output
python manage.py test api --verbosity=2

# Very detailed output
python manage.py test api --verbosity=3
```

### Run Tests in Parallel

```bash
# Use multiple processes to speed up tests
python manage.py test api --parallel

# Specify number of processes
python manage.py test api --parallel=4
```

### Keep Test Database

```bash
# Keep test database after tests (for debugging)
python manage.py test api --keepdb
```

### Fast Tests (Skip Migrations)

```bash
# Skip running migrations (faster, but may cause issues)
python manage.py test api --keepdb --parallel
```

---

## Test Cases

### Test Class: BookAPITestCase

Main test suite covering all core functionality.

#### List View Tests

**test_list_books_unauthenticated**
- **Purpose**: Verify unauthenticated users can list books
- **Expected**: 200 OK with paginated results
- **Validates**: Read-only access for public users

**test_list_books_authenticated**
- **Purpose**: Verify authenticated users can list books
- **Expected**: 200 OK with paginated results
- **Validates**: Authenticated access works

**test_list_books_pagination**
- **Purpose**: Verify pagination works correctly
- **Expected**: Response includes count, next, previous, results
- **Validates**: Pagination metadata present

#### Filtering Tests

**test_filter_by_publication_year**
- **Purpose**: Test filtering by publication year
- **Method**: GET /api/books/?publication_year=2023
- **Expected**: Only books from 2023
- **Validates**: Exact match filtering

**test_filter_by_author**
- **Purpose**: Test filtering by author ID
- **Method**: GET /api/books/?author=1
- **Expected**: Only books by author ID 1
- **Validates**: Foreign key filtering

**test_filter_by_title**
- **Purpose**: Test filtering by exact title
- **Method**: GET /api/books/?title=Django%20for%20APIs
- **Expected**: Only matching book
- **Validates**: String field filtering

**test_filter_multiple_criteria**
- **Purpose**: Test combining multiple filters
- **Method**: GET /api/books/?author=1&publication_year=2023
- **Expected**: Books matching all criteria
- **Validates**: AND logic for multiple filters

**test_filter_no_results**
- **Purpose**: Test filtering with no matches
- **Method**: GET /api/books/?publication_year=2030
- **Expected**: Empty results list
- **Validates**: Graceful handling of no results

#### Searching Tests

**test_search_by_title**
- **Purpose**: Test text search in title field
- **Method**: GET /api/books/?search=Django
- **Expected**: Books with "Django" in title
- **Validates**: Partial match in title

**test_search_by_author_name**
- **Purpose**: Test search across related field
- **Method**: GET /api/books/?search=Vincent
- **Expected**: Books by authors named Vincent
- **Validates**: Related field search

**test_search_case_insensitive**
- **Purpose**: Verify search ignores case
- **Method**: GET /api/books/?search=python (vs PYTHON vs Python)
- **Expected**: Same results regardless of case
- **Validates**: Case-insensitive matching

**test_search_partial_match**
- **Purpose**: Test partial word matching
- **Method**: GET /api/books/?search=Djan
- **Expected**: Matches "Django"
- **Validates**: Substring matching

**test_search_no_results**
- **Purpose**: Test search with no matches
- **Method**: GET /api/books/?search=NonexistentBook
- **Expected**: Empty results
- **Validates**: Graceful handling

#### Ordering Tests

**test_ordering_by_title_ascending**
- **Purpose**: Test alphabetical ordering
- **Method**: GET /api/books/?ordering=title
- **Expected**: Books sorted A-Z
- **Validates**: Ascending sort

**test_ordering_by_title_descending**
- **Purpose**: Test reverse alphabetical ordering
- **Method**: GET /api/books/?ordering=-title
- **Expected**: Books sorted Z-A
- **Validates**: Descending sort

**test_ordering_by_year_ascending**
- **Purpose**: Test chronological ordering
- **Method**: GET /api/books/?ordering=publication_year
- **Expected**: Oldest to newest
- **Validates**: Numeric ascending sort

**test_ordering_by_year_descending**
- **Purpose**: Test reverse chronological ordering
- **Method**: GET /api/books/?ordering=-publication_year
- **Expected**: Newest to oldest
- **Validates**: Numeric descending sort

**test_default_ordering**
- **Purpose**: Verify default ordering
- **Method**: GET /api/books/
- **Expected**: Sorted by title (default)
- **Validates**: Default behavior

#### Combined Query Tests

**test_filter_and_search**
- **Purpose**: Test filter + search combination
- **Method**: GET /api/books/?author=1&search=Django
- **Expected**: Books by author 1 containing "Django"
- **Validates**: Multiple features work together

**test_search_and_ordering**
- **Purpose**: Test search + ordering combination
- **Method**: GET /api/books/?search=Django&ordering=-publication_year
- **Expected**: Django books, newest first
- **Validates**: Search results can be ordered

**test_filter_search_and_ordering**
- **Purpose**: Test all three features together
- **Method**: GET /api/books/?author=1&search=Django&ordering=title
- **Expected**: Filtered, searched, and ordered results
- **Validates**: Complex queries work correctly

#### Detail View Tests

**test_retrieve_book_unauthenticated**
- **Purpose**: Test retrieving single book without auth
- **Method**: GET /api/books/1/
- **Expected**: 200 OK with book details
- **Validates**: Public read access

**test_retrieve_book_authenticated**
- **Purpose**: Test retrieving single book with auth
- **Method**: GET /api/books/1/ (authenticated)
- **Expected**: 200 OK with book details
- **Validates**: Authenticated access works

**test_retrieve_nonexistent_book**
- **Purpose**: Test retrieving non-existent book
- **Method**: GET /api/books/99999/
- **Expected**: 404 Not Found
- **Validates**: Proper error handling

#### Create View Tests

**test_create_book_authenticated**
- **Purpose**: Test creating book with authentication
- **Method**: POST /api/books/create/ (authenticated)
- **Data**: Valid book data
- **Expected**: 201 Created, book in database
- **Validates**: Successful creation

**test_create_book_unauthenticated**
- **Purpose**: Test creating book without authentication
- **Method**: POST /api/books/create/ (unauthenticated)
- **Expected**: 401 or 403
- **Validates**: Authentication required

**test_create_book_missing_fields**
- **Purpose**: Test creation with incomplete data
- **Method**: POST with missing required fields
- **Expected**: 400 Bad Request
- **Validates**: Field validation

**test_create_book_invalid_year**
- **Purpose**: Test creation with future year
- **Method**: POST with publication_year=2030
- **Expected**: 400 Bad Request
- **Validates**: Custom validation (no future dates)

**test_create_book_invalid_author**
- **Purpose**: Test creation with invalid author ID
- **Method**: POST with non-existent author
- **Expected**: 400 Bad Request
- **Validates**: Foreign key validation

#### Update View Tests

**test_update_book_authenticated**
- **Purpose**: Test full update with authentication
- **Method**: PUT /api/books/update/ (authenticated)
- **Expected**: 200 OK, book updated in database
- **Validates**: Full update works

**test_partial_update_book_authenticated**
- **Purpose**: Test partial update with authentication
- **Method**: PATCH /api/books/update/ (authenticated)
- **Expected**: 200 OK, specified fields updated
- **Validates**: Partial update works

**test_update_book_unauthenticated**
- **Purpose**: Test update without authentication
- **Method**: PUT /api/books/update/ (unauthenticated)
- **Expected**: 401 or 403
- **Validates**: Authentication required

**test_update_nonexistent_book**
- **Purpose**: Test updating non-existent book
- **Method**: PUT with invalid book ID
- **Expected**: 404 Not Found
- **Validates**: Error handling

**test_update_book_invalid_data**
- **Purpose**: Test update with invalid data
- **Method**: PUT with future year
- **Expected**: 400 Bad Request
- **Validates**: Validation on updates

#### Delete View Tests

**test_delete_book_authenticated**
- **Purpose**: Test deleting book with authentication
- **Method**: DELETE /api/books/delete/ (authenticated)
- **Expected**: 204 No Content, book removed
- **Validates**: Successful deletion

**test_delete_book_unauthenticated**
- **Purpose**: Test deleting without authentication
- **Method**: DELETE /api/books/delete/ (unauthenticated)
- **Expected**: 401 or 403
- **Validates**: Authentication required

**test_delete_nonexistent_book**
- **Purpose**: Test deleting non-existent book
- **Method**: DELETE with invalid ID
- **Expected**: 404 Not Found
- **Validates**: Error handling

#### Permission Tests

**test_list_view_allows_unauthenticated_read**
- **Purpose**: Verify public read access
- **Validates**: IsAuthenticatedOrReadOnly on list view

**test_detail_view_allows_unauthenticated_read**
- **Purpose**: Verify public detail access
- **Validates**: IsAuthenticatedOrReadOnly on detail view

**test_create_view_requires_authentication**
- **Purpose**: Verify auth required for creation
- **Validates**: IsAuthenticated on create view

**test_update_view_requires_authentication**
- **Purpose**: Verify auth required for updates
- **Validates**: IsAuthenticated on update view

**test_delete_view_requires_authentication**
- **Purpose**: Verify auth required for deletion
- **Validates**: IsAuthenticated on delete view

#### Data Integrity Tests

**test_book_data_structure**
- **Purpose**: Verify response structure
- **Expected**: All required fields present
- **Validates**: Serializer output format

**test_serializer_validation**
- **Purpose**: Test serializer validation
- **Expected**: Invalid data rejected
- **Validates**: Type validation

**test_database_integrity_after_operations**
- **Purpose**: Verify database state consistency
- **Expected**: Counts match expectations
- **Validates**: No orphaned or missing data

### Test Class: BookAPIEdgeCaseTestCase

Edge case and error condition tests.

**test_empty_database_list**
- **Purpose**: Test with no data
- **Expected**: Empty results, no errors
- **Validates**: Graceful handling of empty state

**test_very_long_title**
- **Purpose**: Test max length validation
- **Expected**: 400 Bad Request
- **Validates**: Length constraints

**test_special_characters_in_search**
- **Purpose**: Test special character handling
- **Expected**: No errors
- **Validates**: Input sanitization

**test_sql_injection_attempt**
- **Purpose**: Test security against SQL injection
- **Expected**: No errors, no data breach
- **Validates**: Query parameterization

---

## Interpreting Results

### Successful Test Run

```
System check identified no issues (0 silenced).
..........................................................
----------------------------------------------------------------------
Ran 54 tests in 2.345s

OK
```

**Interpretation**: All tests passed successfully!

### Failed Test

```
FAIL: test_create_book_authenticated (api.test_views.BookAPITestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  ...
AssertionError: 201 != 400

----------------------------------------------------------------------
Ran 54 tests in 2.345s

FAILED (failures=1)
```

**Interpretation**: 
- 53 tests passed, 1 failed
- The create endpoint returned 400 instead of expected 201
- Review the code and fix the issue
- Re-run tests to verify fix

### Error in Test

```
ERROR: test_list_books_authenticated (api.test_views.BookAPITestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  ...
AttributeError: 'NoneType' object has no attribute 'id'

----------------------------------------------------------------------
Ran 54 tests in 2.345s

FAILED (errors=1)
```

**Interpretation**:
- Test encountered an unexpected error (not a failed assertion)
- Issue is likely in test setup or code logic
- Review traceback to identify root cause

### Verbose Output

```bash
python manage.py test api --verbosity=2
```

```
test_create_book_authenticated (api.test_views.BookAPITestCase)
Test creating a book with authentication. ... ok
test_delete_book_authenticated (api.test_views.BookAPITestCase)
Test deleting a book with authentication. ... ok
...
```

**Interpretation**: Shows each test name as it runs

---

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: Django Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test api
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Running tests before commit..."
python manage.py test api --verbosity=0

if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## Best Practices

### 1. Test Isolation

- Each test is independent
- setUp() creates fresh data for each test
- tearDown() cleans up after each test
- No tests depend on others

### 2. Descriptive Names

- Test names clearly describe what they test
- Follow pattern: `test_<feature>_<scenario>`
- Example: `test_create_book_unauthenticated`

### 3. Comprehensive Coverage

- Test happy paths (expected behavior)
- Test error paths (invalid input, edge cases)
- Test permissions and security
- Test all HTTP methods

### 4. Readable Assertions

```python
# Good: Clear assertion messages
self.assertEqual(response.status_code, status.HTTP_200_OK)
self.assertEqual(len(results), 2)

# Even better: Add custom messages
self.assertEqual(
    response.status_code, 
    status.HTTP_200_OK,
    "Unauthenticated users should be able to list books"
)
```

### 5. DRY Principle

- Use setUp() for common test data
- Extract repeated logic into helper methods
- Use class-level constants for URLs

### 6. Test Data Management

- Create minimal data needed for each test
- Use factories for complex object creation
- Keep test data realistic but simple

### 7. Test Coverage Tools

Install coverage:
```bash
pip install coverage
```

Run with coverage:
```bash
coverage run --source='.' manage.py test api
coverage report
coverage html  # Generates HTML report
```

View coverage report:
```bash
open htmlcov/index.html
```

### 8. Continuous Testing

- Run tests before committing
- Use CI/CD to run tests automatically
- Block merges if tests fail
- Monitor test execution time

---

## Troubleshooting

### Common Issues

**Issue**: Tests fail with "Table doesn't exist"
**Solution**: Run migrations in test environment or use `--keepdb`

**Issue**: Tests are very slow
**Solution**: Use `--parallel` flag or optimize database queries

**Issue**: Random test failures
**Solution**: Check for test isolation issues, ensure no shared state

**Issue**: Authentication tests fail
**Solution**: Verify test user is created in setUp(), check credentials

---

## Maintenance

### Adding New Tests

When adding new features:

1. Write tests first (TDD approach)
2. Run tests to see them fail
3. Implement feature
4. Run tests to see them pass
5. Refactor if needed

### Updating Existing Tests

When modifying features:

1. Update tests to reflect new behavior
2. Ensure all tests still pass
3. Add new tests for new edge cases
4. Remove obsolete tests

### Test Review Checklist

- [ ] All CRUD operations tested
- [ ] All query parameters tested
- [ ] All permissions tested
- [ ] Error cases covered
- [ ] Edge cases covered
- [ ] Test names are descriptive
- [ ] Tests are isolated
- [ ] No hardcoded values
- [ ] Documentation updated

---

## Summary

The test suite provides comprehensive coverage of the Book API including:

- **54 test cases** covering all major functionality
- **CRUD operations** fully tested
- **Filtering, searching, ordering** validated
- **Permissions and authentication** enforced
- **Edge cases and security** considerations
- **Data integrity** maintained

Run tests regularly to ensure API reliability and catch regressions early!

---

**Last Updated**: December 7, 2025  
**Version**: 1.0  
**Test Coverage**: 54 test cases
