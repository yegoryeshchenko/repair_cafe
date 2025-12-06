# Repair Café - Project Overview

## Project Structure

```
repair_cafe/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies (minimal)
├── pyproject.toml           # Poetry configuration and dependencies
├── poetry.lock              # Locked dependency versions
├── setup.sh                 # Automated setup script (Unix/Mac)
├── README.md                # Installation and usage guide
├── QUICKSTART.md            # Quick start guide
├── PROJECT_OVERVIEW.md      # This file
├── .gitignore               # Git ignore rules
├── db.sqlite3               # SQLite database (development)
│
├── config/                  # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Main settings (AUTH_USER_MODEL configured)
│   ├── urls.py              # Root URL configuration (custom admin site)
│   ├── wsgi.py              # WSGI config for deployment
│   └── asgi.py              # ASGI config for async
│
└── devices/                 # Main application
    ├── models.py            # User and Device models
    ├── views.py             # View functions (with role-based decorators)
    ├── forms.py             # Django forms (intake, repair, user management)
    ├── urls.py              # URL routing
    ├── admin.py             # Custom admin site with role restrictions
    ├── apps.py              # App configuration
    │
    ├── management/          # Custom management commands
    │   ├── __init__.py
    │   └── commands/
    │       ├── __init__.py
    │       └── sync_user_roles.py   # Sync is_staff with is_admin
    │
    ├── migrations/          # Database migrations
    │   ├── __init__.py
    │   └── 0001_initial.py  # Initial migration
    │
    ├── static/              # Static files
    │   ├── css/
    │   │   └── style.css    # Main stylesheet
    │   └── logo.png         # Repair Café logo (favicon)
    │
    └── templates/
        ├── admin/           # Admin template overrides
        │   └── base_site.html   # Custom admin base (favicon)
        │
        └── devices/         # Application templates
            ├── base.html            # Base template with navigation
            ├── login.html           # Login page
            ├── dashboard.html       # Main dashboard
            ├── intake.html          # Device intake form
            ├── detail.html          # Device details
            ├── update.html          # Update device status
            ├── repair_station.html  # Repair station interface
            ├── print_label.html     # Printable label
            ├── reminders.html       # Reminders page
            ├── user_list.html       # User management (admin only)
            ├── user_form.html       # Create/edit user (admin only)
            └── user_confirm_delete.html  # Confirm user deletion
```

## Application Features

### 0. Authentication & User Management

#### Login System
**URL:** `/login/`
**View:** `login_view()`
**Template:** `login.html`

- Secure authentication for all users
- Username/password login
- Automatic redirect after login
- Role-based access after authentication

#### User Roles
The application implements two distinct user roles:

**Admin Users (`is_admin=True`):**
- Full access to all features
- Can create and manage users (both admins and operators)
- Can access `/users/` page on main site
- Can access Django admin panel at `/admin/`
- Can change other users' roles
- **Cannot change their own role** (security feature - requires another admin)
- Auto-assigned `is_staff=True` for admin panel access

**Operator Users (`is_admin=False`):**
- Can perform device intake (CRUD operations)
- Can update device repair status
- Can view dashboard, search, and filter devices
- Can check reminders
- **Cannot** access Users tab
- **Cannot** access admin panel
- Auto-assigned `is_staff=False`

#### User Management (Admin Only)
**URL:** `/users/`
**View:** `user_list()`, `user_create()`, `user_edit()`, `user_delete()`
**Templates:** `user_list.html`, `user_form.html`, `user_confirm_delete.html`

Admins can:
- View all users with their roles
- Create new admin or operator accounts
- Edit user information (name, email, role, active status)
- Change roles between admin and operator
- Delete users (except themselves)
- Self-role protection: admin checkbox disabled when editing own account

### 1. Device Intake (Reception)
**URL:** `/intake/`
**View:** `device_intake()`
**Template:** `intake.html`
**Access:** All authenticated users (admins and operators)

Reception staff can:
- Fill out intake form with customer and device information
- Record accessories (prominently tracked)
- System automatically generates unique Device ID (YYYY-NNNN format)
- **Auto-assigns logged-in user as intaker** for tracking
- Print label with barcode after submission

