from django.urls import path
from . import views

urlpatterns = [
    path('books/<int:pk>/', views.view_book, name='bookshelf_view_book'),
    path('books/create/', views.create_book, name='bookshelf_create_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='bookshelf_edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='bookshelf_delete_book'),
]
