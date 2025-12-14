# Social Media API

A Django REST Framework-based Social Media API with user authentication, profile management, posts, comments, and a follow system with personalized feeds.

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [User Model](#user-model)
- [Testing with Postman](#testing-with-postman)
- [Additional Documentation](#additional-documentation)

## Features

- **User Authentication**: Token-based authentication using Django REST Framework
- **User Registration**: Create new user accounts with email validation
- **User Login**: Authenticate users and receive authentication tokens
- **User Profile Management**: View and update user profiles
- **Custom User Model**: Extended user model with bio, profile picture, and following/followers
- **Follow System**: Users can follow/unfollow other users
- **Personalized Feed**: View posts from users you follow
- **Posts & Comments**: Create, read, update, and delete posts and comments
- **Likes System**: Like and unlike posts with real-time counts
- **Notifications**: Receive notifications for follows, likes, and comments
- **Search & Filter**: Search posts by title/content and filter by various criteria

## 📚 Documentation

### Getting Started
- **[Quick Start Guide](QUICKSTART.md)** - Fast setup and usage guide
- **[Project Summary](PROJECT_SUMMARY.md)** - Complete project overview

### Features Documentation
- **[Follow System & Feed](FOLLOW_SYSTEM_DOCUMENTATION.md)** - Follow/unfollow and personalized feed
- **[Likes & Notifications](LIKES_NOTIFICATIONS_DOCUMENTATION.md)** - Likes and notification system

### Deployment Guides
- **[Production Deployment](DEPLOYMENT.md)** - Deploy to Heroku, AWS, DigitalOcean, or manual servers
- **[Docker Deployment](DOCKER_DEPLOYMENT.md)** - Containerized deployment with Docker
- **[Production Checklist](PRODUCTION_CHECKLIST.md)** - Pre-deployment verification

### Testing
- **[Postman Collection](Social_Media_API.postman_collection.json)** - Import for API testing

## Technology Stack

- **Python**: 3.x
- **Django**: 5.2.7
- **Django REST Framework**: Latest version
- **SQLite**: Database (development)
- **Token Authentication**: DRF token-based authentication

## Project Structure

```
social_media_api/
├── manage.py
├── db.sqlite3
├── media/                          # User uploaded files (profile pictures)
├── social_media_api/               # Main project directory
│   ├── __init__.py
│   ├── settings.py                # Project settings
│   ├── urls.py                    # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
└── accounts/                       # User authentication app
    ├── __init__.py
    ├── admin.py                   # Admin interface configuration
    ├── models.py                  # CustomUser model
    ├── serializers.py             # API serializers
    ├── views.py                   # API views
    ├── urls.py                    # App URL patterns
    ├── apps.py
    └── migrations/                # Database migrations
```

## Setup Instructions

### Prerequisites

- Python 3.x installed
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd social_media_api
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install django djangorestframework pillow
   ```

4. **Run migrations to create the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at: `http://127.0.0.1:8000/`

## API Endpoints

### Authentication Endpoints

#### 1. User Registration
- **URL**: `/api/accounts/register/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "bio": "Software developer and tech enthusiast",
    "profile_picture": null
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Software developer and tech enthusiast",
    "profile_picture": null,
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "message": "User registered successfully"
  }
  ```

#### 2. User Login
- **URL**: `/api/accounts/login/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "password": "securepassword123"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "message": "Login successful"
  }
  ```

#### 3. User Logout
- **URL**: `/api/accounts/logout/`
- **Method**: `POST`
- **Authentication**: Required (Token)
- **Headers**:
  ```
  Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
  ```
- **Response** (200 OK):
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

### Profile Endpoints

#### 4. Get User Profile
- **URL**: `/api/accounts/profile/`
- **Method**: `GET`
- **Authentication**: Required (Token)
- **Headers**:
  ```
  Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
  ```
- **Response** (200 OK):
  ```json
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Software developer and tech enthusiast",
    "profile_picture": "/media/profile_pictures/profile.jpg",
    "followers_count": 10,
    "following_count": 5,
    "date_joined": "2024-12-14T10:30:00Z"
  }
  ```

#### 5. Update User Profile
- **URL**: `/api/accounts/profile/`
- **Method**: `PUT` or `PATCH`
- **Authentication**: Required (Token)
- **Headers**:
  ```
  Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
  Content-Type: multipart/form-data
  ```
- **Request Body** (form-data):
  ```
  bio: "Updated bio - Full-stack developer"
  profile_picture: [file upload]
  ```
- **Response** (200 OK):
  ```json
  {
    "bio": "Updated bio - Full-stack developer",
    "profile_picture": "/media/profile_pictures/new_profile.jpg"
  }
  ```

## User Model

### CustomUser Model Fields

The `CustomUser` model extends Django's `AbstractUser` with additional fields:

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| username | CharField | Unique username | Yes |
| email | EmailField | User's email address | Yes |
| password | CharField | Hashed password | Yes |
| bio | TextField | User biography (max 500 chars) | No |
| profile_picture | ImageField | Profile picture | No |
| following | ManyToManyField | Users that this user follows | No |
| first_name | CharField | User's first name | No |
| last_name | CharField | User's last name | No |
| date_joined | DateTimeField | Account creation date | Auto |

### Custom Methods

- `get_followers_count()`: Returns the number of followers
- `get_following_count()`: Returns the number of users being followed

### Follow System

The follow system uses a many-to-many relationship:
- **following**: Represents users that the current user follows
- **followers**: Reverse relationship showing users who follow the current user

For detailed information about the follow system and feed, see [FOLLOW_SYSTEM_DOCUMENTATION.md](FOLLOW_SYSTEM_DOCUMENTATION.md).

### Quick Reference: Follow Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/accounts/follow/<user_id>/` | POST | Follow a user |
| `/api/accounts/unfollow/<user_id>/` | POST | Unfollow a user |
| `/api/accounts/following/` | GET | List users you follow |
| `/api/accounts/followers/` | GET | List your followers |
| `/api/posts/feed/` | GET | Get personalized feed from followed users |

## Testing with Postman

### Setting Up Postman

1. **Install Postman**: Download from [postman.com](https://www.postman.com/)

2. **Create a new collection**: Name it "Social Media API"

### Test Scenarios

#### Test 1: User Registration

1. Create a new POST request
2. URL: `http://127.0.0.1:8000/api/accounts/register/`
3. Body → raw → JSON:
   ```json
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "testpass123",
     "password_confirm": "testpass123",
     "bio": "Test user bio"
   }
   ```
4. Send the request
5. **Expected**: 201 Created with token in response
6. **Save the token** for subsequent requests

#### Test 2: User Login

1. Create a new POST request
2. URL: `http://127.0.0.1:8000/api/accounts/login/`
3. Body → raw → JSON:
   ```json
   {
     "username": "testuser",
     "password": "testpass123"
   }
   ```
4. Send the request
5. **Expected**: 200 OK with token in response

#### Test 3: Get User Profile

1. Create a new GET request
2. URL: `http://127.0.0.1:8000/api/accounts/profile/`
3. Headers:
   - Key: `Authorization`
   - Value: `Token [your-token-here]`
4. Send the request
5. **Expected**: 200 OK with user profile data

#### Test 4: Update User Profile

1. Create a new PATCH request
2. URL: `http://127.0.0.1:8000/api/accounts/profile/`
3. Headers:
   - Key: `Authorization`
   - Value: `Token [your-token-here]`
4. Body → raw → JSON:
   ```json
   {
     "bio": "Updated bio text"
   }
   ```
5. Send the request
6. **Expected**: 200 OK with updated profile data

#### Test 5: Upload Profile Picture

1. Create a new PATCH request
2. URL: `http://127.0.0.1:8000/api/accounts/profile/`
3. Headers:
   - Key: `Authorization`
   - Value: `Token [your-token-here]`
4. Body → form-data:
   - Key: `profile_picture`
   - Type: File
   - Value: [Select an image file]
5. Send the request
6. **Expected**: 200 OK with profile picture URL

#### Test 6: User Logout

1. Create a new POST request
2. URL: `http://127.0.0.1:8000/api/accounts/logout/`
3. Headers:
   - Key: `Authorization`
   - Value: `Token [your-token-here]`
4. Send the request
5. **Expected**: 200 OK with logout confirmation
6. Token is now invalidated

### Common Error Responses

- **400 Bad Request**: Invalid data in request body
- **401 Unauthorized**: Missing or invalid authentication token
- **404 Not Found**: Endpoint doesn't exist
- **500 Internal Server Error**: Server-side error

## Configuration Details

### Settings Configuration

Key settings in `settings.py`:

```python
# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Installed Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'accounts',
]
```

## 🚀 Production Deployment

This API is **production-ready** with complete deployment configurations for:

### Deployment Options
- **Heroku** - Quick deployment with managed database
- **AWS (EC2 + RDS)** - Scalable enterprise deployment
- **DigitalOcean** - App Platform or Droplet deployment
- **Docker** - Containerized deployment with Nginx and PostgreSQL
- **Manual Server** - VPS deployment with full control

### Production Features
✅ Environment-based configuration  
✅ PostgreSQL database support  
✅ Gunicorn WSGI server  
✅ WhiteNoise static file serving  
✅ Nginx reverse proxy configuration  
✅ SSL/HTTPS enforcement  
✅ Security headers (HSTS, XSS, CSRF)  
✅ Logging and monitoring  
✅ Docker containerization  

### Quick Deploy Commands

**Heroku:**
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run python manage.py migrate
```

**Docker:**
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
```

📖 **See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions**

📖 **See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for Docker deployment**

📋 **Use [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) before deploying**

## 📦 Dependencies

### Core Dependencies
```
Django==5.2.7
djangorestframework==3.16.1
django-filter==24.3
Pillow==12.0.0
django-cors-headers==4.7.0
```

### Production Dependencies
```
gunicorn==23.0.0
psycopg2-binary==2.9.10
whitenoise==6.8.2
dj-database-url==2.3.0
python-decouple==3.8
python-dotenv==1.0.1
```

Install all dependencies: `pip install -r requirements.txt`

## 🔒 Security

### Production Security Features
- HTTPS enforcement with `SECURE_SSL_REDIRECT`
- HSTS headers for strict transport security
- Secure cookies for sessions and CSRF
- XSS protection headers
- Content type sniffing protection
- CORS configuration for frontend domains
- Environment-based secret key management

### Environment Variables
Create a `.env` file for production:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

## Next Steps

### Already Implemented ✅
1. ✅ **Posts API**: Create, read, update, and delete posts
2. ✅ **Comments**: Comment on posts with notifications
3. ✅ **Likes**: Like/unlike posts with real-time counts
4. ✅ **Follow/Unfollow**: Complete follow system with notifications
5. ✅ **Feed**: Personalized feed from followed users
6. ✅ **Notifications**: Comprehensive notification system
7. ✅ **Production Ready**: Full deployment configurations

### Future Enhancements 🚀
1. **Direct Messaging**: Private messages between users
2. **Post Media**: Support for images and videos in posts
3. **Hashtags**: Tag posts and search by hashtags
4. **Search**: Advanced search for users and posts
5. **Stories**: Temporary 24-hour posts
6. **User Verification**: Verified badges for authentic accounts
7. **Trending Topics**: Display popular hashtags and topics
8. **Rate Limiting**: API throttling for security
9. **Comprehensive Testing**: Unit and integration tests
10. **GraphQL API**: Alternative to REST endpoints

## Troubleshooting

### Issue: Token not returned after registration
**Solution**: Ensure migrations are run and `rest_framework.authtoken` is in INSTALLED_APPS

### Issue: Profile picture upload fails
**Solution**: Ensure Pillow is installed (`pip install pillow`) and MEDIA settings are configured

### Issue: Authentication fails
**Solution**: Check that the token is being sent in the header as `Authorization: Token [token]`

## License

This project is for educational purposes as part of the Alx Django Learn Lab.

## Contact

For questions or issues, please contact the development team.
