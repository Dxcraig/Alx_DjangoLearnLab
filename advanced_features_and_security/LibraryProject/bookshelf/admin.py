from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Book

User = get_user_model()

try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    # If another app already registered the user admin, skip.
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
