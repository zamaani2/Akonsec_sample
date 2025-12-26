#!/bin/bash

# Exit on error
set -o errexit

# Use Python 3.11 to avoid compatibility issues
export PYTHON_VERSION=3.11.4
export PATH="/opt/render/project/python/bin:${PATH}"

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate 