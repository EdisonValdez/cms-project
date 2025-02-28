# LSOperations/lscms/urls.py
from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
import os

@csrf_exempt
@never_cache
def health_check(request):
    """
    Health check endpoint exempt from middleware interference.
    """
    return HttpResponse(
        content="OK",
        status=200,
        content_type="text/plain"
    )

urlpatterns = [
    # Health check endpoints
    path('health', health_check, name='health_check_no_slash'),
    path('health/', health_check, name='health_check'),
    path('system-status/health-check', health_check, name='health_check_system'),
    
    # Admin URLs
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    
    # Document and search URLs
    path('documents/', include(wagtaildocs_urls)),
    path('search/', search_views.search, name='search'),
]

# Serve static Wagtail admin files in all environments
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Handle static files even in production
    import site
    site_packages = site.getsitepackages()[0]
    wagtail_admin_static = os.path.join(site_packages, 'wagtail', 'admin', 'static', 'wagtailadmin')
    
    urlpatterns += [
        re_path(r'^static/wagtailadmin/(?P<path>.*)$', serve, {
            'document_root': wagtail_admin_static
        }),
    ]

# Add Wagtail URLs at the end
urlpatterns += [
    path('', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
