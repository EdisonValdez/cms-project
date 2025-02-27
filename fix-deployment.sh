#!/bin/bash
# Run this script locally before pushing to GitHub
# It will set up a temporary solution until you can properly fix the settings

# 1. Modify your production.py file to import the fixes module
echo "
# Add this at the end of your production.py file
try:
    from .fixes import *
except ImportError:
    pass
" >> lscms/lscms/settings/production.py

# 2. Create the fixes.py file in your settings directory
cat > lscms/lscms/settings/fixes.py << 'EOL'
"""
Emergency fixes for deployment issues
"""
import os

# Force different URLs for static and media
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Make sure staticfiles app is included
if 'django.contrib.staticfiles' not in INSTALLED_APPS:
    INSTALLED_APPS.append('django.contrib.staticfiles')

# Make sure whitenoise is configured properly
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Add Wagtail settings
WAGTAILADMIN_STATIC_FILE_VERSION_STRINGS = True

# Set static root
import inspect
import pathlib
current_file = inspect.getfile(inspect.currentframe())
current_dir = pathlib.Path(current_file).resolve().parent
SETTINGS_DIR = current_dir
BASE_DIR = SETTINGS_DIR.parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Debug information
print(f"Static URL: {STATIC_URL}")
print(f"Media URL: {MEDIA_URL}")
print(f"Static Root: {STATIC_ROOT}")
print(f"Base Dir: {BASE_DIR}")
EOL

# 3. Create placeholder health check URL (if it doesn't exist)
if ! grep -q "def health_check" lscms/lscms/urls.py; then
  sed -i '1i\from django.http import HttpResponse\n\ndef health_check(request):\n    """Health check endpoint for DigitalOcean App Platform."""\n    return HttpResponse("OK", status=200)\n' lscms/lscms/urls.py
  sed -i '/urlpatterns = $/a\    path("health/", health_check, name="health_check"),' lscms/lscms/urls.py
fi

# 4. Create a .gitignore to exclude local development files
cat > .gitignore << 'EOL'
*.pyc
__pycache__/
*.py[cod]
*$py.class
*.so
.env
env/
venv/
ENV/
env.bak/
venv.bak/
db.sqlite3
media/
.DS_Store
EOL

# 5. Add, commit and push changes to GitHub
git add -A
git commit -m "Add emergency fixes for deployment"
git push origin main

echo "Changes committed and pushed to GitHub. Configure DigitalOcean app platform to disable collectstatic or use the updated app spec."
