# In lscms/lscms/middleware.py
from django.http import HttpResponse
import os
from django.http import FileResponse, Http404
from django.conf import settings
import pkg_resources
from django.http import FileResponse
from django.views.static import serve
import site
import re

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
 
class DRFStaticFilesMiddleware:
    """
    Middleware to serve Django REST Framework static files in all environments.
    Similar to the WagtailAdminStaticFilesMiddleware but for DRF.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Get the path to DRF static files
        site_packages = site.getsitepackages()[0]
        self.drf_static_dir = os.path.join(site_packages, 'rest_framework', 'static', 'rest_framework')
        
        # Regex pattern to match DRF static files URL
        self.pattern = re.compile(r'^/static/rest_framework/(.*)$')

    def __call__(self, request):
        # Check if the request is for a DRF static file
        match = self.pattern.match(request.path)
        
        if match and not settings.DEBUG:
            # Path within the static directory
            path = match.group(1)
            # Serve the file
            return serve(request, path, document_root=self.drf_static_dir)
        
        # Let regular middleware handle non-DRF static files
        return self.get_response(request)
 
class CombinedStaticFilesMiddleware:
    """
    Middleware to serve static files from Django packages in all environments.
    Handles both Wagtail admin and Django REST Framework static files.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Get site-packages directory
        site_packages = site.getsitepackages()[0]
        
        # Set up paths to static directories
        self.wagtail_admin_static = os.path.join(site_packages, 'wagtail', 'admin', 'static', 'wagtailadmin')
        self.drf_static_dir = os.path.join(site_packages, 'rest_framework', 'static', 'rest_framework')
        
        # Regex patterns to match static files URLs
        self.wagtail_pattern = re.compile(r'^/static/wagtailadmin/(.*)$')
        self.drf_pattern = re.compile(r'^/static/rest_framework/(.*)$')

    def __call__(self, request):
        # Not needed in DEBUG mode as Django handles static files
        if settings.DEBUG:
            return self.get_response(request)
        
        # Check if the request is for a Wagtail admin static file
        wagtail_match = self.wagtail_pattern.match(request.path)
        if wagtail_match:
            path = wagtail_match.group(1)
            return serve(request, path, document_root=self.wagtail_admin_static)
        
        # Check if the request is for a DRF static file
        drf_match = self.drf_pattern.match(request.path)
        if drf_match:
            path = drf_match.group(1)
            return serve(request, path, document_root=self.drf_static_dir)
        
        # Let regular middleware handle other requests
        return self.get_response(request)