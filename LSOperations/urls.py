"""
URL configuration for LSOperations project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
