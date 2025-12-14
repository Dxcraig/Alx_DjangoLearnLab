# Production Deployment Checklist

Use this checklist to ensure your Social Media API is production-ready before deployment.

## Pre-Deployment Configuration

### Django Settings
- [ ] `DEBUG = False` in production environment
- [ ] Strong `SECRET_KEY` set (50+ random characters)
- [ ] `ALLOWED_HOSTS` configured with production domains
- [ ] Database configured (`DATABASE_URL` with PostgreSQL)
- [ ] Static files configuration (`STATIC_ROOT`, `STATIC_URL`)
- [ ] Media files configuration (`MEDIA_ROOT`, `MEDIA_URL`)
- [ ] CORS settings configured for frontend domains

### Environment Variables
- [ ] `.env` file created (never commit this!)
- [ ] `SECRET_KEY` set in environment
- [ ] `DEBUG` set to `False`
- [ ] `ALLOWED_HOSTS` set with domains
- [ ] `DATABASE_URL` configured
- [ ] `CORS_ALLOWED_ORIGINS` set
- [ ] All sensitive data moved to environment variables

### Database
- [ ] PostgreSQL database created
- [ ] Database user and password configured
- [ ] Database URL accessible from application server
- [ ] All migrations applied: `python manage.py migrate`
- [ ] Superuser created: `python manage.py createsuperuser`
- [ ] Test database connection works

### Dependencies
- [ ] All requirements installed: `pip install -r requirements.txt`
- [ ] Production packages included:
  - [ ] `gunicorn` (WSGI server)
  - [ ] `psycopg2-binary` (PostgreSQL adapter)
  - [ ] `whitenoise` (static files)
  - [ ] `dj-database-url` (database configuration)
  - [ ] `python-decouple` or `python-dotenv` (environment variables)

### Static and Media Files
- [ ] Static files collected: `python manage.py collectstatic --noinput`
- [ ] `STATIC_ROOT` directory exists and is writable
- [ ] `MEDIA_ROOT` directory exists and is writable
- [ ] WhiteNoise middleware configured in `MIDDLEWARE`
- [ ] Consider cloud storage (AWS S3) for media files in production

## Security Configuration

### Django Security Settings
- [ ] `SECRET_KEY` is random and never committed to version control
- [ ] `DEBUG = False` in production
- [ ] `SECURE_SSL_REDIRECT = True` (enforce HTTPS)
- [ ] `SECURE_HSTS_SECONDS = 31536000` (HSTS enabled)
- [ ] `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- [ ] `SECURE_HSTS_PRELOAD = True`
- [ ] `SESSION_COOKIE_SECURE = True` (cookies over HTTPS only)
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `X_FRAME_OPTIONS = 'DENY'` (prevent clickjacking)
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF = True`
- [ ] `SECURE_BROWSER_XSS_FILTER = True`

