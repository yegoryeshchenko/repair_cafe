from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Device
from .forms import DeviceIntakeForm, DeviceRepairForm, DeviceSearchForm


def dashboard(request):
    """Main dashboard showing all devices"""
    devices = Device.objects.all()

    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        devices = devices.filter(status=status_filter)

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        devices = devices.filter(
            Q(device_id__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(device_type__icontains=search_query) |
            Q(brand_model__icontains=search_query)
        )

    # Get devices needing reminders
    devices_needing_reminder = Device.objects.filter(
        status__in=['open', 'in_progress']
    ).exclude(
        date_finished__isnull=False
    )
    reminder_count = sum(1 for d in devices_needing_reminder if d.needs_reminder())

    context = {
        'devices': devices,
        'status_filter': status_filter,
        'search_query': search_query,
        'reminder_count': reminder_count,
        'status_choices': Device.STATUS_CHOICES,
    }
    return render(request, 'devices/dashboard.html', context)


def device_intake(request):
    """Reception form to intake new devices"""
    if request.method == 'POST':
        form = DeviceIntakeForm(request.POST)
        if form.is_valid():
            device = form.save()
            messages.success(request, f'Device registered successfully! Device ID: {device.device_id}')
            return redirect('print_label', device_id=device.device_id)
    else:
        form = DeviceIntakeForm()

    return render(request, 'devices/intake.html', {'form': form})


def device_detail(request, device_id):
    """View device details"""
    device = get_object_or_404(Device, device_id=device_id)
    return render(request, 'devices/detail.html', {'device': device})


def device_update(request, device_id):
    """Update device status and repair information"""
    device = get_object_or_404(Device, device_id=device_id)

    if request.method == 'POST':
        form = DeviceRepairForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            messages.success(request, f'Device {device.device_id} updated successfully!')
            return redirect('device_detail', device_id=device.device_id)
    else:
        form = DeviceRepairForm(instance=device)

    return render(request, 'devices/update.html', {'form': form, 'device': device})


def repair_station(request):
    """Repair station interface to search/scan and update devices"""
    form = DeviceSearchForm()
    device = None

    if request.GET.get('device_id'):
        device_id = request.GET.get('device_id')
        try:
            device = Device.objects.get(device_id=device_id)
        except Device.DoesNotExist:
            messages.error(request, f'Device ID "{device_id}" not found.')

    return render(request, 'devices/repair_station.html', {'form': form, 'device': device})


def print_label(request, device_id):
    """Print label/ticket for device"""
    device = get_object_or_404(Device, device_id=device_id)
    return render(request, 'devices/print_label.html', {'device': device})


def reminders(request):
    """View devices that need reminders"""
    all_active_devices = Device.objects.filter(
        status__in=['open', 'in_progress']
    ).exclude(
        date_finished__isnull=False
    )

    devices_needing_reminder = [d for d in all_active_devices if d.needs_reminder()]

    context = {
        'devices': devices_needing_reminder,
    }
    return render(request, 'devices/reminders.html', context)
