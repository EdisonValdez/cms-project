# lscms/lscms/home/views.py

from django.shortcuts import render
from wagtail.models import Page

def index(request):
    home_page = Page.objects.live().public().filter(title="Home").first()
    if home_page:
        return render(request, 'home/index.html', {'page': home_page})
    else:
        return render(request, 'home/index.html', {})
