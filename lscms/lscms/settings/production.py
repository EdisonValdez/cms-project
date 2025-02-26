from .base import *

# Production settings
DEBUG = False
ALLOWED_HOSTS = ['your-production-domain.com']

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True

try:
    from .local import *
except ImportError:
    pass
