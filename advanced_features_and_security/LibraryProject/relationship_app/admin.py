from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import (
    UserProfile,
    Author,
    Book,
    Library,
    Librarian,
)

User = get_user_model()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')


admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
