# In lscms/lscms/middleware.py
from django.http import HttpResponse

class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bypass host header validation for health checks
        if request.path.endswith('/health/'):
            return HttpResponse("OK", status=200)
        return self.get_response(request)