### 2. Dashboard
**URL:** `/`
**View:** `dashboard()`
**Template:** `dashboard.html`
**Access:** All authenticated users (admins and operators)

Central hub showing:
- All devices in table format with intaker information
- Status filtering (open, in progress, repaired, etc.)
- **Intaker filtering** (filter by who registered the device)
- Search by Device ID, customer name, phone, device type, brand/model
- Sorting by multiple columns (Device ID, customer, type, status, date, intaker)
- Days in repair counter
- Warning banner for devices needing attention
- Quick action buttons
- **Users tab visible only to admins** in navigation

### 3. Repair Station
**URL:** `/repair-station/`
**View:** `repair_station()`
**Template:** `repair_station.html`
**Access:** All authenticated users (admins and operators)

Repairer interface:
- Search/scan device by ID
- View all device information including accessories (highlighted)
- Quick access to update status
- One-click label printing

### 4. Device Detail
**URL:** `/device/<device_id>/`
**View:** `device_detail()`
**Template:** `detail.html`
**Access:** All authenticated users (admins and operators)

Detailed view showing:
- Complete device information
- Customer contact details
- Timeline (intake, finished dates)
- Intaker information
- Problem description
- Accessories (highlighted if present)
- Repair notes
- Action buttons

### 5. Device Update
**URL:** `/device/<device_id>/update/`
**View:** `device_update()`
**Template:** `update.html`
**Access:** All authenticated users (admins and operators)

Update form for:
- Status selection (5 states)
- Repairer name
- Repair notes/solution
- Automatic date_finished when status changes to final state

### 6. Print Label
**URL:** `/device/<device_id>/print/`
**View:** `print_label()`
**Template:** `print_label.html`
**Access:** All authenticated users (admins and operators)

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
**Access:** All authenticated users (admins and operators)

Shows devices:
- In system > 14 days (configurable threshold)
- Not in final status
- Includes accessories flag
- Sortable table
- Contact information for follow-up

## Data Models

### User Model (Custom)
**File:** `devices/models.py`
**Extends:** `AbstractUser`
**Database Table:** `auth_user`

```python
User(AbstractUser):
    # Custom field
    is_admin           # Boolean - designates admin vs operator role

    # Inherited from AbstractUser
    username           # Unique username
    first_name         # First name
    last_name          # Last name
    email              # Email address
    password           # Hashed password
    is_active          # Account active status
    is_staff           # Auto-synced with is_admin
    is_superuser       # Superuser status
    date_joined        # Auto timestamp
    last_login         # Auto timestamp
```

**Model Methods:**
- `save()`: Automatically sets `is_staff = is_admin` on save
- `is_operator()`: Property that returns `not is_admin`
- `__str__()`: Returns full name or username

**Key Features:**
- Role-based access control (admin/operator)
- Automatic `is_staff` synchronization
- Prevents self-role modification in forms and admin

### Device Model
**File:** `devices/models.py`
**Database Table:** `devices_device`

```python
Device:
    # Auto-generated
    device_id          # CharField - Unique ID (YYYY-NNNN)

    # Intake
    intake_datetime    # DateTimeField - Auto-set on creation
    intaker            # ForeignKey(User) - Who registered the device

    # Customer
    customer_name      # CharField
    phone_number       # CharField
    email_address      # EmailField - Optional

    # Device
    device_type        # CharField
    brand_model        # CharField
    problem_description # TextField
    accessories        # TextField - List of accessories

    # Repair
    status             # CharField - Choices: open, in_progress, repaired, not_repaired, free_for_recycling
    repairer_name      # CharField - Optional
    repair_notes       # TextField - Optional
    date_finished      # DateTimeField - Auto-set when status changes to final state

    # Meta
    created_at         # DateTimeField - Auto timestamp
    updated_at         # DateTimeField - Auto timestamp
```

