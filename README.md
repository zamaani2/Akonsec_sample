# School Website

A Django-based school management system with comprehensive features for student, teacher, and course management.

## Features

- Student management
- Course enrollment
- Teacher profiles
- Assignment tracking
- Responsive design with Bootstrap 5
- Authentication and authorization

## Tech Stack

- Django 5.0.3
- PostgreSQL (in production)
- Bootstrap 5.3.0
- Gunicorn (WSGI server)
- WhiteNoise (static file serving)

## Local Development

### Prerequisites

- Python 3.11+ (recommended)
- Git
- PostgreSQL (optional, can use SQLite for development)

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd school_website
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

## Deployment to Render

This project is configured for easy deployment to [Render](https://render.com/).

### Automatic Deployment

1. Fork or clone this repository to your GitHub account.
2. Sign up for a Render account.
3. Create a new "Blueprint" on Render and connect to your GitHub repository.
4. Render will automatically detect the `render.yaml` file and set up the services.

### Manual Deployment

1. Create a new Web Service on Render.
2. Connect to your GitHub repository.
3. Use the following settings:
   - **Environment**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn school_website.wsgi:application`
   
4. Add the following environment variables:
   - `DEBUG=False`
   - `SECRET_KEY` (generate a secure key)
   - `ALLOWED_HOSTS=.onrender.com,your-app-name.onrender.com`
   - `RENDER=true`

5. Add a new PostgreSQL database and get the connection string.
6. Add `DATABASE_URL` environment variable with the connection string.

## Environment Variables

- `DEBUG`: Set to "True" for development, "False" for production
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string (Render will set this automatically if using their PostgreSQL)
- `RENDER`: Set to "true" when deploying to Render

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Django team for the amazing framework
- Bootstrap for the responsive design components
- Render.com for hosting 