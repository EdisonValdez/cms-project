# lscms/settings/__init__.py
import os

# Load settings based on environment variable
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', None)

if not settings_module:
    # Fallback detection - default to dev for safety
    if os.environ.get('DEPLOYMENT_ENVIRONMENT') == 'production':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lscms.settings.production')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lscms.settings.dev')
