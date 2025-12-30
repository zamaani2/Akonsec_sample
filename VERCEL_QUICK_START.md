# Vercel Deployment - Quick Start

## Quick Deployment Steps

1. **Render Django templates to static HTML:**
   ```bash
   python manage.py render_static
   ```

2. **Build static site:**
   ```bash
   npm run build
   ```

3. **Deploy to Vercel:**
   ```bash
   # Using CLI
   vercel --prod
   
   # Or connect via GitHub in Vercel Dashboard
   ```

## Files Created/Modified

- ✅ `vercel.json` - Static site deployment configuration
- ✅ `.vercelignore` - Files to exclude
- ✅ `build-static.js` - Build script for static files
- ✅ `package.json` - Build scripts

## Important Notes

- ✅ **Static website** - No database needed!
- ✅ **No serverless functions** - Pure static HTML/CSS/JS
- ✅ Static files are copied during build
- ✅ All pages are pre-rendered HTML files

## Testing Locally

```bash
# Install Vercel CLI
npm install -g vercel

# Test locally
vercel dev
```

For detailed instructions, see `VERCEL_DEPLOYMENT.md`

