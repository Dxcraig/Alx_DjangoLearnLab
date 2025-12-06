from django.db import models

# Author Model
# Represents an author in the library system.
# This model stores information about authors who have written books.
# Each author can have multiple books associated with them (one-to-many relationship).
class Author(models.Model):
    # The author's full name
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

# Book Model
# Represents a book in the library system.
# This model stores information about individual books including their title,
# publication year, and the author who wrote them.
# Relationship: Each book is written by one author (many-to-one relationship).
class Book(models.Model):
    # The title of the book
    title = models.CharField(max_length=200)
    
    # The year the book was published
    publication_year = models.IntegerField()
    
    # Foreign key relationship to Author model
    # This creates a many-to-one relationship: many books can belong to one author
    # on_delete=models.CASCADE ensures that when an author is deleted,
    # all their associated books are also deleted automatically
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return self.title
