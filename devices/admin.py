from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import Device, User


class RepairCafeAdminSite(admin.AdminSite):
    """Custom admin site that restricts access to admins only"""
    site_header = 'Repair Café Administration'
    site_title = 'Repair Café Admin'
    index_title = 'Welcome to Repair Café Administration'

    def has_permission(self, request):
        """Only allow users with is_admin=True to access the admin site"""
        return request.user.is_active and request.user.is_admin


# Create custom admin site instance
admin_site = RepairCafeAdminSite(name='admin')


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_admin'),
            'description': 'Admin users can manage other users and access the admin panel. Operators can only manage device intakes.'
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_admin'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    def get_readonly_fields(self, request, obj=None):
        """Make is_admin readonly when editing own account"""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj and obj.pk == request.user.pk:
            readonly_fields.append('is_admin')
        return readonly_fields


class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'device_id',
        'customer_name',
        'device_type',
        'brand_model',
        'status',
        'intaker',
        'intake_datetime',
        'repairer_name',
    ]
    list_filter = ['status', 'device_type', 'intaker', 'intake_datetime']
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
            'fields': ('intake_datetime', 'intaker')
        }),
        ('Repair Information', {
            'fields': ('status', 'repairer_name', 'repair_notes', 'date_finished')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Register models with custom admin site
admin_site.register(User, UserAdmin)
admin_site.register(Device, DeviceAdmin)

# Unregister Group model - not needed for this application
admin.site.unregister(Group)
