# Deployment Guide - Food Security Analysis System

## Quick Deployment Options

Choose your preferred platform:

### Option 1: Render (Recommended - Free Tier Available) ⭐

**Steps:**

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Connect GitHub repository
   - Create new Web Service
   - In Build Command: `pip install -r requirements.txt && cd TidalHack && python manage.py migrate && python manage.py collectstatic --noinput`
   - In Start Command: `cd TidalHack && gunicorn TidalHack.wsgi:application`

3. **Configure Environment**
   - Set `PYTHON_VERSION` to `3.10`
   - Add Environment Variables:
     ```
     DEBUG=False
     SECRET_KEY=generate-from-djecrety.ir
     ALLOWED_HOSTS=*.render.com
     ```

4. **Deploy**
   - Click Deploy
   - Your app will be live at: `https://your-app.onrender.com`

---

### Option 2: Railway (Free Credits)

1. Go to https://railway.app
2. Connect GitHub
3. Select repository
4. Add PostgreSQL plugin
5. Set environment variables
6. Deploy automatically

**Result**: Live at `https://<project>.up.railway.app`

---

### Option 3: Heroku (Paid)

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: cd TidalHack && gunicorn TidalHack.wsgi
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set SECRET_KEY=your-secret-key
   git push heroku main
   ```

---

### Option 4: PythonAnywhere (Simple)

1. Go to https://www.pythonanywhere.com
2. Upload files via Web interface
3. Configure WSGI file
4. Enable Web app
5. Get free `.pythonanywhere.com` domain

---

### Option 5: AWS (EC2)

1. Launch Ubuntu EC2 instance
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx supervisor postgresql
   pip install -r requirements.txt
   ```

3. Configure Gunicorn + Nginx
4. Set up SSL with Let's Encrypt
5. Domain via Route 53

---

## Pre-Deployment Checklist

Before deploying, ensure:

```bash
# 1. Test locally
python manage.py runserver

# 2. Create superuser
python manage.py createsuperuser

# 3. Run migrations
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Run tests
python manage.py test food_security
```

---

## Environment Variables

Create `.env` file (never commit):

```
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:5432/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

Generate SECRET_KEY:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use: https://djecrety.ir/

---

## Database Setup

### PostgreSQL (Production)

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb food_security_db

# Run migrations
python manage.py migrate --database production
```

### Use Managed Database

Most platforms offer managed PostgreSQL:
- Render: Add PostgreSQL resource
- Railway: Add PostgreSQL plugin
- AWS: RDS
- DigitalOcean: Managed Databases

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Free)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

### Nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Settings for Production

Update `settings.py`:

```python
# Security
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "style-src": ("'self'", "cdn.jsdelivr.net"),
    "script-src": ("'self'", "cdn.jsdelivr.net"),
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

---

## Monitoring & Maintenance

### Logs
```bash
# View application logs
heroku logs --tail
# or
docker logs container-id
```

### Database Backup
```bash
# PostgreSQL backup
pg_dump dbname > backup.sql

# Restore
psql dbname < backup.sql
```

### Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Run migrations after update
python manage.py migrate
```

---

## Performance Optimization

### Caching
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Static File CDN
Use CloudFront or any CDN:
```python
STATIC_URL = 'https://cdn.yourdomain.com/static/'
```

### Database Connection Pooling
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,
    }
}
```

---

## Troubleshooting

### 503 Service Unavailable
- Check logs: `heroku logs -t`
- Restart: `heroku restart`
- Check memory/resources

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database Connection Error
- Verify DATABASE_URL environment variable
- Check database credentials
- Ensure firewall allows connection

### High Memory Usage
- Check for memory leaks
- Reduce WORKER_CONNECTIONS
- Use celery for background tasks

---

## Deployment Summary

| Platform | Cost | Setup Time | SSL | Database |
|----------|------|-----------|-----|----------|
| Render | Free | 5 min | ✅ | ✅ |
| Railway | Free credits | 5 min | ✅ | ✅ |
| Heroku | Paid ($7+) | 10 min | ✅ | ✅ |
| PythonAnywhere | Free | 10 min | ✅ | ✅ |
| AWS | Pay as you go | 30 min | ✅ | ✅ |

**Recommendation**: Use **Render** for easiest deployment with free tier.

---

## Getting Help

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/6.0/howto/deployment/
- **Gunicorn**: https://gunicorn.org/
- **Nginx**: https://nginx.org/

## Next Steps

1. Choose a platform
2. Follow platform-specific instructions
3. Set up custom domain (optional)
4. Configure email notifications
5. Set up monitoring
6. Enable backups

Your Food Security Analysis System is now live! 🚀