**Model Methods:**
- `generate_device_id()`: Creates unique ID based on year and sequence
- `save()`: Generates device_id and sets date_finished for final statuses
- `days_in_repair()`: Calculates days between intake and finish/now
- `needs_reminder(days_threshold=14)`: Returns True if device is in system > threshold days and not finished
- `__str__()`: Returns "device_id - customer_name - device_type"

## Workflows

### Initial Setup Workflow (First Time)
1. Run `./setup.sh` or install dependencies manually
2. Create first admin user: `poetry run python manage.py createsuperuser`
3. Log in to application at http://127.0.0.1:8000/
4. Go to "Users" tab (visible to admins only)
5. Create operator accounts for team members
6. Distribute login credentials to team

### User Management Workflow (Admin Only)
1. Admin logs in to application
2. Click "Users" tab in navigation
3. View list of all users with their roles
4. To create new user:
   - Click "Create User"
   - Fill in username, name, email, password
   - Check "Admin User" for admin role, leave unchecked for operator
   - Submit
5. To edit user:
   - Click "Edit" next to user
   - Modify details (cannot change own role - disabled)
   - Save changes
6. To delete user:
   - Click "Delete" (not available for self)
   - Confirm deletion

### Reception Workflow (All Users)
1. Log in to application
2. Customer brings device → Navigate to "New Intake"
3. Fill form with all information
4. **Important:** List all accessories in dedicated field
5. Submit form
6. System generates Device ID and assigns logged-in user as intaker
7. Print label automatically shown
8. Attach label to device and accessories

### Repair Workflow (All Users)
1. Log in to application
2. Repairer picks up device → Go to "Repair Station"
3. Enter/scan Device ID
4. System shows all info including **accessories warning** and intaker
5. Click "Update Status / Add Notes"
6. Select status, add name and notes
7. Save
8. System auto-records completion date if final status

### Follow-up Workflow (All Users)
1. Log in to application
2. Check "Reminders" tab
3. See devices > 14 days
4. Devices with accessories are highlighted
5. Contact customers using displayed phone/email
6. Update status accordingly
7. Admins can filter by intaker to assign follow-ups

## Key Design Decisions

### 1. Role-Based Access Control
**Two-tier system: Admin and Operator**
- **Simple role model**: Single `is_admin` boolean field instead of complex permissions
- **Clear separation**: Admins manage users, operators manage devices
- **Self-protection**: Admins cannot change their own role (prevents accidental lockout)
- **Auto-sync**: `is_staff` automatically synced with `is_admin` for admin panel access
- **Custom admin site**: Separate admin site instance with role-based access restrictions
- **No Groups**: Simplified permissions - only admin/operator distinction

**Rationale:**
- Repair Cafés typically have small teams with clear roles
- Simple system is easier to understand and maintain
- Prevents permission complexity for non-technical users

### 2. User Tracking (Intaker Field)
- Every device automatically records who performed the intake
- Enables accountability and performance tracking
- Allows filtering devices by intaker on dashboard
- ForeignKey relationship with User model

### 3. Device ID Format
- Format: YYYY-NNNN (e.g., 2025-0042)
- Resets annually
- Sequential numbering
- Easy to read and scan
- Unique within each year

### 4. Accessories Handling
- Dedicated text field (not checkbox)
- Allows listing specific items
- Highlighted in yellow on all views
- Included on printable label
- Flagged in reminders
- Critical for preventing lost items

### 5. Status States
Five clear states covering all scenarios:
- **Open**: Just received, not started
- **In Progress**: Being worked on
- **Repaired**: Successfully fixed
- **Not Repaired**: Cannot be fixed
- **Free for Recycling**: Customer approved disposal

### 6. Automatic Date Tracking
- `intake_datetime`: Set on creation with logged-in user
- `date_finished`: Auto-set when status becomes final
- `days_in_repair`: Calculated on the fly
- No manual date entry required

### 7. Reminder Logic
- **14-day threshold** (configurable in code)
- Only for non-final statuses
- Includes all devices with accessories
- Prevents items from being forgotten
- Dashboard notification badge

## Customization Points

