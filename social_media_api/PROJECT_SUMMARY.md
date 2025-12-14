# Social Media API - Project Summary

## 📋 Overview

A comprehensive Django REST Framework API for a social media platform with features including user authentication, posts, comments, likes, follows, notifications, and a personalized feed system. The API is production-ready with complete deployment configurations for multiple platforms.

## ✨ Features

### Core Functionality
- **User Authentication**
  - Token-based authentication
  - User registration and login
  - Profile management with bio and profile pictures

- **Social Features**
  - Create, read, update, delete posts
  - Comment on posts
  - Like/unlike posts
  - Follow/unfollow users
  - Personalized feed showing posts from followed users

- **Engagement System**
  - Real-time notifications for:
    - New followers
    - Post likes
    - Post comments
  - Notification read/unread status tracking
  - Mark all notifications as read

- **API Endpoints**
  - RESTful API design
  - Token authentication
  - Permission-based access control
  - Comprehensive error handling

## 🛠️ Technology Stack

### Backend
- **Django 5.2.7** - Web framework
- **Django REST Framework 3.16.1** - API framework
- **Python 3.11.9** - Programming language

### Database
- **SQLite** - Development database
- **PostgreSQL** - Production database (via psycopg2-binary)

### Production Stack
- **Gunicorn 23.0.0** - WSGI HTTP server
- **WhiteNoise 6.8.2** - Static file serving
- **Nginx** - Reverse proxy and static file server

### Utilities
- **django-filter 24.3** - Advanced filtering
- **Pillow 12.0.0** - Image processing
- **dj-database-url** - Database configuration
- **python-decouple/python-dotenv** - Environment variables
- **django-cors-headers** - CORS handling

## 📁 Project Structure

```
social_media_api/
├── accounts/                    # User management app
│   ├── models.py               # CustomUser model with following
│   ├── views.py                # Authentication, follow/unfollow
│   ├── serializers.py          # User serialization
│   └── urls.py                 # User-related endpoints
│
├── posts/                       # Content management app
│   ├── models.py               # Post, Comment, Like models
│   ├── views.py                # CRUD operations, like/unlike
│   ├── serializers.py          # Content serialization
│   └── urls.py                 # Content endpoints
│
├── notifications/               # Notification system
│   ├── models.py               # Notification model
│   ├── views.py                # Notification endpoints
│   └── urls.py                 # Notification routes
│
├── social_media_api/            # Project settings
│   ├── settings.py             # Configuration (dev + prod)
│   ├── urls.py                 # Main URL routing
│   └── wsgi.py                 # WSGI configuration
│
├── Deployment Files
│   ├── Procfile                # Heroku deployment
│   ├── runtime.txt             # Python version
│   ├── Dockerfile              # Docker image
│   ├── docker-compose.yml      # Multi-container setup
│   ├── nginx.conf              # Nginx configuration
│   └── nginx-docker.conf       # Docker Nginx config
│
├── Documentation
│   ├── README.md               # Project overview
│   ├── QUICKSTART.md           # Getting started guide
│   ├── DEPLOYMENT.md           # Comprehensive deployment guide
│   ├── DOCKER_DEPLOYMENT.md    # Docker-specific guide
│   ├── PRODUCTION_CHECKLIST.md # Pre-deployment checklist
│   ├── FOLLOW_SYSTEM_DOCUMENTATION.md
│   └── LIKES_NOTIFICATIONS_DOCUMENTATION.md
│
├── Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment template
│   ├── .gitignore              # Git ignore rules
│   └── .dockerignore           # Docker ignore rules
│
└── Database
    └── db.sqlite3              # SQLite database (dev only)
```

## 🔌 API Endpoints

### Authentication
```
POST   /api/accounts/register/           # Register new user
POST   /api/accounts/login/              # Login and get token
GET    /api/accounts/profile/            # Get user profile
PUT    /api/accounts/profile/            # Update profile
```

### Follow System
```
POST   /api/accounts/follow/<user_id>/   # Follow a user
POST   /api/accounts/unfollow/<user_id>/ # Unfollow a user
GET    /api/accounts/followers/          # List followers
GET    /api/accounts/following/          # List following
```

### Posts
```
GET    /api/posts/                       # List all posts
POST   /api/posts/                       # Create a post
GET    /api/posts/<id>/                  # Get post detail
PUT    /api/posts/<id>/                  # Update post
DELETE /api/posts/<id>/                  # Delete post
GET    /api/feed/                        # Personalized feed
```

### Likes
```
POST   /api/posts/<id>/like/             # Like a post
POST   /api/posts/<id>/unlike/           # Unlike a post
```

