"""
URL configuration for repair_cafe project.
"""
from django.urls import path, include
from devices.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('devices.urls')),
]
