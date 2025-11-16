Advanced Features & Security - Permissions and Groups

This duplicate project demonstrates a custom user model and a simple groups/permissions setup.

Setup (Windows PowerShell):

```pwsh
cd .\advanced_features_and_security\LibraryProject
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install django pillow
python manage.py makemigrations
python manage.py migrate
# Create groups and test users (this creates Viewers, Editors, Admins and example users)
python manage.py setup_groups
# Run server
python manage.py runserver
```

Test users created by `setup_groups`:
- viewer / viewerpass (in Viewers)
- editor / editorpass (in Editors)
- groupadmin / adminpass (in Admins)

Permission codenames used by the Book model: `can_view`, `can_create`, `can_edit`, `can_delete`.

Views demonstrating permission checks (HTTP GET demo endpoints):
- `/relationship/books/<id>/` – requires `relationship_app.can_view`
- `/relationship/books/create/?title=...&author_id=...` – requires `relationship_app.can_create`
- `/relationship/books/<id>/edit/?title=...` – requires `relationship_app.can_edit`
- `/relationship/books/<id>/delete/` – requires `relationship_app.can_delete`

Notes:
- The create/edit/delete views are intentionally minimal for demonstration. In a real app use forms and POST requests with CSRF protection.
- Use Django admin to further manage groups and permissions.
