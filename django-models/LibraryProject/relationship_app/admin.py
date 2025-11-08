from django.contrib import admin
from .models import UserProfile, Author, Book, Library, Librarian

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')

admin.register(Author)
admin.register(Book)
admin.register(Library)
admin.register(Librarian)
