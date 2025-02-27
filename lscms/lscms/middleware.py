# In lscms/middleware.py

from django.http import HttpResponse


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for exact health check paths
        if request.path == '/health' or request.path == '/health/':
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Health check intercepted by middleware: {request.path}")
            return HttpResponse("OK", status=200)
        
        # Process all other requests normally
        return self.get_response(request)
