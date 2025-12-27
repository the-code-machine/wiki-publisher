# config/urls.py
from django.contrib import admin
from django.urls import path, include  # <--- IMPORTANT: Add 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Forward any root request (empty string) to the publisher app
    path('', include('publisher.urls')), 
]