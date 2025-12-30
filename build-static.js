#!/usr/bin/env node

/**
 * Build script for Vercel deployment
 * Collects static files and prepares the project for deployment
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔨 Building Akonsec School Website for Vercel...\n');

// Step 1: Create dist directory structure
console.log('📁 Creating distribution directory...');
const distDir = path.join(__dirname, 'dist');
const publicDir = path.join(distDir, 'public');
const staticDir = path.join(publicDir, 'static');

if (fs.existsSync(distDir)) {
    fs.rmSync(distDir, { recursive: true });
}

fs.mkdirSync(distDir, { recursive: true });
fs.mkdirSync(publicDir, { recursive: true });
fs.mkdirSync(staticDir, { recursive: true });

// Step 2: Copy static files
console.log('📋 Copying static files...');
const sourceStaticDir = path.join(__dirname, 'static');
if (fs.existsSync(sourceStaticDir)) {
    copyDir(sourceStaticDir, staticDir);
    console.log('✅ Static files copied');
} else {
    console.log('⚠️  No static directory found');
}

// Step 3: Copy staticfiles (collected Django static files)
console.log('📋 Copying collected Django static files...');
const sourceStaticFilesDir = path.join(__dirname, 'staticfiles');
if (fs.existsSync(sourceStaticFilesDir)) {
    copyDir(sourceStaticFilesDir, path.join(publicDir, 'staticfiles'));
    console.log('✅ Django static files copied');
} else {
    console.log('⚠️  No staticfiles directory found');
}

// Step 4: Render Django templates to static HTML
console.log('📄 Rendering Django templates to static HTML...');
try {
    // Try to run Django management command to render templates
    execSync('python manage.py render_static --output dist/public', { 
        stdio: 'inherit',
        cwd: __dirname 
    });
    console.log('✅ Templates rendered');
} catch (error) {
    console.log('⚠️  Could not render templates (Django may not be available during build)');
    console.log('   Make sure to run: python manage.py render_static before deploying');
    
    // Create index.html if it doesn't exist
    const indexPath = path.join(publicDir, 'index.html');
    if (!fs.existsSync(indexPath)) {
        console.log('📄 Creating fallback index.html...');
        fs.writeFileSync(indexPath, `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Akonsec School Website</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>Akonsec School Website</h1>
    <p>Powered by Django & Vercel</p>
    <script src="/static/js/programs.js"></script>
</body>
</html>`);
        console.log('✅ Created fallback index.html');
    }
}

// Step 5: Ensure all HTML files are present
console.log('📄 Verifying HTML files...');
const htmlFiles = ['index.html', 'about.html', 'programs.html', 'news.html', 'student_life.html', 'gallery.html', 'contact.html'];
htmlFiles.forEach(file => {
    const filePath = path.join(publicDir, file);
    if (!fs.existsSync(filePath)) {
        console.log(`⚠️  Missing ${file} - make sure to run: python manage.py render_static`);
    }
});

// Step 6: Build complete
console.log('✅ Static site build complete');

console.log('\n✨ Build complete! Ready for Vercel deployment.\n');
console.log('Next steps:');
console.log('1. Push your changes to Git');
console.log('2. Connect your repository to Vercel');
console.log('3. Deploy from the Vercel dashboard\n');

/**
 * Recursively copy directory
 */
function copyDir(src, dest) {
    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
    }

    const files = fs.readdirSync(src);
    files.forEach(file => {
        const srcPath = path.join(src, file);
        const destPath = path.join(dest, file);

        if (fs.lstatSync(srcPath).isDirectory()) {
            copyDir(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    });
}
