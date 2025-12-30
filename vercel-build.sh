#!/bin/bash
# Build script for Vercel deployment
# This script collects static files before deployment

echo "🔨 Building Django project for Vercel..."

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build complete!"

