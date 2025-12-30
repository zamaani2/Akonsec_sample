# Vercel Deployment Guide for Akonsec School Website

This guide will help you deploy your Django-based school website to Vercel.

## Prerequisites

- Vercel account (https://vercel.com)
- Git repository (GitHub, GitLab, or Bitbucket)
- Python 3.11+ (Vercel will use Python 3.11 automatically)
- External database (recommended: PostgreSQL via Vercel Postgres, Supabase, or Railway)

## Important Notes

⚠️ **Database Configuration**: Vercel serverless functions are stateless. You'll need an external database:
- **Recommended**: Use Vercel Postgres, Supabase, or Railway for PostgreSQL
- Update `DATABASE_URL` environment variable in Vercel dashboard
- SQLite (db.sqlite3) will NOT work in production on Vercel

## Deployment Steps

### 1. Prepare Your Project

```bash
# Collect Django static files (this runs automatically during build)
python manage.py collectstatic --noinput

# Ensure all dependencies are in requirements.txt
pip freeze > requirements.txt
```

### 2. Set Up External Database (Required)

1. **Create a PostgreSQL database**:
   - Option A: Vercel Postgres (recommended)
     - Go to Vercel Dashboard → Storage → Create Database → Postgres
   - Option B: Supabase (free tier available)
     - Go to https://supabase.com and create a project
   - Option C: Railway, Render, or other providers

2. **Get your database connection string**:
   - Format: `postgresql://user:password@host:port/database`
   - Or use the connection URL provided by your provider

### 3. Push to Git Repository

```bash
# Stage all changes
git add .

# Commit
git commit -m "Prepare for Vercel deployment"

# Push to your repository
git push -u origin main
```

### 4. Deploy to Vercel

#### Option A: Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy (follow prompts)
vercel

# For production deployment
vercel --prod
```

#### Option B: Using Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your Git repository
4. Vercel will auto-detect the configuration from `vercel.json`
5. Click "Deploy"

### 5. Set Environment Variables

In Vercel Dashboard → Your Project → Settings → Environment Variables:

**Required Variables:**
- `DJANGO_SETTINGS_MODULE`: `school_website.settings`
- `DEBUG`: `False`
- `SECRET_KEY`: Generate a secure secret key (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DATABASE_URL`: Your PostgreSQL connection string
- `ALLOWED_HOSTS`: `*.vercel.app,*.vercel.sh,yourdomain.com` (add your custom domain if applicable)

**Optional Variables:**
- `PYTHONUNBUFFERED`: `1` (already set in vercel.json)

### 6. Run Database Migrations

After first deployment, run migrations:

```bash
# Using Vercel CLI
vercel env pull .env.local
python manage.py migrate

# Or use Vercel's function logs to run migrations
# You may need to create a management command or use Django admin
```

**Alternative**: Create a one-time migration script or use Vercel's function to run migrations programmatically.

### 7. Verify Deployment

After deployment:
- Visit your Vercel URL (e.g., `https://your-project.vercel.app`)
- Check that static files are loading (CSS, JS, images)
- Verify all pages are accessible
- Test the admin panel at `/admin/`
- Check function logs in Vercel Dashboard for any errors

## Project Structure

The deployment is configured with:

- **API Handler**: `api/index.py` - Serverless function that handles all Django requests
- **Static Files**: Served from `/staticfiles/` (collected via `collectstatic`)
- **Media Files**: Served from `/media/` (if using file uploads)
- **Configuration**: `vercel.json` - Routing and build configuration

## Configuration Files

- `vercel.json` - Vercel deployment configuration (routing, builds, env vars)
- `.vercelignore` - Files to exclude from deployment
- `api/index.py` - Python serverless function entry point (handles all Django requests)
- `requirements.txt` - Python dependencies
- `package.json` - Node.js project metadata (for build scripts)

## Troubleshooting

### Static Files Not Loading
- Ensure `collectstatic` runs during build (check build logs)
- Verify static files are in `staticfiles/` directory
- Check that routes in `vercel.json` correctly map `/static/` to `/staticfiles/`
- Verify `STATIC_ROOT` and `STATIC_URL` in settings.py

### Python Import Errors
- Check `requirements.txt` includes all dependencies
- Ensure Python version matches (Vercel uses Python 3.11)
- Verify environment variables are set correctly
- Check function logs in Vercel Dashboard for detailed error messages

### Build Failures
- Check build logs in Vercel Dashboard
- Verify `DJANGO_SETTINGS_MODULE` is set correctly
- Ensure `requirements.txt` is in the root directory
- Check that all Python dependencies are compatible with Python 3.11

### Database Connection Issues
- Verify `DATABASE_URL` environment variable is set correctly
- Ensure database is accessible from Vercel's IP ranges
- Check database connection string format
- Verify database migrations have been run

### Function Timeout Errors
- Default timeout is 30 seconds (configured in vercel.json)
- For longer operations, consider using background jobs
- Optimize database queries and reduce response time

### 500 Internal Server Error
- Check function logs in Vercel Dashboard
- Verify `SECRET_KEY` is set
- Ensure `ALLOWED_HOSTS` includes your Vercel domain
- Check that database is properly configured

## Next Steps

### Performance Optimization
- Enable Vercel Analytics
- Configure caching headers
- Optimize images
- Minify CSS/JS

### Custom Domain
1. In Vercel Dashboard, go to Settings → Domains
2. Add your custom domain
3. Update DNS records with your registrar

### SSL Certificate
- Vercel automatically provides free SSL certificates
- No additional configuration needed

## Support

For more information:
- Vercel Docs: https://vercel.com/docs
- Django Documentation: https://docs.djangoproject.com
- Contact: support@akonsec.edu

---

Last Updated: 2025-12-26
