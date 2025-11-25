# Repair Café - Project Overview

## Project Structure

```
repair_cafe/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── setup.sh                  # Quick setup script (Unix/Mac)
├── README.md                 # Installation and usage guide
├── .gitignore               # Git ignore rules
│
├── config/                   # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Main settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI config for deployment
│   └── asgi.py              # ASGI config for async
│
└── devices/                  # Main application
    ├── models.py            # Device data model
    ├── views.py             # View functions
    ├── forms.py             # Django forms
    ├── urls.py              # URL routing
    ├── admin.py             # Admin interface config
    ├── apps.py              # App configuration
    │
    ├── migrations/          # Database migrations
    │   └── __init__.py
    │
    ├── static/              # Static files (CSS, JS, images)
    │   └── css/
    │       └── style.css    # Main stylesheet
    │
    └── templates/devices/   # HTML templates
        ├── base.html        # Base template
        ├── dashboard.html   # Main dashboard
        ├── intake.html      # Device intake form
        ├── detail.html      # Device details
        ├── update.html      # Update device status
        ├── repair_station.html  # Repair station interface
        ├── print_label.html     # Printable label
        └── reminders.html       # Reminders page
```

## Application Features

### 1. Device Intake (Reception)
**URL:** `/intake/`
**View:** `device_intake()`
**Template:** `intake.html`

Reception staff can:
- Fill out intake form with customer and device information
- Record accessories (prominently tracked)
- System automatically generates unique Device ID (YYYY-NNNN format)
- Print label with barcode after submission

### 2. Dashboard
**URL:** `/`
**View:** `dashboard()`
**Template:** `dashboard.html`

Central hub showing:
- All devices in table format
- Status filtering (open, in progress, repaired, etc.)
- Search by Device ID, customer name, phone, device type
- Days in repair counter
- Warning banner for devices needing attention
- Quick action buttons

### 3. Repair Station
**URL:** `/repair-station/`
**View:** `repair_station()`
**Template:** `repair_station.html`

Repairer interface:
- Search/scan device by ID
- View all device information including accessories (highlighted)
- Quick access to update status
- One-click label printing

### 4. Device Detail
**URL:** `/device/<device_id>/`
**View:** `device_detail()`
**Template:** `detail.html`

Detailed view showing:
- Complete device information
- Customer contact details
- Timeline (intake, finished dates)
- Problem description
- Accessories (highlighted if present)
- Repair notes
- Action buttons

### 5. Device Update
**URL:** `/device/<device_id>/update/`
**View:** `device_update()`
**Template:** `update.html`

Update form for:
- Status selection (5 states)
- Repairer name
- Repair notes/solution
- Automatic date_finished when status changes to final state

### 6. Print Label
**URL:** `/device/<device_id>/print/`
**View:** `print_label()`
**Template:** `print_label.html`

Printable label with:
- Device ID (large)
- Barcode representation
- Customer info
- Device details
- Accessories (highlighted in yellow box)
- Print-optimized CSS

### 7. Reminders
**URL:** `/reminders/`
**View:** `reminders()`
**Template:** `reminders.html`

Shows devices:
- In system > 14 days
- Not in final status
- Includes accessories flag
- Sortable table
- Contact information for follow-up

## Data Model: Device

```python
Device:
    # Auto-generated
    device_id          # Unique ID (YYYY-NNNN)

    # Intake
    intake_datetime    # Auto-set on creation

    # Customer
    customer_name
    phone_number
    email_address      # Optional

    # Device
    device_type
    brand_model
    problem_description
    accessories        # Text field for listing items

    # Repair
    status             # Choices: open, in_progress, repaired, not_repaired, free_for_recycling
    repairer_name      # Optional
    repair_notes       # Optional
    date_finished      # Auto-set when status changes to final state

    # Meta
    created_at         # Auto timestamp
    updated_at         # Auto timestamp
```

### Model Methods:
- `generate_device_id()`: Creates unique ID based on year and sequence
- `days_in_repair()`: Calculates days between intake and finish/now
- `needs_reminder()`: Returns True if device is in system > 14 days and not finished

## Workflows

### Reception Workflow
1. Customer brings device → Navigate to "New Intake"
2. Fill form with all information
3. **Important:** List all accessories in dedicated field
4. Submit form
5. System generates Device ID
6. Print label automatically shown
7. Attach label to device and accessories

