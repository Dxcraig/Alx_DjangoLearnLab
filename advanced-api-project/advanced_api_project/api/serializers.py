from rest_framework import serializers
from .models import Author, Book

# BookSerializer
# Serializes Book model instances to JSON format and vice versa.
# This serializer handles the conversion of Book objects for API responses and requests.
# It includes validation to ensure the publication year is not in the future.
class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        # Include all fields from the Book model (title, publication_year, author)
        fields = '__all__'
    
    # Custom validation method for the Book model
    # Ensures that the publication_year field contains a valid year (not in the future)
    def validate(self, data):
        if data['publication_year'] > 2025:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return data


# AuthorSerializer
# Serializes Author model instances to JSON format and vice versa.
# This serializer demonstrates a nested relationship handling:
# - It includes all books written by the author as a nested representation
# - The 'books' field uses BookSerializer to serialize related Book objects
# 
# Relationship Handling:
# The Author-Book relationship is handled through nested serialization:
# 1. The 'books' field is defined using BookSerializer with many=True,
#    indicating that one author can have multiple books.
# 2. read_only=True means that books are only displayed when retrieving author data,
#    but cannot be created or updated directly through the AuthorSerializer.
# 3. This creates a one-to-many relationship where an author's data includes
#    a list of all their books with complete book details.
# 4. The related_name='books' in the Book model's ForeignKey makes this relationship
#    accessible, allowing the serializer to automatically fetch all books for an author.
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer field that includes all books by this author
    # many=True: indicates this field represents multiple Book instances
    # read_only=True: books can only be read, not created/updated via this serializer
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        # Include both the author's name and their related books
        fields = ['name', 'books']