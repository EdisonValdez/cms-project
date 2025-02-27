# LSOperations/lscms/lscms/settings/production.py

from .base import *
import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Production settings
DEBUG = False

# Get the domain from environment variables
import socket
from ipaddress import IPv4Network

# Basic allowed hosts
ALLOWED_HOSTS = [
    '*',  # Allow all hosts temporarily
    '.ondigitalocean.app',
    'localsecrets.travel',
]

# Add all possible Kubernetes pod IPs
# This covers the 10.244.0.0/16 subnet commonly used by Kubernetes
for subnet in ['10.244.0.0/16']:
    network = IPv4Network(subnet)
    ALLOWED_HOSTS.extend([str(ip) for ip in network.hosts()])

# Database settings
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }

# Static files configuration - CRITICAL FOR DEPLOYMENT
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configure WhiteNoise properly for static files
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    # Find the index of SecurityMiddleware
    try:
        security_index = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
        # Insert WhiteNoise right after SecurityMiddleware
        MIDDLEWARE.insert(security_index + 1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    except ValueError:
        # If SecurityMiddleware is not found, insert WhiteNoise at the beginning
        MIDDLEWARE.insert(0, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Static Files Storage - Use a simpler storage backend that doesn't require manifest
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
WHITENOISE_ROOT = os.path.join(BASE_DIR, 'static')

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

# Enhanced logging configuration
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
        'whitenoise': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Load local settings if they exist
try:
    from .local import *
except ImportError:
    pass

# Load fixes if they exist
try:
    from .fixes import *
except ImportError:
    pass