### SSL/TLS Certificate
- [ ] SSL certificate obtained (Let's Encrypt recommended)
- [ ] Certificate installed on web server
- [ ] HTTPS working on all domains
- [ ] HTTP redirects to HTTPS
- [ ] Certificate auto-renewal configured

### CORS Configuration
- [ ] `django-cors-headers` installed
- [ ] `CORS_ALLOWED_ORIGINS` set with frontend URLs
- [ ] `CORS_ALLOW_CREDENTIALS = True` (if using cookies)
- [ ] `CORS_ALLOW_ALL_ORIGINS = False` in production

### Authentication & Authorization
- [ ] Token authentication configured
- [ ] Strong password requirements enforced
- [ ] Rate limiting considered (django-ratelimit)
- [ ] API endpoints require authentication where appropriate
- [ ] Permissions properly configured on ViewSets

## Infrastructure Setup

### Server Configuration (if using VPS/EC2)
- [ ] Server OS updated: `sudo apt update && sudo apt upgrade`
- [ ] Required packages installed (Python, Nginx, PostgreSQL, Supervisor)
- [ ] Firewall configured (UFW on Ubuntu):
  - [ ] SSH (port 22) allowed from specific IPs
  - [ ] HTTP (port 80) allowed
  - [ ] HTTPS (port 443) allowed
  - [ ] PostgreSQL (port 5432) restricted to localhost

### Gunicorn Configuration
- [ ] Gunicorn installed: `pip install gunicorn`
- [ ] Gunicorn tested manually: `gunicorn social_media_api.wsgi:application`
- [ ] Gunicorn socket file location configured
- [ ] Number of workers configured (2-4 per CPU core)
- [ ] Process managed by Supervisor or systemd

### Nginx Configuration
- [ ] Nginx installed: `sudo apt install nginx`
- [ ] Nginx configuration file created in `/etc/nginx/sites-available/`
- [ ] Symbolic link created in `/etc/nginx/sites-enabled/`
- [ ] Static files location configured
- [ ] Media files location configured
- [ ] Proxy pass to Gunicorn configured
- [ ] Client max body size set (for file uploads)
- [ ] Nginx tested: `sudo nginx -t`
- [ ] Nginx restarted: `sudo systemctl restart nginx`

### Process Management (Supervisor)
- [ ] Supervisor installed: `sudo apt install supervisor`
- [ ] Supervisor config created for Gunicorn
- [ ] Supervisor updated: `sudo supervisorctl reread && sudo supervisorctl update`
- [ ] Application started: `sudo supervisorctl start social_media_api`
- [ ] Auto-restart configured

### Domain and DNS
- [ ] Domain name purchased
- [ ] DNS A records configured:
  - [ ] `@` (root domain) points to server IP
  - [ ] `www` subdomain points to server IP
- [ ] DNS propagation verified (can take 24-48 hours)
- [ ] Domain accessible via browser

## Deployment-Specific Checklists

### Heroku Deployment
- [ ] Heroku account created
- [ ] Heroku CLI installed
- [ ] App created: `heroku create app-name`
- [ ] PostgreSQL addon added: `heroku addons:create heroku-postgresql:mini`
- [ ] Environment variables set: `heroku config:set KEY=value`
- [ ] `Procfile` created with web and release commands
- [ ] `runtime.txt` created with Python version
- [ ] Git repository pushed: `git push heroku main`
- [ ] Migrations run: `heroku run python manage.py migrate`
- [ ] Superuser created: `heroku run python manage.py createsuperuser`

### AWS Deployment (EC2 + RDS)
- [ ] EC2 instance launched (Ubuntu 22.04)
- [ ] Security groups configured (SSH, HTTP, HTTPS)
- [ ] Elastic IP allocated and associated
- [ ] RDS PostgreSQL instance created
- [ ] RDS security group allows EC2 access
- [ ] Application deployed to `/var/www/`
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Gunicorn, Nginx, Supervisor configured
- [ ] SSL certificate installed (Let's Encrypt)

### DigitalOcean App Platform
- [ ] DigitalOcean account created
- [ ] GitHub repository connected
- [ ] Build command configured
- [ ] Run command configured (gunicorn)
- [ ] Environment variables set
- [ ] Database component added (Managed PostgreSQL)
- [ ] App deployed automatically
- [ ] Custom domain configured (optional)

## Testing and Validation

### Functional Testing
- [ ] Homepage loads successfully
- [ ] API endpoints respond correctly
- [ ] User registration works
- [ ] User login works
- [ ] Token authentication works
- [ ] CRUD operations on posts work
- [ ] CRUD operations on comments work
- [ ] Like/Unlike functionality works
- [ ] Follow/Unfollow functionality works
- [ ] Feed displays followed users' posts
- [ ] Notifications system works
- [ ] Admin panel accessible at `/admin/`

### Performance Testing
- [ ] API response times acceptable (<500ms)
- [ ] Database queries optimized (use Django Debug Toolbar in dev)
- [ ] Static files load quickly
- [ ] No N+1 query problems
- [ ] Load testing performed (consider using Locust or JMeter)

### Security Testing
- [ ] HTTPS working across all pages
- [ ] HTTP redirects to HTTPS
- [ ] Security headers present (use securityheaders.com)
- [ ] CORS policy enforced
- [ ] CSRF protection working
- [ ] SQL injection attempts blocked (Django ORM protects)
- [ ] XSS attempts blocked
- [ ] Rate limiting tested (if implemented)
- [ ] Sensitive data not exposed in error messages

### Browser Testing
- [ ] Site works in Chrome
- [ ] Site works in Firefox
- [ ] Site works in Safari
- [ ] Site works in Edge
- [ ] Mobile responsive (if applicable)

## Monitoring and Logging

### Application Logging
- [ ] Logging configured in `settings.py`
- [ ] Log files created in `logs/` directory
- [ ] Log rotation configured
- [ ] Error logs reviewed regularly
- [ ] Application logs accessible: `tail -f logs/django.log`

### Error Tracking
- [ ] Error tracking service configured (Sentry, Rollbar, etc.)
- [ ] Error notifications set up
- [ ] Error dashboard accessible
- [ ] Team members added to error tracking

### Performance Monitoring
- [ ] Application monitoring configured (New Relic, Datadog, etc.)
- [ ] Performance metrics tracked:
  - [ ] Response time
  - [ ] Request rate
  - [ ] Error rate
  - [ ] Database query time
- [ ] Alerts configured for critical issues

### Uptime Monitoring
- [ ] Uptime monitoring service configured (UptimeRobot, Pingdom, etc.)
- [ ] Ping checks every 5 minutes
- [ ] Email/SMS alerts configured
- [ ] Status page created (optional)

## Backup and Recovery

### Database Backups
- [ ] Automated daily backups configured
- [ ] Backup retention policy set (30 days recommended)
- [ ] Backups stored in secure location (S3, separate server)
- [ ] Database restore tested successfully
- [ ] Backup notifications configured

### Application Backups
- [ ] Code repository backed up (Git)
- [ ] Environment variables documented
- [ ] Static files backed up
- [ ] Media files backed up (if not using cloud storage)

### Disaster Recovery Plan
- [ ] Recovery procedures documented
- [ ] Recovery time objective (RTO) defined
- [ ] Recovery point objective (RPO) defined
- [ ] Team roles and responsibilities defined
- [ ] Recovery plan tested

## Documentation

### Technical Documentation
- [ ] API documentation complete (Swagger/OpenAPI)
- [ ] README.md updated with production info
- [ ] DEPLOYMENT.md guide complete
- [ ] Architecture diagram created
- [ ] Database schema documented

### Operational Documentation
- [ ] Deployment procedures documented
- [ ] Rollback procedures documented
- [ ] Troubleshooting guide created
- [ ] Contact information for team members
- [ ] Third-party service credentials documented (securely)

## Post-Deployment

### Immediate Actions (First 24 Hours)
- [ ] Monitor error logs continuously
- [ ] Check application performance metrics
- [ ] Verify all critical functionality works
- [ ] Test all API endpoints in production
- [ ] Monitor database performance
- [ ] Check SSL certificate is working
- [ ] Verify email notifications (if applicable)

### First Week
- [ ] Review error logs daily
- [ ] Monitor user feedback
- [ ] Check performance trends
- [ ] Verify backups are running
- [ ] Test disaster recovery procedure
- [ ] Update documentation based on issues found

### Ongoing Maintenance
- [ ] Weekly security updates: `sudo apt update && sudo apt upgrade`
- [ ] Monthly dependency updates: `pip list --outdated`
- [ ] Quarterly SSL certificate check
- [ ] Regular database optimization
- [ ] Review and rotate logs
- [ ] Performance optimization based on metrics

## Team Communication

### Pre-Deployment
- [ ] Deployment plan shared with team
- [ ] Deployment date/time scheduled
- [ ] Maintenance window communicated to users
- [ ] Rollback plan communicated

### During Deployment
- [ ] Team members on standby
- [ ] Status updates provided
- [ ] Issues escalated immediately

### Post-Deployment
- [ ] Deployment completion announced
- [ ] Known issues communicated
- [ ] Documentation updated
- [ ] Post-mortem meeting scheduled (if issues occurred)

---

## Quick Commands Reference

### Check Application Status
```bash
# Check if Gunicorn is running
ps aux | grep gunicorn

# Check Supervisor status
sudo supervisorctl status

# Check Nginx status
sudo systemctl status nginx

# Check PostgreSQL status
sudo systemctl status postgresql
```

### View Logs
```bash
# Application logs
tail -f logs/django.log

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Supervisor logs
sudo tail -f /var/log/social_media_api.err.log
```

### Restart Services
```bash
# Restart application (Supervisor)
sudo supervisorctl restart social_media_api

# Restart Nginx
sudo systemctl restart nginx

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Emergency Rollback
```bash
# Git rollback
git revert HEAD
git push heroku main

# Heroku rollback
heroku releases
heroku rollback v123

# Manual server rollback
cd /var/www/social_media_api
git pull origin previous-stable-branch
sudo supervisorctl restart social_media_api
```

---

## Completion Sign-Off

**Deployment Date:** _________________

**Deployed By:** _________________

**Production URL:** _________________

**Database:** _________________

**Checklist Completed:** ☐ Yes  ☐ No

**Notes:**
```
[Add any deployment-specific notes here]
```

---

**Congratulations! Your Social Media API is now live in production! 🎉**

Remember to monitor logs closely for the first 24-48 hours and address any issues promptly.
