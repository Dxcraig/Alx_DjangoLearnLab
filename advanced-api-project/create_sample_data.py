"""
Create Sample Data for Testing

This script creates sample books and authors for testing the API
filtering, searching, and ordering capabilities.

Usage:
    python manage.py shell < create_sample_data.py
    
Or run from Django shell:
    exec(open('create_sample_data.py').read())
"""

from api.models import Author, Book

# Clear existing data (optional - comment out to keep existing data)
print("Clearing existing data...")
Book.objects.all().delete()
Author.objects.all().delete()

# Create Authors
print("\nCreating authors...")
author1 = Author.objects.create(name="William Vincent")
author2 = Author.objects.create(name="Eric Matthes")
author3 = Author.objects.create(name="Luciano Ramalho")
author4 = Author.objects.create(name="Mark Lutz")

print(f"Created: {author1.name}")
print(f"Created: {author2.name}")
print(f"Created: {author3.name}")
print(f"Created: {author4.name}")

# Create Books
print("\nCreating books...")

books_data = [
    # Django books by William Vincent
    ("Django for Beginners", 2023, author1),
    ("Django for APIs", 2022, author1),
    ("Django for Professionals", 2023, author1),
    
    # Python books by Eric Matthes
    ("Python Crash Course", 2019, author2),
    ("Python Crash Course - 2nd Edition", 2021, author2),
    ("Python Crash Course - 3rd Edition", 2023, author2),
    
    # Advanced Python by Luciano Ramalho
    ("Fluent Python", 2015, author3),
    ("Fluent Python - 2nd Edition", 2022, author3),
    
    # Python books by Mark Lutz
    ("Learning Python", 2013, author4),
    ("Programming Python", 2011, author4),
    ("Python Pocket Reference", 2014, author4),
]

for title, year, author in books_data:
    book = Book.objects.create(
        title=title,
        publication_year=year,
        author=author
    )
    print(f"Created: {book.title} ({book.publication_year}) by {book.author.name}")

print("\n" + "="*60)
print("Sample data created successfully!")
print("="*60)

# Display summary
total_authors = Author.objects.count()
total_books = Book.objects.count()

print(f"\nTotal Authors: {total_authors}")
print(f"Total Books: {total_books}")

print("\nBooks by Author:")
for author in Author.objects.all():
    book_count = Book.objects.filter(author=author).count()
    print(f"  {author.name}: {book_count} book(s)")

print("\nBooks by Year:")
for year in sorted(set(Book.objects.values_list('publication_year', flat=True))):
    book_count = Book.objects.filter(publication_year=year).count()
    print(f"  {year}: {book_count} book(s)")

print("\n✓ Sample data is ready for testing!")
print("\nYou can now:")
print("  1. Start the development server: python manage.py runserver")
print("  2. Run the test suite: python test_api_queries.py")
print("  3. Visit: http://localhost:8000/api/books/")
