# Vercel Deployment - Quick Start

## Quick Deployment Steps

1. **Set up external database** (PostgreSQL required)
   - Use Vercel Postgres, Supabase, or Railway
   - Get your `DATABASE_URL`

2. **Set environment variables in Vercel Dashboard:**
   ```
   DJANGO_SETTINGS_MODULE=school_website.settings
   DEBUG=False
   SECRET_KEY=<generate-a-secure-key>
   DATABASE_URL=<your-postgres-connection-string>
   ALLOWED_HOSTS=*.vercel.app,*.vercel.sh
   ```

3. **Deploy:**
   ```bash
   # Using CLI
   vercel --prod
   
   # Or connect via GitHub in Vercel Dashboard
   ```

4. **Run migrations** (after first deployment):
   - Use Django admin or create a migration script
   - Or run locally with Vercel env vars: `vercel env pull .env.local`

## Files Created/Modified

- ✅ `api/index.py` - Serverless function handler
- ✅ `api/__init__.py` - Python package init
- ✅ `vercel.json` - Deployment configuration
- ✅ `.vercelignore` - Files to exclude
- ✅ `school_website/settings.py` - Updated for Vercel

## Important Notes

- ⚠️ SQLite won't work - use PostgreSQL
- ⚠️ Static files are auto-collected during build
- ⚠️ Function timeout is 30 seconds (configurable)
- ✅ All routes go through `api/index.py`

## Testing Locally

```bash
# Install Vercel CLI
npm install -g vercel

# Test locally
vercel dev
```

For detailed instructions, see `VERCEL_DEPLOYMENT.md`