### Comments
```
GET    /api/comments/                    # List comments
POST   /api/comments/                    # Create comment
GET    /api/comments/<id>/               # Get comment
PUT    /api/comments/<id>/               # Update comment
DELETE /api/comments/<id>/               # Delete comment
```

### Notifications
```
GET    /api/notifications/               # List all notifications
GET    /api/notifications/unread/        # List unread notifications
POST   /api/notifications/<id>/read/     # Mark as read
POST   /api/notifications/read-all/      # Mark all as read
```

## 🗄️ Database Models

### CustomUser
- Extends Django's AbstractUser
- Additional fields: `bio`, `profile_picture`, `following`
- Many-to-many self-relationship for followers/following

### Post
- Fields: `author`, `title`, `content`, `created_at`, `updated_at`
- Related: Comments, Likes
- Methods: `get_likes_count()`

### Comment
- Fields: `post`, `author`, `content`, `created_at`, `updated_at`
- Foreign keys to Post and User
- Triggers notification on creation

### Like
- Fields: `user`, `post`, `created_at`
- Unique constraint on (user, post)
- Triggers notification on creation

### Notification
- Fields: `recipient`, `actor`, `verb`, `target`, `timestamp`, `read`
- Uses GenericForeignKey for flexible target objects
- Methods: `mark_as_read()`

## 🔒 Security Features

### Production Security Settings
- ✅ `DEBUG = False` in production
- ✅ Strong `SECRET_KEY` from environment
- ✅ HTTPS enforcement (`SECURE_SSL_REDIRECT`)
- ✅ HSTS headers (max-age: 1 year)
- ✅ Secure cookies (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)
- ✅ XSS protection (`X_FRAME_OPTIONS='DENY'`)
- ✅ Content type sniffing protection
- ✅ CORS configuration for frontend domains
- ✅ SQL injection protection (Django ORM)
- ✅ CSRF protection (Django middleware)

### Authentication & Authorization
- Token-based authentication (DRF authtoken)
- Permission classes: `IsAuthenticated`, `IsAuthorOrReadOnly`
- User-specific data filtering

## 📦 Dependencies

### Core (17 packages)
```
asgiref==3.8.1
Django==5.2.7
django-cors-headers==4.7.0
django-filter==24.3
djangorestframework==3.16.1
Pillow==12.0.0
sqlparse==0.5.4
tzdata==2024.2
```

### Production
```
dj-database-url==2.3.0
gunicorn==23.0.0
psycopg2-binary==2.9.10
python-decouple==3.8
python-dotenv==1.0.1
typing_extensions==4.12.2
whitenoise==6.8.2
```

## 🚀 Deployment Options

### 1. Heroku (PaaS - Easiest)
- One-command deployment
- Managed PostgreSQL
- Automatic SSL
- See: `DEPLOYMENT.md` → Heroku section

### 2. AWS (Most Scalable)
- EC2 + RDS setup
- Full control over infrastructure
- Load balancing capable
- See: `DEPLOYMENT.md` → AWS section

### 3. DigitalOcean (Balanced)
- App Platform (easy) or Droplets (flexible)
- Managed databases available
- Cost-effective
- See: `DEPLOYMENT.md` → DigitalOcean section

### 4. Docker (Containerized)
- Multi-container setup with Docker Compose
- PostgreSQL + Django + Nginx
- Easy local development and production parity
- See: `DOCKER_DEPLOYMENT.md`

### 5. Manual Server (Full Control)
- VPS deployment
- Custom Nginx + Gunicorn + Supervisor
- Maximum flexibility
- See: `DEPLOYMENT.md` → Manual Server section

## 🧪 Testing

### Run Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test accounts
python manage.py test posts
python manage.py test notifications

