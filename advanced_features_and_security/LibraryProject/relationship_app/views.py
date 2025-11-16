from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import permission_required, login_required

from .models import Book


@permission_required('relationship_app.can_view', raise_exception=True)
def view_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return HttpResponse(f"Viewing book: {book.title}")


@permission_required('relationship_app.can_create', raise_exception=True)
def create_book(request):
    # For demo purposes we expect ?title=...&author_id=... in GET
    title = request.GET.get('title', 'Untitled')
    author_id = request.GET.get('author_id')
    # Minimal create flow for demonstration only
    book = Book.objects.create(title=title, author_id=author_id)
    return HttpResponse(f"Created book: {book.title} (id={book.id})")


@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    new_title = request.GET.get('title')
    if new_title:
        book.title = new_title
        book.save()
        return HttpResponse(f"Updated book: {book.title}")
    return HttpResponse(f"Edit page for: {book.title}")


@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return HttpResponse(f"Deleted book id={pk}")
