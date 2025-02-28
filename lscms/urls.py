# LSOperations/lscms/urls.py
import os
import site
from django.contrib import admin
from django.urls import path, include, re_path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls
from search import views as search_views
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

# Find the wagtail admin static directory
site_packages = site.getsitepackages()[0]
wagtail_admin_static = os.path.join(site_packages, 'wagtail', 'admin', 'static', 'wagtailadmin')

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
    # Health check must be before the Wagtail catch-all
    path('health', health_check, name='health_check_no_slash'),
    path('health/', health_check, name='health_check'),
    path('system-status/health-check', health_check, name='health_check'),
   
    # Your existing patterns
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('search/', search_views.search, name='search'),
   
    # Make sure this is before the Wagtail catch-all
    path('', include('lscms.urls')),
    
    # Serve wagtailadmin static files directly from the package
    re_path(r'^static/wagtailadmin/(?P<path>.*)$', serve, {
        'document_root': wagtail_admin_static
    }),
   
    # Wagtail catch-all must be last
    path('', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
