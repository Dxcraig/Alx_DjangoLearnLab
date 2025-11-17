from django.contrib import admin
from django.contrib import admin as django_admin

from .models import Book, CustomUser

# Import the CustomUserAdmin defined in `accounts.admin` so we can reuse it.
try:
    from accounts.admin import CustomUserAdmin
except Exception:
    CustomUserAdmin = None

if CustomUserAdmin is not None:
    try:
        admin.site.register(CustomUser, CustomUserAdmin)
    except django_admin.sites.AlreadyRegistered:
        pass
else:
    # Fallback: if CustomUserAdmin isn't importable, let the default admin
    # registration happen elsewhere (e.g. accounts.admin uses get_user_model()).
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
