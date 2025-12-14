# Docker Deployment Guide

This guide explains how to run the Social Media API using Docker and Docker Compose.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

Install Docker: https://docs.docker.com/get-docker/

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/social_media_api.git
cd social_media_api
```

### 2. Create Environment File
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 3. Build and Start Services
```bash
# Build images
docker-compose build

# Start all services (database, web, nginx)
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Run Migrations
```bash
docker-compose exec web python manage.py migrate
```

### 5. Create Superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Access the Application
- **API:** http://localhost/api/
- **Admin:** http://localhost/admin/
- **Documentation:** http://localhost/api/docs/ (if enabled)

## Docker Commands

### Service Management
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx
```

### Execute Commands
```bash
# Django management commands
docker-compose exec web python manage.py <command>

# Django shell
docker-compose exec web python manage.py shell

# Database shell
docker-compose exec web python manage.py dbshell

# PostgreSQL shell
docker-compose exec db psql -U social_media_user -d social_media_db
```

### Database Operations
```bash
# Create migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Backup database
docker-compose exec db pg_dump -U social_media_user social_media_db > backup.sql

# Restore database
docker-compose exec -T db psql -U social_media_user social_media_db < backup.sql
```

### Static Files
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

## Architecture

```
┌─────────────────┐
│     Client      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Nginx (Port 80)│
│  Reverse Proxy  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Django + Gunicorn│
│   (Port 8000)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │
│   (Port 5432)   │
└─────────────────┘
```

## Services

### Web (Django Application)
- **Image:** Built from Dockerfile
- **Port:** 8000 (internal), 80 (via Nginx)
- **Command:** Gunicorn WSGI server
- **Health Check:** HTTP request to /api/

### Database (PostgreSQL)
- **Image:** postgres:15-alpine
- **Port:** 5432
- **Volume:** postgres_data (persistent)
- **Health Check:** pg_isready

### Nginx (Reverse Proxy)
- **Image:** nginx:alpine
- **Port:** 80, 443
- **Purpose:** Serves static files, proxies to Django
- **Volumes:** static_volume, media_volume

## Volumes

- **postgres_data:** Database persistence
- **static_volume:** Django static files
- **media_volume:** User-uploaded media

## Environment Variables

Configure in `.env` or `docker-compose.yml`:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | (required) |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` |
| `DATABASE_URL` | Database connection | PostgreSQL in Docker |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` |

## Production Deployment

### 1. Update Environment
```env
SECRET_KEY=<strong-random-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### 2. Configure SSL (Let's Encrypt)
Update `docker-compose.yml` to add Certbot:

```yaml
certbot:
  image: certbot/certbot
  volumes:
    - ./certbot/conf:/etc/letsencrypt
    - ./certbot/www:/var/www/certbot
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

Update nginx service to mount SSL certificates:
```yaml
nginx:
  volumes:
    - ./certbot/conf:/etc/letsencrypt
    - ./certbot/www:/var/www/certbot
```

### 3. Obtain SSL Certificate
```bash
docker-compose run --rm certbot certonly --webroot \
  --webroot-path=/var/www/certbot \
  -d yourdomain.com -d www.yourdomain.com
```

### 4. Deploy
```bash
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py createsuperuser
```

## Monitoring

### Health Checks
All services have health checks configured:
```bash
docker-compose ps
```

Healthy output:
```
NAME                IMAGE               STATUS
social_media_api    app:latest          Up (healthy)
social_media_db     postgres:15-alpine  Up (healthy)
social_media_nginx  nginx:alpine        Up (healthy)
```

### Resource Usage
```bash
# View resource usage
docker stats

# View disk usage
docker system df
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs web

# Check configuration
docker-compose config

# Rebuild image
docker-compose build --no-cache web
```

### Database connection error
```bash
# Check database status
docker-compose ps db

# Check database logs
docker-compose logs db

# Verify database exists
docker-compose exec db psql -U social_media_user -l
```

### Static files not loading
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check Nginx logs
docker-compose logs nginx

# Verify volume mounts
docker volume inspect social_media_api_static_volume
```

### Permission errors
```bash
# Fix ownership
docker-compose exec -u root web chown -R appuser:appuser /app
```

### Reset everything
```bash
# Stop and remove all containers, networks, volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Clean Docker system
docker system prune -a --volumes
```

## Performance Tuning

### Increase Workers
Edit `docker-compose.yml`:
```yaml
web:
  command: gunicorn --bind 0.0.0.0:8000 --workers 5 social_media_api.wsgi:application
```

### Database Connection Pooling
Install pgbouncer:
```yaml
pgbouncer:
  image: edoburu/pgbouncer
  environment:
    - DATABASE_URL=postgres://social_media_user:changeme123@db/social_media_db
    - POOL_MODE=transaction
    - MAX_CLIENT_CONN=100
  ports:
    - "6432:5432"
```

### Redis Cache (Optional)
Add Redis service:
```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
```

Update Django settings to use Redis for caching.

## CI/CD with Docker

### GitHub Actions Example
```yaml
name: Docker Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t social-media-api .
      - name: Run tests
        run: docker-compose run web python manage.py test
      - name: Deploy
        run: |
          # Your deployment commands
```

## Best Practices

1. **Never commit `.env` files** - Use `.env.example` as template
2. **Use secrets management** - For production, use Docker Secrets or cloud provider secrets
3. **Regular backups** - Automate database backups
4. **Monitor logs** - Use centralized logging (ELK, Splunk, CloudWatch)
5. **Update images** - Keep base images up to date for security patches
6. **Resource limits** - Set memory and CPU limits in production
7. **Health checks** - Ensure all services have health checks
8. **Multi-stage builds** - Optimize Dockerfile for smaller images

## Additional Resources

- **Docker Documentation:** https://docs.docker.com/
- **Docker Compose Documentation:** https://docs.docker.com/compose/
- **Django Docker Guide:** https://docs.djangoproject.com/en/stable/howto/deployment/
- **Nginx Docker:** https://hub.docker.com/_/nginx
- **PostgreSQL Docker:** https://hub.docker.com/_/postgres

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Review troubleshooting section above
3. Consult main DEPLOYMENT.md
4. Open an issue on GitHub

---

**Happy Dockerizing! 🐳**
