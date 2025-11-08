from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books
from .views import LibraryDetailView

urlpatterns = [
    # Book and Library views
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]
