# Create Operation

## Command:
```python
from bookshelf.models import Book

# Create a Book instance with title "1984", author "George Orwell", and publication year 1949
book = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)

# Display the created book
print(f'Book created: ID={book.id}, Title={book.title}, Author={book.author}, Year={book.publication_year}')
```

## Output:
```
Book created: ID=1, Title=1984, Author=George Orwell, Year=1949
```

## Description:
Successfully created a Book instance with:
- **Title**: 1984
- **Author**: George Orwell
- **Publication Year**: 1949
- **ID**: 1 (auto-generated primary key)

The `Book.objects.create()` method creates a new book record in the database and returns the created instance.
