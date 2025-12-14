# Quick Start Guide - Social Media API

## Installation

1. **Navigate to project directory**
   ```bash
   cd social_media_api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

   Server will be running at: http://127.0.0.1:8000/

## Quick Testing

### 1. Register a new user
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "bio": "Test user"
  }'
```

### 2. Login
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

Save the token from the response!

### 3. Get Profile
```bash
curl -X GET http://127.0.0.1:8000/api/accounts/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 4. Update Profile
```bash
curl -X PATCH http://127.0.0.1:8000/api/accounts/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Updated bio text"
  }'
```

## Available Endpoints

- `POST /api/accounts/register/` - Register new user
- `POST /api/accounts/login/` - Login user
- `POST /api/accounts/logout/` - Logout user (requires auth)
- `GET /api/accounts/profile/` - Get user profile (requires auth)
- `PATCH /api/accounts/profile/` - Update profile (requires auth)

## Testing with Postman

Import the `Social_Media_API.postman_collection.json` file into Postman to test all endpoints easily.

## Admin Interface

Create a superuser to access the Django admin:
```bash
python manage.py createsuperuser
```

Access admin at: http://127.0.0.1:8000/admin/

## Next Steps

Refer to the main README.md for detailed documentation.
