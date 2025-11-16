from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

from .models import Book


@permission_required('bookshelf.can_view', raise_exception=True)
def view_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return HttpResponse(f"Bookshelf: Viewing book: {book.title}")


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    # Minimal demo: use GET params ?title=...&author=...&publication_year=...
    title = request.GET.get('title', 'Untitled')
    author = request.GET.get('author', 'Unknown')
    publication_year = request.GET.get('publication_year', 0)
    book = Book.objects.create(title=title, author=author, publication_year=publication_year)
    return HttpResponse(f"Bookshelf: Created book: {book.title} (id={book.id})")


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    new_title = request.GET.get('title')
    if new_title:
        book.title = new_title
        book.save()
        return HttpResponse(f"Bookshelf: Updated book: {book.title}")
    return HttpResponse(f"Bookshelf: Edit page for: {book.title}")


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return HttpResponse(f"Bookshelf: Deleted book id={pk}")
