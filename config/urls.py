"""
URL configuration for repair_cafe project.
"""
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from devices.admin import admin_site

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Language switcher
]

urlpatterns += i18n_patterns(
    path('admin/', admin_site.urls),
    path('', include('devices.urls')),
)
