from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard and Device Management
    path('', views.dashboard, name='dashboard'),
    path('intake/', views.device_intake, name='device_intake'),
    path('device/<str:device_id>/', views.device_detail, name='device_detail'),
    path('device/<str:device_id>/update/', views.device_update, name='device_update'),
    path('device/<str:device_id>/print/', views.print_label, name='print_label'),
    path('device/<str:device_id>/print-formulier/', views.print_formulier, name='print_formulier'),
    path('repair-station/', views.repair_station, name='repair_station'),
    path('reminders/', views.reminders, name='reminders'),
]
