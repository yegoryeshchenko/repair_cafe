from django.contrib import admin
from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'device_id',
        'customer_name',
        'device_type',
        'brand_model',
        'status',
        'intake_datetime',
        'repairer_name',
    ]
    list_filter = ['status', 'device_type', 'intake_datetime']
    search_fields = [
        'device_id',
        'customer_name',
        'phone_number',
        'email_address',
        'device_type',
        'brand_model',
    ]
    readonly_fields = ['device_id', 'created_at', 'updated_at']

    fieldsets = (
        ('Device Information', {
            'fields': ('device_id', 'device_type', 'brand_model', 'problem_description', 'accessories')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'phone_number', 'email_address')
        }),
        ('Intake Information', {
            'fields': ('intake_datetime',)
        }),
        ('Repair Information', {
            'fields': ('status', 'repairer_name', 'repair_notes', 'date_finished')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
