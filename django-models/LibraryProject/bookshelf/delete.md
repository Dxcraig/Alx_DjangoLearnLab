# Delete Operation

## Command:
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

## Output:
```
Book deleted successfully
Total books remaining: 0
All books: []
```

## Description:
Successfully deleted the book with ID 1 from the database using `book.delete()`. The deletion is confirmed by:
1. The success message: "Book deleted successfully"
2. Querying all books using `Book.objects.all()` which returns an empty QuerySet
3. The count of remaining books is 0
4. The list of all books is empty: `[]`

The `delete()` method permanently removes the book record from the database.
