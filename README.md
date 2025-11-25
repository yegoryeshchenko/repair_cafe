# Repair Café Device Tracking System

A Django web application to help Repair Cafés track devices brought by customers for repair.

## Features

### Reception/Intake Workflow
- Easy-to-use intake form for receptionists
- Captures all customer and device information
- Automatic Device ID generation (format: YYYY-NNNN, e.g., 2025-0042)
- Accessories tracking with prominent display
- Printable labels with barcode representation for device identification

### Repair Station Workflow
- Quick device search/scan by Device ID
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
- Search functionality (Device ID, customer name, phone, device type)
- Visual status badges
- Days in repair counter
- Quick access to device details

### Reminders
- Automatic tracking of devices in system > 14 days
- Includes devices with accessories
- Helps prevent long wait times and lost items
- Dashboard notification when reminders are active

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Navigate to the project directory:**
   ```bash
   cd repair_cafe
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Usage Guide

### For Receptionists

1. **Intake New Device:**
   - Click "New Intake" in navigation
   - Fill out the form with customer and device information
   - Make sure to list any accessories
   - Submit the form
   - Print the generated label and attach to device

2. **Print Additional Labels:**
   - Find device in dashboard
   - Click "View" then "Print Label"

### For Repairers

1. **Find Device:**
   - Go to "Repair Station"
   - Enter or scan the Device ID
   - All device information will be displayed, including accessories

2. **Update Status:**
   - Click "Update Status / Add Notes"
   - Select current status
   - Add your name as repairer
   - Add repair notes/solution
   - Save changes

### For Managers

1. **Monitor All Devices:**
   - View dashboard for overview
   - Filter by status to see specific categories
   - Use search to find specific devices

2. **Check Reminders:**
   - Click "Reminders" in navigation
   - See devices that have been in system > 14 days
   - Pay special attention to devices with accessories
   - Contact customers or prioritize these repairs

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

### Change Reminder Threshold
Edit `devices/models.py`, line ~100 in the `needs_reminder()` method to change the 14-day default.

### Modify Status Options
Edit `devices/models.py`, line ~8 in the `STATUS_CHOICES` list.

### Change Device ID Format
Edit `devices/models.py`, line ~60 in the `generate_device_id()` method.

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
