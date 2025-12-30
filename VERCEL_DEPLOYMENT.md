# Vercel Deployment Guide for Akonsec School Website

This guide will help you deploy your Django-based school website to Vercel.

## Prerequisites

- Vercel account (https://vercel.com)
- Git repository (GitHub, GitLab, or Bitbucket)
- Python 3.11+ (Vercel will use Python 3.11 automatically)
- External database (recommended: PostgreSQL via Vercel Postgres, Supabase, or Railway)

## Important Notes

✅ **Static Website**: This is a static website deployment - no database or serverless functions needed!
- All pages are pre-rendered as static HTML files
- Static files (CSS, JS, images) are served directly
- No backend server required

## Deployment Steps

### 1. Prepare Your Project

```bash
# Collect Django static files (this runs automatically during build)
python manage.py collectstatic --noinput

# Ensure all dependencies are in requirements.txt
pip freeze > requirements.txt
```

### 2. Generate Static HTML Files

Before deploying, render your Django templates to static HTML:

```bash
# Render all templates to static HTML files
python manage.py render_static

# This will create HTML files in dist/public/
# - home.html → index.html
# - about.html, programs.html, news.html, etc.
```

### 3. Push to Git Repository

```bash
# Stage all changes
git add .

# Commit
git commit -m "Prepare for Vercel deployment"

# Push to your repository
git push -u origin main
```

### 4. Build Static Site

```bash
# Build the static site (copies static files and HTML)
npm run build
```

### 5. Deploy to Vercel

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

### 6. Set Environment Variables (Optional)

For a static site, no environment variables are required! However, if you want to customize the build:

**Optional Variables:**
- None required for static deployment

### 7. Verify Deployment

After deployment:
- Visit your Vercel URL (e.g., `https://your-project.vercel.app`)
- Check that static files are loading (CSS, JS, images)
- Verify all pages are accessible
- Test the admin panel at `/admin/`
- Check function logs in Vercel Dashboard for any errors

## Project Structure

The deployment is configured with:

- **Static HTML Files**: Pre-rendered HTML in `dist/public/`
- **Static Assets**: CSS, JS, images served from `/static/`
- **Build Output**: `dist/public/` - This is what Vercel serves
- **Configuration**: `vercel.json` - Static site configuration

## Configuration Files

- `vercel.json` - Vercel static site configuration
- `.vercelignore` - Files to exclude from deployment
- `build-static.js` - Build script that prepares static files
- `package.json` - Node.js project metadata and build scripts
- `school/management/commands/render_static.py` - Django command to render templates

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

### Pages Not Loading
- Ensure `python manage.py render_static` was run before deployment
- Check that HTML files exist in `dist/public/`
- Verify `vercel.json` has correct `outputDirectory` set to `dist/public`

### Static Files Not Loading
- Ensure static files are in `dist/public/static/` after build
- Check that routes in `vercel.json` correctly map `/static/` paths
- Verify file paths in HTML templates use `/static/` prefix

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
