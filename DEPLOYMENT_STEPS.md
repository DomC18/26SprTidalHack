# Deployment Steps - Food Security Analysis System

This guide includes step-by-step instructions to deploy your Django Food Security Analysis System to production on Render.com (recommended).

## Quick Deploy to Render (Recommended) ⭐

Render.com is free, simple, and requires no credit card for initial test deployment.

### Step 1: Prepare Your Code

1. **Initialize Git Repository** (if not already done):
```bash
cd ./TidalHack
git init
git add .
git commit -m "Initial commit: Food Security Analysis System"
```

2. **Create a `.env` file for local testing** (NOT for production):
```
DEBUG=False
SECRET_KEY=your-secret-key-here-generate-one
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

For production SECRET_KEY, use:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 2: Update Django Settings

Edit `TidalHack/settings.py`:

```python
# Near the top, add:
import os
from pathlib import Path

# Change DEBUG based on environment
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Update ALLOWED_HOSTS
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# Update SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# If using PostgreSQL in production, add this:
import dj_database_url
if os.getenv('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(default=os.getenv('DATABASE_URL'))
```

### Step 3: Create Render Configuration Files

**Create `render.yaml` in project root:**
```yaml
services:
  - type: web
    name: food-security-app
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt && cd TidalHack && python manage.py migrate && python manage.py collectstatic --noinput"
    startCommand: "cd TidalHack && gunicorn TidalHack.wsgi:application"
    envVars:
      - key: DEBUG
        value: "False"
      - key: SECRET_KEY
        generateValue: true
      - key: ALLOWED_HOSTS
        value: "food-security-app.onrender.com"
      - key: PYTHON_VERSION
        value: "3.11"
```

**Create `Procfile` in project root:**
```
web: cd TidalHack && gunicorn TidalHack.wsgi:application
release: cd TidalHack && python manage.py migrate && python manage.py collectstatic --noinput
```

### Step 4: Update Requirements

Ensure your `requirements.txt` includes:
```
Django==6.0.2
djangorestframework==3.14.0
gunicorn==21.2.0
whitenoise==6.6.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
python-dotenv==1.0.0
requests==2.31.0
numpy==1.24.3
scikit-learn==1.3.1
pandas==2.0.3
```

Run: `pip freeze > requirements.txt`

### Step 5: Push to GitHub

1. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Create repo (e.g., `food-security-analysis`)
   - Don't initialize with README

2. **Push Code**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/food-security-analysis.git
git branch -M main
git push -u origin main
```

### Step 6: Deploy on Render.com

1. **Go to https://render.com** and sign up (free)

2. **Create a New Web Service**:
   - Click "New +" > "Web Service"
   - Connect your GitHub account
   - Select the `food-security-analysis` repo
   - Name: `food-security-app`
   - Environment: Python 3
   - Build Command: 
     ```
     pip install -r requirements.txt && cd TidalHack && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - Start Command:
     ```
     cd TidalHack && gunicorn TidalHack.wsgi:application
     ```

3. **Set Environment Variables**:
   Click "Advanced" and add:
   - `DEBUG`: `False`
   - `SECRET_KEY`: Generate using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `ALLOWED_HOSTS`: `food-security-app.onrender.com`
   - `PYTHON_VERSION`: `3.11`

4. **Click "Create Web Service"**

5. **Wait for Deployment** (2-3 minutes):
   - Check the deploy log
   - Look for "Build successful" and "Service is running"

### Step 7: Verify Deployment

Once live, visit:
- Dashboard: `https://food-security-app.onrender.com/`
- API: `https://food-security-app.onrender.com/api/food-deserts/`
- Admin: `https://food-security-app.onrender.com/admin/`

### Step 8: Create First Admin User

In Render's shell:
```bash
cd TidalHack
python manage.py createsuperuser
# Follow prompts for username, email, password
```

Then visit `/admin/` with those credentials.

---

## Alternative: Deploy to Railway

Railway.app offers better free tier with PostgreSQL included.

1. Go to https://railway.app
2. Click "New Project" > "Deploy from GitHub"
3. Select your repo
4. Set environment variables (same as above)
5. Service auto-deploys when code is pushed

Environment variables:
- `DEBUG=False`
- `SECRET_KEY=[generate new]`
- `ALLOWED_HOSTS=yourapp.railway.app`

---

## Production Checklist ✓

- [ ] DEBUG=False in production
- [ ] SECRET_KEY is long and random (50+ chars)
- [ ] ALLOWED_HOSTS includes your domain
- [ ] Static files collected (`collectstatic`)
- [ ] Database migrations run (`migrate`)
- [ ] HTTPS/SSL enabled (Render/Railway do this automatically)
- [ ] Admin user created for data management
- [ ] Email configured (optional, for notifications)
- [ ] Backups configured (if using PostgreSQL)

---

## Troubleshooting

**502 Bad Gateway Error:**
- Check build logs for errors
- Verify environment variables are set
- Ensure gunicorn starts correctly

**Static Files Not Loading:**
- Run: `python manage.py collectstatic --noinput`
- Check whitenoise is in MIDDLEWARE
- Verify STATIC_ROOT is correct

**Database Connection Error:**
- Verify DATABASE_URL environment variable
- Ensure migrations ran successfully
- Check database credentials

**Admin Page Shows No CSS:**
- Run collectstatic again
- Clear browser cache
- Restart the service on Render

---

## Live Application URLs

Once deployed, your app will be live at:
- **Main App**: `https://food-security-app.onrender.com`
- **API Documentation**: `https://food-security-app.onrender.com/api/`
- **Admin Panel**: `https://food-security-app.onrender.com/admin/`

Share these URLs with stakeholders!

---

## Next Steps

1. Add actual food desert data via admin panel
2. Run analyses for each area
3. Export reports in PDF format (optional enhancement)
4. Set up monitoring/alerts (Render offers free Grafana)
5. Configure email notifications (SendGrid integration)

Happy deployment! 🚀
