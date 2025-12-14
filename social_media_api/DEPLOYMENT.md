# Social Media API - Production Deployment Guide

This guide covers deploying the Social Media API to production environments including Heroku, AWS, DigitalOcean, and manual server deployments.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Variables](#environment-variables)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS Deployment (EC2 + RDS)](#aws-deployment)
5. [DigitalOcean Deployment](#digitalocean-deployment)
6. [Manual Server Deployment](#manual-server-deployment)
7. [Database Configuration](#database-configuration)
8. [Static Files](#static-files)
9. [Security Considerations](#security-considerations)
10. [Monitoring and Logging](#monitoring-and-logging)
11. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

Before deploying to production, ensure you have:

- [ ] Set `DEBUG=False` in production
- [ ] Configured a strong `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configured `ALLOWED_HOSTS` with your domain
- [ ] Collected static files (`python manage.py collectstatic`)
- [ ] Applied all migrations (`python manage.py migrate`)
- [ ] Installed production dependencies (`pip install -r requirements.txt`)
- [ ] Configured SSL/TLS certificates
- [ ] Set up environment variables
- [ ] Configured CORS settings for frontend domains
- [ ] Tested the application locally with production settings

---

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Core Django Settings
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DATABASE_URL=postgresql://username:password@host:5432/dbname

# CORS Settings (comma-separated list)
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Optional Settings
DJANGO_LOG_LEVEL=INFO
```

**Generate a secure SECRET_KEY:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository initialized

### Step 1: Install Heroku CLI
```bash
# Windows (PowerShell)
winget install Heroku.HerokuCLI

# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login and Create App
```bash
heroku login
heroku create your-app-name
```

### Step 3: Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

### Step 4: Configure Environment Variables
```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
heroku config:set CORS_ALLOWED_ORIGINS="https://your-frontend-domain.com"
```

### Step 5: Deploy
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

### Step 6: Run Migrations
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Step 7: Open Your App
```bash
heroku open
```

### Heroku Useful Commands
```bash
# View logs
heroku logs --tail

# Run Django shell
heroku run python manage.py shell

# Scale dynos
heroku ps:scale web=1

# Restart the app
heroku restart

# Check app info
heroku info
```

---

## AWS Deployment (EC2 + RDS)

### Prerequisites
- AWS account
- EC2 instance (Ubuntu 22.04 recommended)
- RDS PostgreSQL database
- Security groups configured (ports 80, 443, 22)

### Step 1: Launch EC2 Instance
1. Create Ubuntu 22.04 EC2 instance (t2.micro for small apps)
2. Configure security group:
   - SSH (22) - Your IP
   - HTTP (80) - 0.0.0.0/0
   - HTTPS (443) - 0.0.0.0/0
3. Download and save your .pem key file

### Step 2: Set Up RDS PostgreSQL
1. Create PostgreSQL RDS instance
2. Note down: endpoint, port, database name, username, password
3. Configure security group to allow EC2 access

### Step 3: Connect to EC2
```bash
# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 4: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx postgresql-client -y

# Install supervisor for process management
sudo apt install supervisor -y
```

### Step 5: Clone and Set Up Application
```bash
# Create application directory
sudo mkdir -p /var/www/social_media_api
sudo chown ubuntu:ubuntu /var/www/social_media_api
cd /var/www/social_media_api

# Clone repository
git clone https://github.com/yourusername/social_media_api.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 6: Configure Environment
```bash
# Create .env file
nano .env
```

Add:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-ec2-ip
DATABASE_URL=postgresql://username:password@rds-endpoint:5432/dbname
CORS_ALLOWED_ORIGINS=https://your-frontend.com
```

### Step 7: Collect Static Files and Migrate
```bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

### Step 8: Configure Gunicorn with Supervisor
```bash
sudo nano /etc/supervisor/conf.d/social_media_api.conf
```

Add:
```ini
[program:social_media_api]
directory=/var/www/social_media_api
command=/var/www/social_media_api/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock social_media_api.wsgi:application
user=ubuntu
autostart=true
autorestart=true
stderr_logfile=/var/log/social_media_api.err.log
stdout_logfile=/var/log/social_media_api.out.log

[group:social_media_api]
programs=social_media_api
```

```bash
# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start social_media_api
```

### Step 9: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/social_media_api
```

Copy content from `nginx.conf` in the project, then:

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### Step 10: Set Up SSL with Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
```

---

## DigitalOcean Deployment

### Option 1: App Platform (PaaS - Easiest)

1. **Create Account** at DigitalOcean
2. **Create New App** from GitHub repository
3. **Configure Build Settings:**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn --worker-tmp-dir /dev/shm social_media_api.wsgi`
4. **Add PostgreSQL Database** (Managed Database)
5. **Set Environment Variables** in App Settings
6. **Deploy** - automatic on git push

### Option 2: Droplet (VPS - More Control)

Follow the same steps as AWS EC2 deployment above. DigitalOcean Droplets are similar to EC2 instances.

**Quick Start:**
```bash
# Create Droplet with Ubuntu 22.04
# SSH into droplet
ssh root@your-droplet-ip

# Follow AWS deployment steps 4-10
```

---

## Manual Server Deployment

For any Ubuntu/Debian server (VPS, dedicated server, etc.):

### Complete Setup Script

```bash
#!/bin/bash
# Save as deploy.sh and run with: bash deploy.sh

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib supervisor -y

# Create application directory
sudo mkdir -p /var/www/social_media_api
sudo chown $USER:$USER /var/www/social_media_api
cd /var/www/social_media_api

# Clone repository (replace with your repo)
git clone https://github.com/yourusername/social_media_api.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Create .env file (you'll need to edit this)
cp .env.example .env
nano .env

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

echo "✅ Setup complete! Now configure Nginx and Supervisor."
```

---

## Database Configuration

### PostgreSQL Setup (Local)

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Access PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE social_media_db;
CREATE USER social_media_user WITH PASSWORD 'your_password';
ALTER ROLE social_media_user SET client_encoding TO 'utf8';
ALTER ROLE social_media_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE social_media_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE social_media_db TO social_media_user;
\q
```

### Database URL Format

```
DATABASE_URL=postgresql://username:password@host:port/database

# Examples:
# Local: postgresql://social_media_user:password@localhost:5432/social_media_db
# Heroku: postgres://user:pass@host.compute-1.amazonaws.com:5432/db
# RDS: postgresql://admin:pass@mydb.123456.us-east-1.rds.amazonaws.com:5432/social_media
```

### Backup and Restore

```bash
# Backup
pg_dump -U username dbname > backup.sql

# Restore
psql -U username dbname < backup.sql

# Heroku backup
heroku pg:backups:capture
heroku pg:backups:download
```

---

## Static Files

### Collect Static Files

```bash
# Development
python manage.py collectstatic

# Production (no input prompts)
python manage.py collectstatic --noinput
```

### WhiteNoise Configuration (Already Configured)

WhiteNoise serves static files efficiently in production. Configuration in `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Right after SecurityMiddleware
    # ... other middleware
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Media Files

For user-uploaded files (profile pictures, etc.), use cloud storage:

**AWS S3:**
```bash
pip install django-storages boto3
```

```python
# settings.py
INSTALLED_APPS += ['storages']
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## Security Considerations

### Security Checklist

- [x] `DEBUG=False` in production
- [x] Strong `SECRET_KEY` (50+ random characters)
- [x] HTTPS enforced (`SECURE_SSL_REDIRECT=True`)
- [x] HSTS enabled (configured in settings.py)
- [x] Secure cookies (`SESSION_COOKIE_SECURE=True`)
- [x] CSRF protection enabled (Django default)
- [x] XSS protection (`X_FRAME_OPTIONS='DENY'`)
- [x] SQL injection protection (Django ORM)
- [ ] Regular security updates (`pip list --outdated`)
- [ ] Database backups configured
- [ ] Rate limiting (consider django-ratelimit)
- [ ] WAF (Web Application Firewall) if using AWS/Cloudflare

### Additional Security Measures

**Install django-ratelimit:**
```bash
pip install django-ratelimit
```

```python
# views.py
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m')
def login_view(request):
    # Only allow 5 login attempts per minute
    pass
```

**Environment Variable Security:**
- Never commit `.env` to version control
- Use AWS Secrets Manager or Heroku Config Vars
- Rotate credentials regularly

---

## Monitoring and Logging

### Application Logs

Logs are configured in `settings.py` and saved to `logs/django.log`:

```bash
# View logs
tail -f logs/django.log

# View errors only
grep ERROR logs/django.log

# Heroku logs
heroku logs --tail --app your-app-name
```

### Error Tracking with Sentry

```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### Performance Monitoring

**New Relic:**
```bash
pip install newrelic
newrelic-admin generate-config LICENSE_KEY newrelic.ini
```

**Datadog:**
```bash
pip install ddtrace
ddtrace-run gunicorn social_media_api.wsgi
```

---

## Troubleshooting

### Common Issues

#### 1. Static Files Not Loading

```bash
# Ensure static files are collected
python manage.py collectstatic --noinput

# Check STATIC_ROOT in settings.py
# Verify Nginx configuration for /static/ location
```

#### 2. Database Connection Error

```bash
# Test database connection
python manage.py dbshell

# Check DATABASE_URL format
echo $DATABASE_URL

# Verify PostgreSQL is running
sudo systemctl status postgresql
```

#### 3. Gunicorn Not Starting

```bash
# Check logs
sudo tail -f /var/log/social_media_api.err.log

# Test Gunicorn manually
gunicorn --bind 0.0.0.0:8000 social_media_api.wsgi:application

# Check supervisor status
sudo supervisorctl status
```

#### 4. 502 Bad Gateway (Nginx)

```bash
# Check if Gunicorn is running
ps aux | grep gunicorn

# Check Nginx error log
sudo tail -f /var/log/nginx/error.log

# Verify socket file permissions
ls -l /run/gunicorn.sock
```

#### 5. CORS Errors

```python
# settings.py - Ensure CORS settings are correct
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

# For development only
# CORS_ALLOW_ALL_ORIGINS = True
```

#### 6. Permission Denied Errors

```bash
# Fix directory permissions
sudo chown -R ubuntu:ubuntu /var/www/social_media_api

# Fix socket permissions
sudo chown ubuntu:www-data /run/gunicorn.sock
```

### Debug Mode Testing

Test with `DEBUG=True` locally before production:

```bash
# .env
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

python manage.py runserver
```

Then switch to production settings:

```bash
# .env
DEBUG=False
DATABASE_URL=postgresql://...

gunicorn social_media_api.wsgi:application
```

---

## Post-Deployment Tasks

### 1. Create Superuser
```bash
python manage.py createsuperuser
```

### 2. Test All Endpoints
Use Postman collection: `Social_Media_API.postman_collection.json`

### 3. Monitor for 24 Hours
- Check error logs
- Monitor database queries
- Track response times

### 4. Set Up Automated Backups
```bash
# Cron job for daily backups
crontab -e

# Add:
0 2 * * * pg_dump -U user dbname > /backups/db_$(date +\%Y\%m\%d).sql
```

### 5. Configure Domain and DNS
Point your domain A record to your server IP:
```
A    @     YOUR_SERVER_IP
A    www   YOUR_SERVER_IP
```

---

## Production Checklist

Final checklist before going live:

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] SSL certificate installed
- [ ] Domain DNS configured
- [ ] Superuser created
- [ ] All tests passing
- [ ] Backup system configured
- [ ] Monitoring/logging set up
- [ ] Security headers verified
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] Team notified

---

## Support and Resources

- **Django Deployment:** https://docs.djangoproject.com/en/stable/howto/deployment/
- **Heroku Django Guide:** https://devcenter.heroku.com/articles/django-app-configuration
- **AWS EC2 Tutorial:** https://docs.aws.amazon.com/ec2/
- **DigitalOcean Tutorials:** https://www.digitalocean.com/community/tutorials
- **Django Security:** https://docs.djangoproject.com/en/stable/topics/security/

---

## Conclusion

Your Social Media API is now production-ready! Choose the deployment method that best fits your needs:

- **Heroku:** Fastest, easiest, great for MVPs
- **AWS:** Most scalable, enterprise-grade
- **DigitalOcean:** Balance of simplicity and control
- **Manual Server:** Full control, cost-effective

For questions or issues, refer to the troubleshooting section or consult the official Django documentation.

**Happy Deploying! 🚀**
