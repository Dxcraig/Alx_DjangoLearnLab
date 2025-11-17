from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required, login_required

from .models import Book
from .forms import BookForm, ExampleForm
from django.contrib import messages


@permission_required('bookshelf.can_view', raise_exception=True)
def view_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('bookshelf_view_book', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form, 'action': 'Create'})


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookshelf_view_book', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/form_example.html', {'form': form, 'action': 'Edit'})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('bookshelf_book_list')


def example_form(request):
    """Render and process the small `ExampleForm` used for demos.

    GET: show empty form
    POST: validate and show success message with submitted name
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            messages.success(request, f'Thanks, {name}! Your message was received.')
            return redirect('bookshelf_example_form')
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/example_form.html', {'form': form})
