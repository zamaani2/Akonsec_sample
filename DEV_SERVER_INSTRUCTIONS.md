# Development Server Instructions

This document provides simple instructions for running the Django development server.

## Running the Development Server

You can run the development server in two ways:

### Method 1: Using Django's runserver command

```bash
python manage.py runserver
```

This will start the development server on the default port 8000.

### Method 2: Using the run_dev_server.py script

```bash
python run_dev_server.py
```

This script provides a convenient way to start the development server with DEBUG set to True.

To run the server on a different port:

```bash
python run_dev_server.py 8080
```

## Accessing Your Site

Once the server is running, you can access your site at:

http://127.0.0.1:8000/ (or the port you specified)

## Configuration

The application is configured to run in development mode with DEBUG=True.

### Production Deployment

For production deployment, we have provided a separate settings file:

```bash
# Use the production settings
python manage.py runserver --settings=school_website.production_settings
```

When deploying to production, you need to:

1. Set the following environment variables:
   - SECRET_KEY: Your Django secret key
   - ALLOWED_HOSTS: Comma-separated list of allowed hosts
   - DATABASE_URL: (Optional) Database connection URL for PostgreSQL

2. Run with the production settings:
   ```bash
   DJANGO_SETTINGS_MODULE=school_website.production_settings gunicorn school_website.wsgi
   ```

3. Configure a production-ready web server like Nginx or Apache

## Checking Settings

You can check your Django settings with:

```bash
python manage.py check_http_settings
```

This will show basic information about your Django configuration.

## Troubleshooting

If you encounter issues with the development server:

1. Make sure no other application is using the same port
2. Check the console output for any error messages
3. Verify that all required dependencies are installed 