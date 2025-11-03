# Retrieve Operation

## Command:
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

## Output:
```
Retrieved Book:
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```

## Description:
Successfully retrieved the book with ID 1 from the database using `Book.objects.get(id=1)`. The method returns a single Book instance matching the given criteria. All attributes of the book are displayed:
- **ID**: 1
- **Title**: 1984
- **Author**: George Orwell
- **Publication Year**: 1949
