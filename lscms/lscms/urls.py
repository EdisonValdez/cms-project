# LSOperations/lscms/lscms/urls.py

from django.conf import settings
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls.static import static
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
    
    # For anything not caught by the above, fall back to the Wagtail page serving mechanism
    path("", include(wagtail_urls)),
]

if not settings.DEBUG:
    site_packages = site.getsitepackages()[0]
    wagtail_admin_static = os.path.join(site_packages, 'wagtail', 'admin', 'static', 'wagtailadmin')
    drf_static_dir = os.path.join(site_packages, 'rest_framework', 'static', 'rest_framework')
    
    urlpatterns += [
        re_path(r'^static/wagtailadmin/(?P<path>.*)$', serve, {
            'document_root': wagtail_admin_static
        }),
        re_path(r'^static/rest_framework/(?P<path>.*)$', serve, {
            'document_root': drf_static_dir
        }),
    ]
    
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  