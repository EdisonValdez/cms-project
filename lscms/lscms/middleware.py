# In lscms/lscms/middleware.py
from django.http import HttpResponse
import os
from django.http import FileResponse, Http404
from django.conf import settings
import pkg_resources

class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bypass host header validation for health checks
        if request.path.endswith('/health/'):
            return HttpResponse("OK", status=200)
        return self.get_response(request)
 
class WagtailAdminStaticFilesMiddleware:
    """
    Middleware to serve Wagtail admin static files directly from the installed package.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Only handle static files for wagtailadmin
        if request.path.startswith('/static/wagtailadmin/'):
            # Extract the relative path within wagtailadmin
            relative_path = request.path.replace('/static/wagtailadmin/', '')
            
            # Remove query parameters if present
            if '?' in relative_path:
                relative_path = relative_path.split('?')[0]
            
            try:
                # Try to find the file in the installed wagtail package
                wagtail_path = pkg_resources.resource_filename('wagtail', f'admin/static/wagtailadmin/{relative_path}')
                
                if os.path.exists(wagtail_path):
                    # Determine content type based on file extension
                    content_type = None
                    if relative_path.endswith('.js'):
                        content_type = 'application/javascript'
                    elif relative_path.endswith('.css'):
                        content_type = 'text/css'
                    elif relative_path.endswith('.png'):
                        content_type = 'image/png'
                    elif relative_path.endswith('.jpg') or relative_path.endswith('.jpeg'):
                        content_type = 'image/jpeg'
                    elif relative_path.endswith('.svg'):
                        content_type = 'image/svg+xml'
                    
                    # Return the file
                    return FileResponse(open(wagtail_path, 'rb'), content_type=content_type)
            except (FileNotFoundError, pkg_resources.DistributionNotFound):
                pass
        
        # For all other requests, continue normal processing
        return self.get_response(request)
