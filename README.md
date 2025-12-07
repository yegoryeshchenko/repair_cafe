# Repair Café Device Tracking System

A Django web application to help Repair Cafés track devices brought by customers for repair.

## Features

### User Roles & Access Control

The application supports two user roles with different permissions:

**Admin Users:**
- Create and manage other admin and operator users via admin panel at `/admin`
- Perform all intake and repair operations (can act as operator)
- Change user roles from admin to operator and back
- Full access to Django admin panel for user and device management
- Cannot change their own role (requires another admin)

**Operator Users:**
- Perform intake and repair operations (CRUD on devices)
- Cannot access admin panel at `/admin`
- Cannot manage other users

### Reception/Intake Workflow
- Easy-to-use intake form for receptionists and operators
- Captures all customer and device information
- Automatic Device ID generation (format: YYYY-NNNN, e.g., 2025-0042)
- Accessories tracking with prominent display
- Printable labels with scannable Code128 barcodes for device identification
- Auto-assigns logged-in user as intaker

### Repair Station Workflow
- Quick device search/scan by Device ID using barcode scanner
- Automatically focuses on search field for instant scanning
- View all device information including accessories
- Update repair status with multiple states:
  - Open
  - In Progress
  - Repaired
  - Not Repaired
  - Free for Recycling
- Add repair notes and repairer name
- Automatic date tracking when status changes to final state

### Dashboard
- View all devices with filtering by status
- Filter by intaker (see who registered each device)
- Search functionality with barcode scanner support (Device ID, customer name, phone, device type, brand/model)
- Visual status badges
- Days in repair counter
- Quick access to device details
- Sorting by multiple fields

### Reminders
- Automatic tracking of devices in system > 14 days
- Includes devices with accessories
- Helps prevent long wait times and lost items
- Dashboard notification when reminders are active

## Installation

### Prerequisites
- Python 3.12 or higher
- Poetry (Python dependency manager)
- pyenv (optional, for Python version management)

### Automated Setup

The easiest way to set up the application is using the included setup script:

```bash
./setup.sh
```

This script will:
- Install pyenv (if not already installed)
- Install Poetry (if not already installed)
- Install all dependencies
- Create and run database migrations
- Start the development server

### Manual Setup

If you prefer to set up manually:

1. **Navigate to the project directory:**
   ```bash
   cd repair_cafe
   ```

2. **Install dependencies with Poetry:**
   ```bash
   poetry install --sync
   ```

3. **Activate Poetry virtual environment:**
   ```bash
   source "$(poetry env info --path)/bin/activate"
   ```
   Or use Poetry to run commands:
   ```bash
   poetry run python manage.py [command]
   ```

4. **Run database migrations:**
   ```bash
   poetry run python manage.py migrate
   ```

5. **Create the first admin user:**
   ```bash
   poetry run python manage.py createsuperuser
   ```
   Follow the prompts to create your first admin account.

6. **Run the development server:**
   ```bash
   poetry run python manage.py runserver
   ```

7. **Access the application:**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Usage Guide

### First Time Setup

After installation, you'll need to create users:

1. **Log in as the admin** you created during setup
2. **Create operator users via Django admin panel:**
   - Go to http://127.0.0.1:8000/admin/
   - Log in with admin credentials
   - Navigate to "Users" and click "Add User"
   - Fill in username and password
   - Click "Save and continue editing"
   - Fill in first name, last name, email
   - Check "Is admin" checkbox for admin users, leave unchecked for operators
   - Click "Save"

### For Operators (Reception & Repair)

**All operators can:**

1. **Intake New Device:**
   - Click "New Intake" in navigation
   - Fill out the form with customer and device information
   - Make sure to list any accessories
   - Submit the form
   - Print the generated label and attach to device

2. **Find and Update Devices:**
   - Go to "Repair Station"
   - Scan the barcode or manually enter the Device ID
   - View all device information including accessories
   - Click "Update Status / Add Notes"
   - Select current status, add repairer name and notes
   - Save changes

3. **View Dashboard:**
   - See all devices with status badges
   - Filter by status or intaker
   - Search for specific devices (supports barcode scanning)
   - View device details

4. **Check Reminders:**
   - Click "Reminders" in navigation
   - See devices that have been in system > 14 days
   - Contact customers as needed

### For Admins

**Admins have all operator permissions PLUS:**

1. **User Management (Admin Panel):**
   - Go to http://127.0.0.1:8000/admin/
   - Full Django admin access
   - Create new admin or operator users
   - Edit existing users (change names, emails, roles)
   - Delete users
   - Manage devices directly if needed
   - View detailed device information
   - **Note:** You cannot change your own role - another admin must do it

2. **Monitor All Activity:**
   - Filter devices by intaker to see who registered what
   - Track team performance
   - Manage reminders and follow-ups

### Barcode Scanning

The application supports barcode scanning for quick device lookup:

**How it works:**
- When you print a device label, a scannable Code128 barcode is generated
- Use any USB or wireless barcode scanner (they work like keyboards)
- The scanner reads the barcode, types the Device ID, and presses Enter automatically

**Where you can scan:**
1. **Repair Station page** (recommended):
   - Navigate to "Repair Station"
   - The search field is automatically focused
   - Scan the barcode
   - Device details appear immediately

2. **Dashboard page**:
   - Navigate to "Dashboard"
   - Click in the search field
   - Scan the barcode
   - Device appears in the filtered table

**Note:** Make sure you're on one of these pages before scanning. The barcode scanner needs a text input field to be active.

## Data Model

Each device record contains:
- **Device ID**: Auto-generated (YYYY-NNNN)
- **Intake Date/Time**: Automatically recorded
- **Customer Information**: Name, phone, email
- **Device Information**: Type, brand/model, problem description, accessories
- **Status**: Current repair status
- **Repair Information**: Repairer name, notes, completion date
- **Metadata**: Days in repair, reminder flags

## Customization

### Reminder Threshold
The reminder system is currently set to 14 days. Devices that have been in the system for more than 14 days will appear in the Reminders section.

To change this threshold, edit `devices/models.py` (line 121) in the `needs_reminder()` method:
```python
def needs_reminder(self, days_threshold=14):  # Change 14 to your preferred number
```

### Modify Status Options
Edit `devices/models.py` (line 29) in the `STATUS_CHOICES` list to add or modify device statuses.

### Change Device ID Format
Edit `devices/models.py` (line 87) in the `generate_device_id()` method to customize the Device ID format (currently: YYYY-NNNN).

## Production Deployment

Before deploying to production:

1. **Change SECRET_KEY** in `config/settings.py`
2. **Set DEBUG = False** in `config/settings.py`
3. **Configure ALLOWED_HOSTS** in `config/settings.py`
4. **Use a production database** (PostgreSQL recommended)
5. **Set up static file serving**
6. **Configure email settings** for notifications (optional)
7. **Use a production web server** (gunicorn, uwsgi)
8. **Set up HTTPS**

## Support

For issues or questions about this application, please refer to the Django documentation:
https://docs.djangoproject.com/

## License

This is a custom application for Repair Café operations.
