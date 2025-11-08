"""
Django ORM Query Samples for Relationship Models

This script demonstrates various query operations on the relationship_app models:
- Author
- Book
- Library
- Librarian

To run this script, use Django shell:
    python manage.py shell < relationship_app/query_samples.py

Or import in Django shell:
    python manage.py shell
    >>> exec(open('relationship_app/query_samples.py').read())
"""

from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """
    Query all books by a specific author.
    
    Args:
        author_name (str): The name of the author
    
    Returns:
        QuerySet: All books written by the specified author
    """
    try:
        # Get the author object
        author = Author.objects.get(name=author_name)
        
        # Query all books by this author using the reverse relationship
        books = Book.objects.filter(author=author)
        
        print(f"\n{'='*60}")
        print(f"Books by {author_name}:")
        print(f"{'='*60}")
        
        if books.exists():
            for book in books:
                print(f"  - {book.title}")
        else:
            print(f"  No books found for author: {author_name}")
        
        return books
    
    except Author.DoesNotExist:
        print(f"\n  Error: Author '{author_name}' not found in database.")
        return None


def list_books_in_library(library_name):
    """
    List all books in a library.
    
    Args:
        library_name (str): The name of the library
    
    Returns:
        QuerySet: All books in the specified library
    """
    try:
        # Get the library object
        library = Library.objects.get(name=library_name)
        
        # Query all books in this library using the ManyToMany relationship
        books = library.books.all()
        
        print(f"\n{'='*60}")
        print(f"Books in {library_name}:")
        print(f"{'='*60}")
        
        if books.exists():
            for book in books:
                print(f"  - {book.title} by {book.author.name}")
        else:
            print(f"  No books found in library: {library_name}")
        
        return books
    
    except Library.DoesNotExist:
        print(f"\n  Error: Library '{library_name}' not found in database.")
        return None


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    
    Args:
        library_name (str): The name of the library
    
    Returns:
        Librarian: The librarian managing the specified library
    """
    try:
        # Get the library object
        library = Library.objects.get(name=library_name)
        
        # Retrieve the librarian using the reverse OneToOne relationship
        librarian = Librarian.objects.get(library=library)
        
        print(f"\n{'='*60}")
        print(f"Librarian for {library_name}:")
        print(f"{'='*60}")
        print(f"  {librarian.name}")
        
        return librarian
    
    except Library.DoesNotExist:
        print(f"\n  Error: Library '{library_name}' not found in database.")
        return None
    
    except Librarian.DoesNotExist:
        print(f"\n  Error: No librarian assigned to library: {library_name}")
        return None


# Example usage and demonstrations
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Django ORM Relationship Query Samples")
    print("="*60)
    
    # Sample data creation (for demonstration purposes)
    print("\nCreating sample data...")
    
    # Create authors
    author1, _ = Author.objects.get_or_create(name="George Orwell")
    author2, _ = Author.objects.get_or_create(name="J.K. Rowling")
    author3, _ = Author.objects.get_or_create(name="Harper Lee")
    
    # Create books
    book1, _ = Book.objects.get_or_create(title="1984", author=author1)
    book2, _ = Book.objects.get_or_create(title="Animal Farm", author=author1)
    book3, _ = Book.objects.get_or_create(title="Harry Potter and the Philosopher's Stone", author=author2)
    book4, _ = Book.objects.get_or_create(title="To Kill a Mockingbird", author=author3)
    
    # Create libraries
    library1, _ = Library.objects.get_or_create(name="Central Library")
    library2, _ = Library.objects.get_or_create(name="City Library")
    
    # Add books to libraries (ManyToMany relationship)
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4)
    
    # Create librarians
    librarian1, _ = Librarian.objects.get_or_create(name="Alice Johnson", library=library1)
    librarian2, _ = Librarian.objects.get_or_create(name="Bob Smith", library=library2)
    
    print("Sample data created successfully!")
    
    # Demonstrate queries
    print("\n" + "="*60)
    print("RUNNING QUERY DEMONSTRATIONS")
    print("="*60)
    
    # Query 1: All books by a specific author
    query_books_by_author("George Orwell")
    query_books_by_author("J.K. Rowling")
    
    # Query 2: List all books in a library
    list_books_in_library("Central Library")
    list_books_in_library("City Library")
    
    # Query 3: Retrieve the librarian for a library
    retrieve_librarian_for_library("Central Library")
    retrieve_librarian_for_library("City Library")
    
    print("\n" + "="*60)
    print("Query demonstrations completed!")
    print("="*60 + "\n")
