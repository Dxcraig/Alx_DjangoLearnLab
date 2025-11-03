# Update Operation

## Command:
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

## Output:
```
Before Update: 1984
After Update: Nineteen Eighty-Four
```

## Description:
Successfully updated the book's title from "1984" to "Nineteen Eighty-Four". The process involves:
1. Retrieving the book instance using `Book.objects.get(id=1)`
2. Modifying the `title` attribute
3. Calling `book.save()` to persist the changes to the database

The output confirms that the title was successfully changed from "1984" to "Nineteen Eighty-Four".
