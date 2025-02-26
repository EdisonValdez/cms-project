# Create a new file: lscms/system_urls.py

from django.urls import path
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('health', health_check),
]
