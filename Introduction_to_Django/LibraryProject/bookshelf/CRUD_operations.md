# CRUD Operations Documentation

This document contains all CRUD (Create, Read, Update, Delete) operations performed on the Book model in the Django shell.

---

## 1. CREATE Operation

### Command:
```python
from bookshelf.models import Book

# Create a Book instance with title "1984", author "George Orwell", and publication year 1949
book = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)

# Display the created book
print(f'Book created: ID={book.id}, Title={book.title}, Author={book.author}, Year={book.publication_year}')
```

### Output:
```
Book created: ID=1, Title=1984, Author=George Orwell, Year=1949
```

### Description:
Successfully created a Book instance using `Book.objects.create()` with the following attributes:
- **Title**: 1984
- **Author**: George Orwell
- **Publication Year**: 1949
- **ID**: 1 (auto-generated primary key)

---

## 2. RETRIEVE Operation

### Command:
```python
from bookshelf.models import Book

# Retrieve the book with ID 1
book = Book.objects.get(id=1)

# Display all attributes of the retrieved book
print(f'Retrieved Book:')
print(f'ID: {book.id}')
print(f'Title: {book.title}')
print(f'Author: {book.author}')
print(f'Publication Year: {book.publication_year}')
```

### Output:
```
Retrieved Book:
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```

### Description:
Successfully retrieved the book with ID 1 from the database using `Book.objects.get(id=1)`. All attributes of the book are displayed correctly.

---

## 3. UPDATE Operation

### Command:
```python
from bookshelf.models import Book

# Retrieve the book with ID 1
book = Book.objects.get(id=1)

# Display the title before update
print(f'Before Update: {book.title}')

# Update the title from "1984" to "Nineteen Eighty-Four"
book.title = 'Nineteen Eighty-Four'

# Save the changes to the database
book.save()

# Display the title after update
print(f'After Update: {book.title}')
```

### Output:
```
Before Update: 1984
After Update: Nineteen Eighty-Four
```

### Description:
Successfully updated the book's title from "1984" to "Nineteen Eighty-Four". The process involves retrieving the book, modifying the title attribute, and calling `book.save()` to persist the changes.

---

## 4. DELETE Operation

### Command:
```python
from bookshelf.models import Book

# Retrieve the book with ID 1
book = Book.objects.get(id=1)

# Delete the book from the database
book.delete()
print('Book deleted successfully')

# Confirm deletion by retrieving all books
all_books = Book.objects.all()
print(f'Total books remaining: {all_books.count()}')
print(f'All books: {list(all_books)}')
```

### Output:
```
Book deleted successfully
Total books remaining: 0
All books: []
```

### Description:
Successfully deleted the book with ID 1 using `book.delete()`. The deletion was confirmed by querying all books, which returned an empty QuerySet with a count of 0.

---

## Summary

All CRUD operations were successfully performed on the Book model:
- ✅ **Create**: Created a book titled "1984" by George Orwell (1949)
- ✅ **Retrieve**: Retrieved and displayed all attributes of the created book
- ✅ **Update**: Updated the title from "1984" to "Nineteen Eighty-Four"
- ✅ **Delete**: Deleted the book and confirmed deletion

Each operation demonstrates the Django ORM's capabilities for database interactions without writing raw SQL queries.
