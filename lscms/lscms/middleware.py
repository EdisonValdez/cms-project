# LSOperations/lscms/lscms/middleware.py

import os
import mimetypes
from django.conf import settings
from django.http import FileResponse, Http404
from django.http import HttpResponse  
import pkg_resources
from django.http import FileResponse
from django.views.static import serve
import mimetypes
import site
import re 


class StaticFilesMIMEMiddleware:
    """
    Middleware to ensure proper MIME types are set for static files.
    This helps resolve the "Refused to apply style" and "Refused to execute script" errors.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Ensure proper MIME types are registered
        self._register_mime_types()
        
        # Static file patterns to catch
        self.static_patterns = [
            '/static/css/',
            '/static/js/',
            '/static/CACHE/css/',
            '/static/CACHE/js/',
            '/static/wagtail',
            '/static/wagtailadmin/',
            '/static/wagtailimages/',
            '/static/wagtaildocs/',
            '/static/wagtailembeds/',
            '/static/rest_framework/',
        ]

    def _register_mime_types(self):
        """Register correct MIME types for common static files."""
        mimetypes.add_type('text/css', '.css')
        mimetypes.add_type('application/javascript', '.js')
        mimetypes.add_type('image/svg+xml', '.svg')
        mimetypes.add_type('image/x-icon', '.ico')
        mimetypes.add_type('font/woff', '.woff')
        mimetypes.add_type('font/woff2', '.woff2')
        mimetypes.add_type('font/ttf', '.ttf')
        
    def _is_static_file(self, path):
        """Check if the request path is for a static file we want to handle."""
        return any(path.startswith(pattern) for pattern in self.static_patterns)
    
    def _get_content_type(self, file_path):
        """Get the proper content type based on file extension."""
        _, ext = os.path.splitext(file_path)
        
        # Explicit mapping for common types
        if ext == '.css':
            return 'text/css'
        elif ext == '.js':
            return 'application/javascript'
        elif ext == '.svg':
            return 'image/svg+xml'
        elif ext in ['.jpg', '.jpeg']:
            return 'image/jpeg'
        elif ext == '.png':
            return 'image/png'
        elif ext == '.woff':
            return 'font/woff'
        elif ext == '.woff2':
            return 'font/woff2'
        elif ext == '.ttf':
            return 'font/ttf'
        elif ext == '.ico':
            return 'image/x-icon'
        
        # Fallback to Python's mimetype module
        content_type, _ = mimetypes.guess_type(file_path)
        return content_type or 'application/octet-stream'

    def __call__(self, request):
        """Process each request through the middleware."""
        # First, let the regular middleware handle the request
        response = self.get_response(request)
        
        # We only care about static file responses that might have incorrect MIME types
        path = request.path
        
        if not self._is_static_file(path):
            return response
            
        # If it's a FileResponse, we want to ensure proper MIME type
        if isinstance(response, FileResponse) or 'Content-Type' in response:
            if isinstance(response, FileResponse) and hasattr(response, 'file_to_stream'):
                content_type = self._get_content_type(path)
                response['Content-Type'] = content_type
            elif 'Content-Type' in response and response['Content-Type'] == 'text/html':
                # The MIME type is incorrectly set to text/html, fix it
                content_type = self._get_content_type(path)
                response['Content-Type'] = content_type
        
        return response
 
class ComprehensiveStaticFilesMiddleware:
    """
    Comprehensive middleware to serve static files from all Wagtail and DRF packages.
    Handles MIME types properly and serves files from various package static directories.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Get the site-packages directory
        site_packages_list = site.getsitepackages()
        self.site_packages = site_packages_list[0]
        
        # Set up static file directory mappings
        self.static_dirs = {
            # Core Wagtail static files
            'wagtailadmin': os.path.join(self.site_packages, 'wagtail', 'admin', 'static', 'wagtailadmin'),
            
            # Wagtail module static files
            'wagtailimages': os.path.join(self.site_packages, 'wagtail', 'images', 'static', 'wagtailimages'),
            'wagtaildocs': os.path.join(self.site_packages, 'wagtail', 'documents', 'static', 'wagtaildocs'),
            'wagtailembeds': os.path.join(self.site_packages, 'wagtail', 'embeds', 'static', 'wagtailembeds'),
            'wagtailsnippets': os.path.join(self.site_packages, 'wagtail', 'snippets', 'static', 'wagtailsnippets'),
            'wagtailsites': os.path.join(self.site_packages, 'wagtail', 'sites', 'static', 'wagtailsites'),
            'wagtailusers': os.path.join(self.site_packages, 'wagtail', 'users', 'static', 'wagtailusers'),
            'wagtailcore': os.path.join(self.site_packages, 'wagtail', 'core', 'static', 'wagtailcore'),
            'wagtail_modeladmin': os.path.join(self.site_packages, 'wagtail_modeladmin', 'static', 'wagtail_modeladmin'),
            
            # Django REST Framework static files
            'rest_framework': os.path.join(self.site_packages, 'rest_framework', 'static', 'rest_framework'),
        }
        
        # Regular expression to match all static files from known packages
        self.static_pattern = re.compile(r'^/static/(?P<package>[a-zA-Z_]+)/(?P<path>.+)$')
        
        # Regular expression to match compiled CSS from Django Compressor
        self.cache_pattern = re.compile(r'^/static/CACHE/(?P<path>.+)$')
        
        # Pattern for regular static files
        self.regular_static_pattern = re.compile(r'^/static/(?P<path>.+)$')
        
        # Ensure MIME types are correctly registered
        self._register_mime_types()

    def _register_mime_types(self):
        """Register additional MIME types to ensure proper content serving."""
        mimetypes.add_type('text/css', '.css')
        mimetypes.add_type('application/javascript', '.js')
        mimetypes.add_type('image/svg+xml', '.svg')
        mimetypes.add_type('image/x-icon', '.ico')
        mimetypes.add_type('image/png', '.png')
        mimetypes.add_type('image/jpeg', '.jpg')
        mimetypes.add_type('image/jpeg', '.jpeg')
        mimetypes.add_type('font/woff', '.woff')
        mimetypes.add_type('font/woff2', '.woff2')
        mimetypes.add_type('font/ttf', '.ttf')
        mimetypes.add_type('font/eot', '.eot')

    def _serve_static_file(self, request, file_path):
        """Serve a static file with the correct MIME type."""
        try:
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                raise Http404(f"Static file not found: {file_path}")
            
            # Get the file's MIME type based on extension
            content_type, encoding = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'
                
            # Open and serve the file with the correct MIME type
            response = FileResponse(open(file_path, 'rb'), content_type=content_type)
            
            # Set caching headers to improve performance
            response['Cache-Control'] = 'max-age=86400, public'  # Cache for 24 hours
                
            return response
            
        except FileNotFoundError:
            raise Http404(f"Static file not found: {file_path}")

    def __call__(self, request):
        # Skip in DEBUG mode as Django's staticfiles app handles it
        if settings.DEBUG:
            return self.get_response(request)
        
        # Check if the request is for a package-specific static file
        package_match = self.static_pattern.match(request.path)
        if package_match:
            package = package_match.group('package')
            path = package_match.group('path')
            
            # If we have a directory for this package
            if package in self.static_dirs:
                file_path = os.path.join(self.static_dirs[package], path)
                return self._serve_static_file(request, file_path)
        
        # Check if the request is for a compiled CSS file
        cache_match = self.cache_pattern.match(request.path)
        if cache_match:
            cache_path = cache_match.group('path')
            file_path = os.path.join(settings.STATIC_ROOT, 'CACHE', cache_path)
            return self._serve_static_file(request, file_path)
        
        # Check for regular static files (fallback)
        regular_match = self.regular_static_pattern.match(request.path)
        if regular_match:
            static_path = regular_match.group('path')
            # First try project static root
            file_path = os.path.join(settings.STATIC_ROOT, static_path)
            
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return self._serve_static_file(request, file_path)
                
            # Then try project static dirs
            for static_dir in settings.STATICFILES_DIRS:
                file_path = os.path.join(static_dir, static_path)
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    return self._serve_static_file(request, file_path)
 
        return self.get_response(request)
 
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