### Change Reminder Threshold
`devices/models.py` line 121:
```python
def needs_reminder(self, days_threshold=14):  # Change 14 to desired days
```

### Add/Modify Status Options
`devices/models.py` line 29:
```python
STATUS_CHOICES = [
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    # Add more here
]
```

### Modify Device ID Format
`devices/models.py` line 87:
```python
def generate_device_id(self):
    return f"{year}-{new_number:04d}"  # Modify format here (e.g., :05d for 5 digits)
```

### Change Colors/Styling
`devices/static/css/style.css`:
- CSS variables at top for color scheme
- Status badge colors around line 150
- Print styles at bottom
- Responsive breakpoints

### Modify Role Permissions
`devices/views.py` - Update decorator:
```python
@admin_required  # Custom decorator for admin-only views
def user_list(request):
    # Admin only function
```

## Admin Interface

### Custom Admin Site
**Access:** `/admin/` (admins only)
**Implementation:** `devices/admin.py` - `RepairCafeAdminSite` class

**Custom Features:**
- **Role-based access**: Only users with `is_admin=True` can access
- **Simplified user management**: Removed Groups, only admin/operator roles
- **Self-role protection**: `get_readonly_fields()` prevents self-role changes
- **Custom branding**: "Repair Café Administration" header
- **Favicon**: Same logo as main site

**Available Models:**
- **Users**: Full CRUD with simplified permissions interface
- **Devices**: Full CRUD with advanced filtering

**Features:**
- Advanced filtering by status, type, intaker, date
- Search across all device and user fields
- Bulk operations
- Organized fieldsets
- Readonly fields (device_id, timestamps)

### Standard Django Admin vs. Main Site
**Django Admin (`/admin/`):**
- Power users (admins only)
- Full database access
- Advanced filtering and bulk operations
- Technical interface

**Main Site User Management (`/users/`):**
- User-friendly interface
- Simplified user creation
- Clear role selection
- Integrated with main application flow

## Security Considerations for Production

### Application Security
1. **Change SECRET_KEY** in `config/settings.py` to a random string
2. **Set DEBUG = False** in production
3. **Configure ALLOWED_HOSTS** with your domain
4. **Use production database** (PostgreSQL recommended)
5. **Enable HTTPS** (required for secure authentication)
6. **Set up proper static file serving** (Whitenoise or S3)
7. **Configure backup strategy** for database
8. **Strong password policy** (enforced by Django validators)

### User Authentication Security
9. **First admin user**: Create with `createsuperuser` command
10. **Self-role protection**: Admins cannot change own role (prevents lockout)
11. **Password hashing**: Django's PBKDF2 algorithm (secure by default)
12. **Session security**: Configure SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE
13. **Login required**: All views protected with `@login_required` decorator

### Access Control
14. **Role-based access**: Custom `@admin_required` decorator
15. **Admin panel protection**: Custom admin site checks `is_admin` field
16. **No permission escalation**: Operators cannot access admin functions
17. **Form-level protection**: Self-role editing disabled in forms

## Quick Start Commands

```bash
# Automated Setup (first time)
./setup.sh

# Manual Setup with Poetry
poetry install --sync
poetry run python manage.py migrate

# Create first admin user
poetry run python manage.py createsuperuser

# Sync existing user roles (if upgrading)
poetry run python manage.py sync_user_roles

# Run development server
poetry run python manage.py runserver

# Or activate Poetry shell first
poetry shell
python manage.py runserver

# Create migrations (after model changes)
poetry run python manage.py makemigrations

# Apply migrations
poetry run python manage.py migrate

# Collect static files (for production)
poetry run python manage.py collectstatic

# Create database backup
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)
```

## URLs Reference

