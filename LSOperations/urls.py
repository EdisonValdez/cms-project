# LSOperations/urls.py
from django.views.generic.base import RedirectView

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def health_check(request):
    """Simple health check endpoint for DigitalOcean."""
    return HttpResponse("OK", status=200)
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('health', health_check, name='health_check_no_slash'),
    path('static/<path:path>', RedirectView.as_view(url='/lscms/staticfiles/%(path)s')),
]
 
def debug_view(request):
    from django.http import HttpResponse
    import sys
    html = "<html><body><h1>Debug Info</h1>"
    html += "<p>Python version: {}</p>".format(sys.version)
    html += "<p>PYTHONPATH: {}</p>".format(sys.path)
    html += "<p>Request path: {}</p>".format(request.path)
    html += "<p>Available URLs:</p><ul>"
    for pattern in urlpatterns:
        html += "<li>{}</li>".format(pattern.pattern)
    html += "</ul></body></html>"
    return HttpResponse(html)

urlpatterns += [
    path('debug/', debug_view),
]
