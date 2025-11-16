# LibraryProject

A Django-based library management system.

## Project Information

- **Django Version**: 5.2.7
- **Python Version**: 3.13.9
- **Project Type**: Library Management System

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install django
   ```

2. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

3. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

4. **Access the Application**
   - Open your browser and navigate to: `http://127.0.0.1:8000/`

## Project Structure

```
LibraryProject/
├── LibraryProject/      # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── manage.py            # Django management script
└── db.sqlite3          # SQLite database
```

## Features

- Django admin interface
- Database management with SQLite
- Ready for app development

## Development

To create a new Django app:
```bash
python manage.py startapp <app_name>
```

## License

This project is part of the ALX Django Learning Lab.