# With coverage
coverage run --source='.' manage.py test
coverage report
```

### Test API with Postman
Import `Social_Media_API.postman_collection.json` into Postman for comprehensive API testing.

## 📊 Development Workflow

### Local Setup
```bash
# Clone repository
git clone https://github.com/yourusername/social_media_api.git
cd social_media_api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations
```

### Admin Panel
- Access at: http://localhost:8000/admin/
- All models registered for easy management

## 🌐 Environment Variables

### Required for Production
```env
SECRET_KEY=<50-character-random-string>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://frontend.com
```

### Optional
```env
DJANGO_LOG_LEVEL=INFO
SENTRY_DSN=<sentry-project-dsn>
AWS_ACCESS_KEY_ID=<for-s3-storage>
AWS_SECRET_ACCESS_KEY=<for-s3-storage>
AWS_STORAGE_BUCKET_NAME=<bucket-name>
```

## 📝 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview and features |
| `QUICKSTART.md` | Getting started guide |
| `DEPLOYMENT.md` | Comprehensive deployment guide (all platforms) |
| `DOCKER_DEPLOYMENT.md` | Docker-specific deployment |
| `PRODUCTION_CHECKLIST.md` | Pre-deployment verification checklist |
| `FOLLOW_SYSTEM_DOCUMENTATION.md` | Follow system implementation details |
| `LIKES_NOTIFICATIONS_DOCUMENTATION.md` | Likes and notifications details |

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `Procfile` | Heroku deployment commands |
| `runtime.txt` | Python version specification |
| `Dockerfile` | Docker image build instructions |
| `docker-compose.yml` | Multi-container Docker setup |
| `nginx.conf` | Nginx reverse proxy config |
| `nginx-docker.conf` | Docker-specific Nginx config |
| `.env.example` | Environment variables template |
| `.gitignore` | Git ignore rules |
| `.dockerignore` | Docker build ignore rules |

## 📈 Performance Considerations

### Optimization Techniques Implemented
- Database indexing on foreign keys
- `select_related()` and `prefetch_related()` for query optimization
- WhiteNoise for efficient static file serving
- Gunicorn with multiple workers
- Nginx caching for static files
- Database connection pooling (production)

### Recommended Additions
- Redis for caching and session storage
- Celery for background tasks (email notifications, etc.)
- CDN for static files (CloudFront, Cloudflare)
- Database read replicas for high traffic
- Rate limiting (django-ratelimit)

## 🔍 Monitoring and Logging

### Logging Configuration
- Console logging for development
- File logging for production (`logs/django.log`)
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Separate error file logging

### Recommended Monitoring Tools
- **Error Tracking:** Sentry
- **Performance:** New Relic, Datadog
- **Uptime:** UptimeRobot, Pingdom
- **Analytics:** Google Analytics, Mixpanel

## 🤝 Contributing

### Development Guidelines
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Follow PEP 8 style guide
5. Update documentation
6. Submit pull request

### Code Style
- Use Django naming conventions
- Write docstrings for complex functions
- Keep views thin, models fat
- Use serializers for data validation

## 📜 License

This project is open source and available under the MIT License.

## 👥 Team

**Project Type:** Educational/Portfolio Project  
**Framework:** Django REST Framework  
**Status:** Production Ready  

## 🎯 Future Enhancements

### Planned Features
- [ ] Direct messaging between users
- [ ] Post sharing/reposting functionality
- [ ] Hashtag support
- [ ] Search functionality (users, posts, hashtags)
- [ ] User verification badges
- [ ] Post media (images, videos)
- [ ] Stories feature
- [ ] Trending topics
- [ ] User blocking functionality
- [ ] Report/moderation system

### Technical Improvements
- [ ] GraphQL API option
- [ ] WebSocket support for real-time updates
- [ ] Elasticsearch for advanced search
- [ ] Redis caching layer
- [ ] Celery for async tasks
- [ ] Rate limiting per user
- [ ] API versioning
- [ ] Automated testing with CI/CD
- [ ] Load testing and optimization
- [ ] Multi-language support (i18n)

## 📞 Support

### Resources
- **Django Documentation:** https://docs.djangoproject.com/
- **DRF Documentation:** https://www.django-rest-framework.org/
- **Deployment Guide:** See `DEPLOYMENT.md`
- **Docker Guide:** See `DOCKER_DEPLOYMENT.md`

### Troubleshooting
For common issues and solutions, refer to:
1. `DEPLOYMENT.md` → Troubleshooting section
2. `DOCKER_DEPLOYMENT.md` → Troubleshooting section
3. Check application logs: `logs/django.log`

## ✅ Project Status

**Current Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** 2024  

### Completed Milestones
- ✅ Core API implementation
- ✅ User authentication system
- ✅ Follow/unfollow functionality
- ✅ Feed system
- ✅ Likes and comments
- ✅ Notification system
- ✅ Production security configuration
- ✅ Multi-platform deployment guides
- ✅ Docker containerization
- ✅ Comprehensive documentation

### Ready for Production
- ✅ Security hardening complete
- ✅ Environment-based configuration
- ✅ Static file handling configured
- ✅ Database migration system
- ✅ Error handling and logging
- ✅ API documentation
- ✅ Deployment automation (Heroku, Docker)
- ✅ Production checklist provided

---

## 🎉 Quick Links

- **Local Development:** `python manage.py runserver` → http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin/
- **API Root:** http://localhost:8000/api/
- **Postman Collection:** `Social_Media_API.postman_collection.json`

---

**Built with ❤️ using Django REST Framework**

For detailed setup and deployment instructions, see:
- **Getting Started:** `QUICKSTART.md`
- **Deployment:** `DEPLOYMENT.md`
- **Docker:** `DOCKER_DEPLOYMENT.md`
- **Pre-Deployment:** `PRODUCTION_CHECKLIST.md`
