from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta


class User(AbstractUser):
    """Custom User model with role-based access"""
    is_admin = models.BooleanField(
        default=False,
        help_text="Designates whether the user has admin privileges (can manage users)."
    )

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.get_full_name() or self.username

    def save(self, *args, **kwargs):
        """Automatically set is_staff based on is_admin status"""
        # Don't override is_staff for superusers (they always need admin access)
        if not self.is_superuser:
            self.is_staff = self.is_admin
        else:
            # Superusers should always have both is_staff and is_admin
            self.is_staff = True
            self.is_admin = True
        super().save(*args, **kwargs)

    @property
    def is_operator(self):
        """Check if user is an operator (regular user)"""
        return not self.is_admin


class Device(models.Model):
    STATUS_CHOICES = [
        ('open', _('Open')),
        ('in_progress', _('In Progress')),
        ('repaired', _('Repaired')),
        ('not_repaired', _('Not Repaired')),
        ('free_for_recycling', _('Free for Recycling')),
    ]

    # Auto-generated Device ID (e.g., 2025-0042)
    device_id = models.CharField(max_length=20, unique=True, editable=False)

    # Intake information
    intake_datetime = models.DateTimeField(default=timezone.now)
    intaker = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='intaken_devices',
        help_text="User who registered this device"
    )

    # Customer information
    customer_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField(blank=True)

    # Device information
    device_type = models.CharField(max_length=100)
    brand_model = models.CharField(max_length=200)
    problem_description = models.TextField()
    accessories = models.TextField(blank=True, help_text="List of accessories brought with the device")
    work_material_costs = models.TextField(blank=True, help_text="Work and material costs")
    investigation_cost_paid = models.BooleanField(default=False, help_text="Investigation cost paid")

    # Repair information
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    repairer_name = models.CharField(max_length=200, blank=True)
    repair_notes = models.TextField(blank=True, help_text="Repair solution and notes")
    date_finished = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-intake_datetime']

    def __str__(self):
        return f"{self.device_id} - {self.customer_name} - {self.device_type}"

    def save(self, *args, **kwargs):
        if not self.device_id:
            self.device_id = self.generate_device_id()

        # Set date_finished when status changes to a final state
        if self.status in ['repaired', 'not_repaired', 'free_for_recycling'] and not self.date_finished:
            self.date_finished = timezone.now()

        super().save(*args, **kwargs)

    def generate_device_id(self):
        """Generate a unique device ID in format YYYY-NNNN"""
        year = datetime.now().year

        # Get the last device for this year
        last_device = Device.objects.filter(
            device_id__startswith=f"{year}-"
        ).order_by('device_id').last()

        if last_device:
            # Extract the number and increment
            last_number = int(last_device.device_id.split('-')[1])
            new_number = last_number + 1
        else:
            # First device of the year
            new_number = 1

        return f"{year}-{new_number:04d}"

    def days_in_repair(self):
        """Calculate how many days the device has been in the system"""
        if self.date_finished:
            end_date = self.date_finished
        else:
            end_date = timezone.now()

        delta = end_date - self.intake_datetime
        return delta.days

    def needs_reminder(self, days_threshold=7):
        """Check if device needs a reminder (been in system too long)"""
        if self.status in ['repaired', 'not_repaired', 'free_for_recycling']:
            return False

        return self.days_in_repair() >= days_threshold
