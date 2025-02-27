"""
Emergency fixes for deployment issues
"""
import os

from lscms.lscms.settings.base import INSTALLED_APPS, MIDDLEWARE

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
