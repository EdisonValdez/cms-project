# LSOperations/lscms/lscms/settings/production.py

from .base import *
import os
import dj_database_url
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Production settings
DEBUG = False

# Get the domain from environment variables
ALLOWED_HOSTS = [
    os.environ.get('DJANGO_ALLOWED_HOST', '*'),
    '.ondigitalocean.app',
    'localsecrets.travel',
]

# Database settings
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }

# Add WhiteNoise middleware for static files
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configure AWS S3 for media files
if 'AWS_STORAGE_BUCKET_NAME' in os.environ:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'nyc3')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    # Check if using DigitalOcean Spaces
    if 'AWS_S3_ENDPOINT_URL' in os.environ:
        AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
        AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL.split('//')[1]}"
    else:
        AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN', f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com')
    
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    
    MEDIA_URL = os.environ.get('MEDIA_URL', f'https://{AWS_S3_CUSTOM_DOMAIN}/')
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

# Security settings - temporarily disabled for testing
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Wagtail specific settings
WAGTAILADMIN_STATIC_FILE_VERSION_STRINGS = True

# Uncomment these when you're ready for production-grade security
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Wagtail API settings
WAGTAILAPI_LIMIT_MAX = 100

# Get secret key from environment variable
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Make sure LOG_LEVEL is set
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'wagtail': {
            'handlers': ['console'],
            'level': os.environ.get('WAGTAIL_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

try:
    from .local import *
except ImportError:
    pass