# Django Project - Tidal Hack

A Django web application for managing and processing tidal data.

## Features

- 🚀 **Django** - Robust Python web framework
- 🗄️ **Database Support** - Built-in ORM for database management
- 🔐 **Security** - Django's built-in security features
- 🎯 **Admin Interface** - Built-in Django admin panel
- 🔧 **Modular Apps** - Organized app-based architecture

## Project Structure

```
├── manage.py          # Django management script
├── TidalHack/         # Project configuration package
│   ├── __init__.py
│   ├── asgi.py        # ASGI configuration
│   ├── settings.py    # Project settings
│   ├── urls.py        # URL routing
│   └── wsgi.py        # WSGI configuration
└── README.md          # This file
```

## Installation

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install django
```

## Development

Start the development server:

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`.

## Database

Run migrations to set up the database:

```bash
python manage.py migrate
```

Create a superuser for the admin panel:

```bash
python manage.py createsuperuser
```

## Getting Started

1. Update `TidalHack/settings.py` with your project configuration
2. Create Django apps using `python manage.py startapp appname`
3. Define models in your app's `models.py`
4. Create views and URL routes for your application
5. Access the admin panel at `http://localhost:8000/admin`

## Deployment

For production deployment:

```bash
python manage.py collectstatic
```

Configure your web server (Gunicorn, uWSGI, etc.) to serve the WSGI application in `TidalHack/wsgi.py`.

## Learn More

- [Django Documentation](https://docs.djangoproject.com)
- [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)