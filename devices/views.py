from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.utils import timezone
from .models import Device, User
from .forms import DeviceIntakeForm, DeviceRepairForm, DeviceSearchForm, UserCreateForm, UserEditForm
from .barcode_utils import generate_barcode_base64


def admin_required(function):
    """Decorator to require admin privileges"""
    def check_admin(user):
        return user.is_authenticated and user.is_admin

    decorator = user_passes_test(check_admin, login_url='dashboard')
    return decorator(function)


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome, {user.get_full_name() or user.username}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'devices/login.html')


def logout_view(request):
    """User logout"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    """Main dashboard showing all devices"""
    devices = Device.objects.select_related('intaker').all()

    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        devices = devices.filter(status=status_filter)

    # Filter by intaker if provided
    intaker_filter = request.GET.get('intaker', '')
    if intaker_filter:
        devices = devices.filter(intaker_id=intaker_filter)

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

    # Sorting functionality
    sort_by = request.GET.get('sort', '-intake_datetime')
    allowed_sorts = [
        'device_id', '-device_id',
        'customer_name', '-customer_name',
        'device_type', '-device_type',
        'status', '-status',
        'intake_datetime', '-intake_datetime',
        'intaker__username', '-intaker__username',
    ]
    if sort_by in allowed_sorts:
        devices = devices.order_by(sort_by)

    # Get devices needing reminders
    devices_needing_reminder = Device.objects.filter(
        status__in=['open', 'in_progress']
    ).exclude(
        date_finished__isnull=False
    )
    reminder_count = sum(1 for d in devices_needing_reminder if d.needs_reminder())

    # Get all intakers for filter dropdown
    intakers = User.objects.filter(intaken_devices__isnull=False).distinct().order_by('username')

    context = {
        'devices': devices,
        'status_filter': status_filter,
        'intaker_filter': intaker_filter,
        'search_query': search_query,
        'sort_by': sort_by,
        'reminder_count': reminder_count,
        'status_choices': Device.STATUS_CHOICES,
        'intakers': intakers,
    }
    return render(request, 'devices/dashboard.html', context)


@login_required
def device_intake(request):
    """Reception form to intake new devices"""
    if request.method == 'POST':
        form = DeviceIntakeForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.intaker = request.user  # Auto-assign logged-in user as intaker
            device.save()
            messages.success(request, f'Device registered successfully! Device ID: {device.device_id}')
            return redirect('print_label', device_id=device.device_id)
    else:
        form = DeviceIntakeForm()

    return render(request, 'devices/intake.html', {'form': form})


@login_required
def device_detail(request, device_id):
    """View device details"""
    device = get_object_or_404(Device, device_id=device_id)
    return render(request, 'devices/detail.html', {'device': device})


@login_required
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


@login_required
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


@login_required
def print_label(request, device_id):
    """Print label/ticket for device"""
    device = get_object_or_404(Device, device_id=device_id)
    barcode_image = generate_barcode_base64(device.device_id)
    return render(request, 'devices/print_label.html', {
        'device': device,
        'barcode_image': barcode_image,
    })


@login_required
def print_formulier(request, device_id):
    """Print A4 form for device"""
    device = get_object_or_404(Device, device_id=device_id)
    barcode_image = generate_barcode_base64(device.device_id)
    return render(request, 'devices/print_formulier.html', {
        'device': device,
        'barcode_image': barcode_image,
    })


@login_required
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


# User Management Views (Admin Only)

@admin_required
def user_list(request):
    """List all users (admin only)"""
    users = User.objects.all().order_by('username')
    context = {
        'users': users,
    }
    return render(request, 'devices/user_list.html', context)


@admin_required
def user_create(request):
    """Create new user (admin only)"""
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.username}" created successfully!')
            return redirect('user_list')
    else:
        form = UserCreateForm()

    return render(request, 'devices/user_form.html', {'form': form, 'action': 'Create'})


@admin_required
def user_edit(request, user_id):
    """Edit existing user (admin only)"""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user, current_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{user.username}" updated successfully!')
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user, current_user=request.user)

    return render(request, 'devices/user_form.html', {'form': form, 'action': 'Edit', 'user_obj': user})


@admin_required
def user_delete(request, user_id):
    """Delete user (admin only)"""
    user = get_object_or_404(User, id=user_id)

    # Prevent deleting yourself
    if user.id == request.user.id:
        messages.error(request, 'You cannot delete your own account!')
        return redirect('user_list')

    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" deleted successfully!')
        return redirect('user_list')

    return render(request, 'devices/user_confirm_delete.html', {'user_obj': user})
