from django import forms
from .models import Device


class DeviceIntakeForm(forms.ModelForm):
    """Form for reception to intake new devices"""

    class Meta:
        model = Device
        fields = [
            'customer_name',
            'phone_number',
            'email_address',
            'device_type',
            'brand_model',
            'problem_description',
            'accessories',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'device_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Laptop, Phone, Tablet'}),
            'brand_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Apple MacBook Pro 2020'}),
            'problem_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the problem...'}),
            'accessories': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List any accessories (charger, case, etc.)'}),
        }


class DeviceRepairForm(forms.ModelForm):
    """Form for repairers to update device status and add notes"""

    class Meta:
        model = Device
        fields = [
            'status',
            'repairer_name',
            'repair_notes',
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'repairer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Repairer Name'}),
            'repair_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Repair solution and notes...'}),
        }


class DeviceSearchForm(forms.Form):
    """Form for searching/scanning devices by ID"""
    device_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Device ID (e.g., 2025-0042)',
            'autofocus': True
        })
    )
