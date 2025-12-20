from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Device, User


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
            'work_material_costs',
            'investigation_cost_paid',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'device_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Laptop, Phone, Tablet'}),
            'brand_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Apple MacBook Pro 2020'}),
            'problem_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Duidelijk omschriving van de klacht/verstoring'}),
            'accessories': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Lijst van alle accessoires (slangen, kabels, voeding, etc.)'}),
            'work_material_costs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Werkzamheden / materiaalkosten'}),
            'investigation_cost_paid': forms.RadioSelect(choices=[(True, 'Ja'), (False, 'Nee')], attrs={'class': 'form-check-input'}),
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


class UserCreateForm(UserCreationForm):
    """Form for creating new users"""
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    is_admin = forms.BooleanField(
        required=False,
        label='Admin User',
        help_text='Check if this user should have admin privileges (can manage users)',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_admin', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class UserEditForm(forms.ModelForm):
    """Form for editing existing users"""
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    is_admin = forms.BooleanField(
        required=False,
        label='Admin User',
        help_text='Check if this user should have admin privileges (can manage users)',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_admin', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        # Disable is_admin checkbox if editing own account
        if self.current_user and self.instance and self.instance.pk == self.current_user.pk:
            self.fields['is_admin'].disabled = True
            self.fields['is_admin'].help_text = 'You cannot change your own admin role. Another admin must change it for you.'
