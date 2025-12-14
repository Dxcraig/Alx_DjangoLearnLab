"""
Django settings for LibraryProject project (advanced_features_and_security copy).
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Keep the secret key used in production secret!
# In production, load this from environment variables or a secure configuration file
SECRET_KEY = 'django-insecure-replaced-for-advanced-features'

# SECURITY WARNING: Don't run with debug turned on in production!
# DEBUG = True exposes sensitive information in error pages
# Set to False in production to prevent information disclosure
DEBUG = False

# SECURITY: Define allowed hosts to prevent Host Header attacks
# In production, set this to your actual domain names
# Example: ALLOWED_HOSTS = ['example.com', 'www.example.com']
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

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
# Use custom user model in `bookshelf` app (moved from `accounts`)
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Media for profile photos
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Reminder: install Pillow to use ImageField

# ============================================================================
# SECURITY SETTINGS
# ============================================================================
# These settings protect against common web vulnerabilities

# XSS Protection: Enables browser's XSS filtering to prevent cross-site scripting attacks
# This header instructs the browser to block pages if it detects XSS attacks
SECURE_BROWSER_XSS_FILTER = True

# Content Type Sniffing Protection: Prevents browsers from MIME-sniffing responses
# This protects against MIME type confusion attacks
SECURE_CONTENT_TYPE_NOSNIFF = True

# Clickjacking Protection: Prevents the site from being embedded in frames/iframes
# 'DENY' prevents any domain from framing the content
# Alternative: 'SAMEORIGIN' allows only same-origin framing
X_FRAME_OPTIONS = 'DENY'

# CSRF Cookie Security: Ensures CSRF tokens are only sent over HTTPS
# This prevents token interception over insecure connections
CSRF_COOKIE_SECURE = True

# Session Cookie Security: Forces session cookies to be sent only over HTTPS
# This prevents session hijacking over insecure connections
SESSION_COOKIE_SECURE = True

# HTTP-Only Cookies: Prevents JavaScript from accessing session cookies
# This mitigates XSS attacks that attempt to steal session data
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
