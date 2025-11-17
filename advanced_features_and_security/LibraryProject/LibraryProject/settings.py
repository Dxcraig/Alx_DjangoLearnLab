"""
Django settings for LibraryProject project (advanced_features_and_security copy).
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-replaced-for-advanced-features'
DEBUG = True
ALLOWED_HOSTS = []

# SECURITY: in production make sure DEBUG=False and set real hosts
# For local development you can temporarily set DEBUG=True, but keep
# the secure defaults below to prevent accidental exposure.
DEBUG = False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    "bookshelf.apps.BookshelfConfig",
    "relationship_app.apps.RelationshipAppConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'LibraryProject.middleware.security.SecurityHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_REDIRECT_URL = 'list_books'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'
# Use custom user model in new `accounts` app
AUTH_USER_MODEL = 'accounts.CustomUser'

# Media for profile photos
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Reminder: install Pillow to use ImageField

# Security settings (recommended for production)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Ensure cookies are only sent over HTTPS in production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Basic Content Security Policy sources for inline resources.
# You should adapt these to your deployment (CDNs, analytics, etc.).
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'",)

# ---- HTTPS / HSTS / secure cookies -------------------------------------
# Redirect all HTTP traffic to HTTPS. Enable this in production when SSL is
# terminated at your load balancer or web server (e.g. nginx) and the site is
# accessible over HTTPS.
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security (HSTS). A long duration (e.g. 1 year) is
# recommended once you are confident HTTPS is working for all hosts.
# See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
SECURE_HSTS_SECONDS = 31536000  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# If your project sits behind a proxy / load balancer that sets
# X-Forwarded-Proto, enable this so Django knows the original scheme.
# Be sure your proxy is trusted; do NOT enable this unless you control the
# proxy (example shown as comment):
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Note: `ALLOWED_HOSTS` must include your production domain names when
# DEBUG=False, otherwise Django will raise a DisallowedHost error. For
# development you can use `ALLOWED_HOSTS = ['localhost', '127.0.0.1']`.
