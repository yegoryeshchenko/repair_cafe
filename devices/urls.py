from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('intake/', views.device_intake, name='device_intake'),
    path('device/<str:device_id>/', views.device_detail, name='device_detail'),
    path('device/<str:device_id>/update/', views.device_update, name='device_update'),
    path('device/<str:device_id>/print/', views.print_label, name='print_label'),
    path('repair-station/', views.repair_station, name='repair_station'),
    path('reminders/', views.reminders, name='reminders'),
]
