# LSOperations/lscms/lscms/urls.py

from django import views
from django.conf import settings
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls.static import static
from .views import static_files_debug
from search import views as search_views
from django.conf.urls.i18n import i18n_patterns
from rest_framework.authtoken.views import obtain_auth_token
from .api import api_router
from .authentication import CustomAuthToken
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.urls import path, include, re_path
from django.contrib import admin
from django.views.static import serve
import os
import site


@csrf_exempt
@never_cache
def health_check(request):
    """
    Health check endpoint exempt from middleware interference.
    """
    # Basic service check
    return HttpResponse(
        content="OK",
        status=200,
        content_type="text/plain"
    )


urlpatterns = [
    path('health/', include('health.urls')),
    # Django Admin
    path('django-admin/', admin.site.urls),

    # Wagtail Admin
    path('admin/', include(wagtailadmin_urls)),
   
    # Wagtail Documents
    path("documents/", include(wagtaildocs_urls)),
   
    path("search/", search_views.search, name="search"),
   
    path('i18n/', include('django.conf.urls.i18n')),
   
    # Authentication endpoints
    path('api/v1/token/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls')),  # This is for the browsable API
   
    # API endpoints
    path('api/v1/', include(api_router.urls)),
    path('debug/static/', static_files_debug, name='static_files_debug'),
   
    # For anything not caught by the above, fall back to the Wagtail page serving mechanism
    path("", include(wagtail_urls)),
]


# Static file handling for production mode
if not settings.DEBUG:
    # Get site-packages directory
    site_packages = site.getsitepackages()[0]
    
    # Define all the static directories we need to serve
    static_mappings = {
        'wagtailadmin': os.path.join(site_packages, 'wagtail', 'admin', 'static', 'wagtailadmin'),
        'wagtailimages': os.path.join(site_packages, 'wagtail', 'images', 'static', 'wagtailimages'),
        'wagtaildocs': os.path.join(site_packages, 'wagtail', 'documents', 'static', 'wagtaildocs'),
        'wagtailembeds': os.path.join(site_packages, 'wagtail', 'embeds', 'static', 'wagtailembeds'),
        'wagtailsnippets': os.path.join(site_packages, 'wagtail', 'snippets', 'static', 'wagtailsnippets'),
        'wagtailsites': os.path.join(site_packages, 'wagtail', 'sites', 'static', 'wagtailsites'),
        'wagtailusers': os.path.join(site_packages, 'wagtail', 'users', 'static', 'wagtailusers'),
        'wagtailcore': os.path.join(site_packages, 'wagtail', 'core', 'static', 'wagtailcore'),
        'rest_framework': os.path.join(site_packages, 'rest_framework', 'static', 'rest_framework'),
    }
    
    # Add URL patterns for each static directory
    for app_name, static_dir in static_mappings.items():
        if os.path.exists(static_dir) and os.path.isdir(static_dir):
            urlpatterns += [
                re_path(f'^static/{app_name}/(?P<path>.*)$', serve, {
                    'document_root': static_dir,
                }),
            ]
    
    # Add handling for compressed/cached static files
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        cache_dir = os.path.join(settings.STATIC_ROOT, 'CACHE')
        if os.path.exists(cache_dir) and os.path.isdir(cache_dir):
            urlpatterns += [
                re_path(r'^static/CACHE/(?P<path>.*)$', serve, {
                    'document_root': cache_dir,
                }),
            ]
    
    # Add fallback for other static files (CSS, JS, etc.)
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        urlpatterns += [
            re_path(r'^static/(?P<path>.*)$', serve, {
                'document_root': settings.STATIC_ROOT,
                'show_indexes': False,
            }),
        ]
    
    # Add handling for media files if MEDIA_ROOT is defined
    if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
        urlpatterns += [
            re_path(r'^media/(?P<path>.*)$', serve, {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': False,
            }),
        ]

# Development mode static file handling
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
