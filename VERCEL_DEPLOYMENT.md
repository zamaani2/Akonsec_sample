# Vercel Deployment Guide for Akonsec School Website

This guide will help you deploy your Django-based school website to Vercel.

## Prerequisites

- Vercel account (https://vercel.com)
- Git repository (GitHub, GitLab, or Bitbucket)
- Node.js 18+ installed locally
- Python 3.11+

## Deployment Steps

### 1. Prepare Your Project

```bash
# Install Node dependencies
npm install

# Collect Django static files
python manage.py collectstatic --noinput

# Build the project for Vercel
npm run build
```

### 2. Push to Git Repository

```bash
# Stage all changes
git add .

# Commit
git commit -m "Prepare for Vercel deployment"

# Push to your repository
git push -u origin main
```

### 3. Deploy to Vercel

#### Option A: Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Follow the prompts to connect your Git repository
```

#### Option B: Using Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your Git repository
4. Configure project settings:
   - **Framework Preset**: Other
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Click "Deploy"

### 4. Set Environment Variables (if needed)

In Vercel Dashboard:
1. Go to your project settings
2. Click "Environment Variables"
3. Add any required variables:
   - `DEBUG`: false
   - `ALLOWED_HOSTS`: your-vercel-domain.vercel.app
   - `SECRET_KEY`: your-secret-key

### 5. Verify Deployment

After deployment:
- Visit your Vercel URL
- Check that static files are loading (CSS, JS, images)
- Verify all pages are accessible

## Project Structure

The deployment is configured with:

- **Static Files**: Served from `/static/` and `/staticfiles/`
- **API Routes**: Python backend functions in `/api/`
- **Public Directory**: HTML and assets in `/dist/public/`

## Configuration Files

- `vercel.json` - Vercel deployment configuration
- `.vercelignore` - Files to exclude from deployment
- `package.json` - Node.js project metadata and scripts
- `build-static.js` - Build script for preparing deployment
- `api/index.py` - Python serverless function entry point

## Troubleshooting

### Static Files Not Loading
- Ensure `npm run build` runs without errors
- Check that static files are in `dist/public/static/`
- Verify paths are correct in HTML templates

### Python Import Errors
- Check `requirements.txt` includes all dependencies
- Ensure Python version matches (3.11)
- Verify environment variables are set correctly

### Build Failures
- Check build logs in Vercel Dashboard
- Run `npm run build` locally to debug
- Verify all dependencies are in `requirements.txt`

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
