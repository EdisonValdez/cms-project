# lscms/lscms/views.py

import os
import site
from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets
from .models import HeaderBlock, FooterBlock, AdBlock, SEOSettings, MenuItem, MarketingCampaign, NotificationMessage, LayoutSettings, AnalyticsSettings
from .serializers import HeaderBlockSerializer, FooterBlockSerializer, AdBlockSerializer, SEOSettingsSerializer, MenuItemSerializer, MarketingCampaignSerializer, NotificationMessageSerializer, LayoutSettingsSerializer, AnalyticsSettingsSerializer
from rest_framework.permissions import IsAuthenticated  # Modify with other permission class
from .permissions import IsAdminOrReadOnly
from django.contrib.admin.views.decorators import staff_member_required
import logging
logger = logging.getLogger(__name__)

def health_check(request): 
    """
    Debug health check.
    """
    logger.info(f"Health check called with path: {request.path}, full_path: {request.get_full_path()}")
    logger.info(f"Request META: {request.META}")
    
    return HttpResponse("OK", status=200)
 
@staff_member_required
def static_files_debug(request):
    """
    A view to help debug static file issues.
    Only accessible to staff members for security.
    """
    site_packages_list = site.getsitepackages()
    site_packages = site_packages_list[0]
    
    # Static directories we're trying to serve
    static_dirs = {
        'wagtailadmin': os.path.join(site_packages, 'wagtail', 'admin', 'static', 'wagtailadmin'),
        'wagtailimages': os.path.join(site_packages, 'wagtail', 'images', 'static', 'wagtailimages'),
        'wagtaildocs': os.path.join(site_packages, 'wagtail', 'documents', 'static', 'wagtaildocs'),
        'wagtailembeds': os.path.join(site_packages, 'wagtail', 'embeds', 'static', 'wagtailembeds'),
        'rest_framework': os.path.join(site_packages, 'rest_framework', 'static', 'rest_framework'),
        'project_static': settings.STATIC_ROOT,
    }
    
    # Check if directories exist and are readable
    dir_status = {}
    for name, path in static_dirs.items():
        dir_status[name] = {
            'path': path,
            'exists': os.path.exists(path),
            'is_dir': os.path.isdir(path) if os.path.exists(path) else False,
            'readable': os.access(path, os.R_OK) if os.path.exists(path) else False,
            'example_files': []
        }
        
        # List some example files in each directory
        if dir_status[name]['exists'] and dir_status[name]['is_dir']:
            try:
                files = os.listdir(path)
                dir_status[name]['example_files'] = files[:5]  # Just show first 5 files
            except:
                dir_status[name]['example_files'] = ['Error listing files']
    
    # Check MIME types configuration
    import mimetypes
    mime_types = {
        '.css': mimetypes.guess_type('style.css')[0],
        '.js': mimetypes.guess_type('script.js')[0],
        '.png': mimetypes.guess_type('image.png')[0],
        '.jpg': mimetypes.guess_type('image.jpg')[0],
        '.svg': mimetypes.guess_type('image.svg')[0],
    }
    
    # Generate HTML response with all the debug info
    html = """
    <html>
    <head>
        <title>Static Files Debug</title>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            h1 { color: #333; }
            h2 { color: #666; margin-top: 30px; }
            .section { margin-bottom: 30px; }
            .success { color: green; }
            .error { color: red; }
            table { border-collapse: collapse; width: 100%; }
            th, td { text-align: left; padding: 8px; border: 1px solid #ddd; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>Static Files Debug Information</h1>
        
        <div class="section">
            <h2>Static Directories</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Path</th>
                    <th>Exists</th>
                    <th>Is Directory</th>
                    <th>Readable</th>
                    <th>Example Files</th>
                </tr>
    """
    
    for name, status in dir_status.items():
        exists_class = "success" if status['exists'] else "error"
        is_dir_class = "success" if status['is_dir'] else "error"
        readable_class = "success" if status['readable'] else "error"
        
        html += f"""
                <tr>
                    <td>{name}</td>
                    <td>{status['path']}</td>
                    <td class="{exists_class}">{status['exists']}</td>
                    <td class="{is_dir_class}">{status['is_dir']}</td>
                    <td class="{readable_class}">{status['readable']}</td>
                    <td>{', '.join(status['example_files'])}</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>MIME Types Configuration</h2>
            <table>
                <tr>
                    <th>Extension</th>
                    <th>MIME Type</th>
                </tr>
    """
    
    for ext, mime_type in mime_types.items():
        mime_class = "success" if mime_type else "error"
        html += f"""
                <tr>
                    <td>{ext}</td>
                    <td class="{mime_class}">{mime_type or 'Not configured'}</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>Django Settings</h2>
            <table>
                <tr>
                    <th>Setting</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>DEBUG</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>STATIC_URL</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>STATIC_ROOT</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>STATICFILES_DIRS</td>
                    <td>{}</td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """.format(
        settings.DEBUG,
        settings.STATIC_URL,
        settings.STATIC_ROOT,
        ', '.join(str(d) for d in getattr(settings, 'STATICFILES_DIRS', []))
    )
    
    return HttpResponse(html)

# HeaderBlock ViewSet
class HeaderBlockViewSet(viewsets.ModelViewSet):
    queryset = HeaderBlock.objects.all()
    serializer_class = HeaderBlockSerializer
    permission_classes = [IsAdminOrReadOnly]

# FooterBlock ViewSet
class FooterBlockViewSet(viewsets.ModelViewSet):
    queryset = FooterBlock.objects.all()
    serializer_class = FooterBlockSerializer
    permission_classes = [IsAdminOrReadOnly]

# AdBlock ViewSet
class AdBlockViewSet(viewsets.ModelViewSet):
    queryset = AdBlock.objects.all()
    serializer_class = AdBlockSerializer
    permission_classes = [IsAdminOrReadOnly]

# SEOSettings ViewSet
class SEOSettingsViewSet(viewsets.ModelViewSet):
    queryset = SEOSettings.objects.all()
    serializer_class = SEOSettingsSerializer
    permission_classes = [IsAdminOrReadOnly]

# MenuItem ViewSet
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

# MarketingCampaign ViewSet
class MarketingCampaignViewSet(viewsets.ModelViewSet):
    queryset = MarketingCampaign.objects.all()
    serializer_class = MarketingCampaignSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = MarketingCampaign.objects.filter(is_active=True)
        platform = self.request.query_params.get('platform', None)
        location = self.request.query_params.get('location', None)

        if platform:
            queryset = queryset.filter(target_platforms__contains=[platform])
        if location:
            queryset = queryset.filter(target_locations__contains=[location])
        
        return queryset.order_by('-priority')

# NotificationMessage ViewSet
class NotificationMessageViewSet(viewsets.ModelViewSet):
    queryset = NotificationMessage.objects.all()
    serializer_class = NotificationMessageSerializer
    permission_classes = [IsAdminOrReadOnly]

# LayoutSettings ViewSet
class LayoutSettingsViewSet(viewsets.ModelViewSet):
    queryset = LayoutSettings.objects.all()
    serializer_class = LayoutSettingsSerializer
    permission_classes = [IsAdminOrReadOnly]

# AnalyticsSettings ViewSet
class AnalyticsSettingsViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsSettings.objects.all()
    serializer_class = AnalyticsSettingsSerializer
    permission_classes = [IsAdminOrReadOnly]

