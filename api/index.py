"""
Vercel serverless function to run Django on Vercel
"""
import sys
import os
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