| URL | Purpose | Access |
|-----|---------|--------|
| `/login/` | User login | Public |
| `/logout/` | User logout | Authenticated |
| `/` | Dashboard - view all devices | All authenticated |
| `/intake/` | New device intake form | All authenticated |
| `/repair-station/` | Repair station search interface | All authenticated |
| `/reminders/` | View devices needing attention (>14 days) | All authenticated |
| `/device/<id>/` | Device detail view | All authenticated |
| `/device/<id>/update/` | Update device status and notes | All authenticated |
| `/device/<id>/print/` | Print device label | All authenticated |
| `/users/` | User management list | Admins only |
| `/users/create/` | Create new user | Admins only |
| `/users/<id>/edit/` | Edit user (self-role protected) | Admins only |
| `/users/<id>/delete/` | Delete user (not self) | Admins only |
| `/admin/` | Django admin interface | Admins only |

## Technology Stack

### Backend
- **Framework:** Django 4.2+
- **Language:** Python 3.8+
- **ORM:** Django ORM
- **Authentication:** Django Auth with custom User model
- **Forms:** Django Forms with custom validation

### Database
- **Development:** SQLite3 (included)
- **Production:** PostgreSQL (recommended)
- **Migrations:** Django Migrations

### Frontend
- **HTML:** HTML5 with semantic markup
- **CSS:** CSS3 vanilla (no framework)
- **JavaScript:** Minimal/none (form-focused application)
- **Templates:** Django Template Language
- **Icons/Logo:** Static PNG images

### Dependency Management
- **Poetry:** Modern Python dependency management
- **pyproject.toml:** Dependency configuration
- **poetry.lock:** Locked versions for reproducibility

### Development Tools
- **setup.sh:** Automated setup script
- **Management commands:** Custom Django commands (sync_user_roles)

## Browser Compatibility

- **Primary:** Modern browsers (Chrome, Firefox, Safari, Edge)
- **Print:** Print functionality tested on major browsers
- **Responsive:** Optimized for desktop and tablet
- **Mobile:** Mobile-friendly but optimized for larger screens
- **Accessibility:** Semantic HTML for screen readers

## Implemented Features

✅ **User Role Management:** Two-tier admin/operator system with self-role protection
✅ **User Authentication:** Secure login with role-based access control
✅ **Device Tracking:** Complete intake to completion workflow
✅ **Accessories Tracking:** Prominently highlighted to prevent loss
✅ **Automatic Reminders:** 14-day threshold for follow-ups
✅ **Intaker Tracking:** Know who registered each device
✅ **Search & Filter:** Multiple criteria including status, intaker, customer info
✅ **Print Labels:** Browser-based label printing
✅ **Status Management:** Five clear device states
✅ **Custom Admin:** Simplified admin interface with role restrictions

## Future Enhancement Ideas

1. **Barcode Generation:** Use python-barcode library for scannable barcodes
2. **Email Notifications:** Automated reminders to customers
3. **Statistics Dashboard:** Charts showing repair metrics, turnaround time
4. **PDF Export:** Generate PDF labels instead of browser print
5. **Photo Upload:** Attach device photos for documentation
6. **Parts Inventory:** Track spare parts and usage
7. **QR Code:** Alternative to barcode for mobile scanning
8. **SMS Notifications:** Send status updates to customers
9. **Multi-language:** Support for different languages
10. **Export Reports:** Excel/CSV export of device records
11. **Digital Signatures:** Customer signature on intake
12. **Multi-location:** Support for multiple repair café locations
13. **Appointment System:** Schedule repair appointments
14. **Payment Tracking:** Optional donation/payment tracking

## Notes for Developers

### Custom User Model
- Extends `AbstractUser` not `AbstractBaseUser`
- Uses `auth_user` table for compatibility
- `is_admin` field controls all permissions
- `save()` method syncs `is_staff` automatically

### View Decorators
- `@login_required`: All views require authentication
- `@admin_required`: Custom decorator for admin-only views
- Both decorators redirect to appropriate pages

### Form Patterns
- `UserEditForm` accepts `current_user` kwarg for self-detection
- Forms disable fields dynamically in `__init__()`
- Self-role protection implemented at form level

### Model Signals
- No signals used - logic in model `save()` methods
- Keeps code simple and traceable
- Easy to understand for maintenance

### Testing Recommendations
- Test role-based access restrictions
- Test self-role protection
- Test intaker auto-assignment
- Test device ID generation across year boundaries
- Test reminder calculations