### Repair Workflow
1. Repairer picks up device → Go to "Repair Station"
2. Enter/scan Device ID
3. System shows all info including **accessories warning**
4. Click "Update Status / Add Notes"
5. Select status, add name and notes
6. Save
7. System auto-records completion date if final status

### Follow-up Workflow
1. Manager checks "Reminders"
2. See devices > 14 days
3. Devices with accessories are highlighted
4. Contact customers using displayed phone/email
5. Update status accordingly

## Key Design Decisions

### 1. Device ID Format
- Format: YYYY-NNNN (e.g., 2025-0042)
- Resets annually
- Sequential numbering
- Easy to read and scan

### 2. Accessories Handling
- Dedicated text field (not checkbox)
- Allows listing specific items
- Highlighted in yellow on all views
- Included on printable label
- Flagged in reminders

### 3. Status States
Five clear states covering all scenarios:
- **Open**: Just received, not started
- **In Progress**: Being worked on
- **Repaired**: Successfully fixed
- **Not Repaired**: Cannot be fixed
- **Free for Recycling**: Customer approved disposal

### 4. Automatic Date Tracking
- `intake_datetime`: Set on creation
- `date_finished`: Auto-set when status becomes final
- `days_in_repair`: Calculated on the fly

### 5. Reminder Logic
- 14-day threshold (configurable)
- Only for non-final statuses
- Includes all devices with accessories
- Prevents items from being forgotten

## Customization Points

### Change Reminder Threshold
`devices/models.py` line ~100:
```python
def needs_reminder(self, days_threshold=14):  # Change 14 to desired days
```

### Add/Modify Status Options
`devices/models.py` line ~8:
```python
STATUS_CHOICES = [
    ('open', 'Open'),
    # Add more here
]
```

### Modify Device ID Format
`devices/models.py` line ~60:
```python
def generate_device_id(self):
    return f"{year}-{new_number:04d}"  # Modify format here
```

### Change Colors/Styling
`devices/static/css/style.css`:
- CSS variables at top for color scheme
- Status badge colors around line 150
- Print styles at bottom

## Admin Interface

Access at `/admin/`

Features:
- Full CRUD operations
- Advanced filtering by status, type, date
- Search across all fields
- Bulk operations
- Organized fieldsets

## Security Considerations for Production

1. **Change SECRET_KEY** in settings.py
2. **Set DEBUG = False**
3. **Configure ALLOWED_HOSTS**
4. **Use production database** (PostgreSQL)
5. **Enable HTTPS**
6. **Set up proper static file serving**
7. **Configure backup strategy**
8. **Add user authentication** if needed
9. **Review permissions**

## Quick Start Commands

```bash
# Setup (first time)
./setup.sh

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Create migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files (for production)
python manage.py collectstatic
```

## URLs Reference

| URL | Purpose |
|-----|---------|
| `/` | Dashboard - view all devices |
| `/intake/` | New device intake form |
| `/repair-station/` | Repair station search interface |
| `/reminders/` | View devices needing attention |
| `/device/<id>/` | Device detail view |
| `/device/<id>/update/` | Update device status |
| `/device/<id>/print/` | Print device label |
| `/admin/` | Django admin interface |

## Technology Stack

- **Backend:** Django 4.2+
- **Database:** SQLite (development), PostgreSQL (recommended for production)
- **Frontend:** HTML5, CSS3 (vanilla, no framework)
- **Templates:** Django Template Language
- **Forms:** Django Forms

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Print functionality tested on major browsers
- Responsive design for tablets (main use case)
- Mobile-friendly but optimized for desktop/tablet

## Future Enhancement Ideas

1. **Barcode Generation:** Use python-barcode library for real barcodes
2. **Email Notifications:** Send reminders automatically
3. **Statistics Dashboard:** Charts and metrics
4. **PDF Export:** Generate PDF labels
5. **User Roles:** Different permissions for reception/repair/admin
6. **Photo Upload:** Attach device photos
7. **Parts Inventory:** Track spare parts
8. **QR Code:** Alternative to barcode
9. **SMS Notifications:** Send status updates to customers
10. **Multi-language:** Support for different languages
