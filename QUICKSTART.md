# Quick Start Guide

## Getting Started

### First Time Setup

If this is your first time, run the automated setup script:

```bash
./setup.sh
```

This will install all dependencies and start the server automatically.

### If Server is Already Running 🎉

The Django development server may already be running at:
**http://127.0.0.1:8000/**

You can open this URL in your browser to start using the application.

## Important Commands

All commands use Poetry to manage the virtual environment:

### Start the Server
```bash
poetry run python manage.py runserver
```

Or if you've activated the Poetry shell:
```bash
source "$(poetry env info --path)/bin/activate"
python manage.py runserver
```

### Create the First Admin User
```bash
poetry run python manage.py createsuperuser
```
You'll be prompted for:
- Username
- Email (optional, can press Enter to skip)
- Password (type twice)
- First Name and Last Name

**Important:** This user will automatically be set as an admin with full privileges.

### Create Additional Users
Once you have an admin account:
1. Log into the application at http://127.0.0.1:8000/
2. Go to "Users" tab (visible to admins only)
3. Click "Create User" to add operators or other admins

### Stop the Server
Press `Ctrl+C` in the terminal where the server is running.

### Other Useful Commands

**Check if server is running:**
```bash
lsof -ti:8000
```

**Apply database migrations (after model changes):**
```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

**Sync user roles (after upgrading):**
```bash
poetry run python manage.py sync_user_roles
```

**Access Django shell:**
```bash
poetry run python manage.py shell
```

**Create a database backup:**
```bash
cp db.sqlite3 db.sqlite3.backup
```

**Install new dependencies:**
```bash
poetry add package-name
```

## URLs

| URL | Purpose | Access |
|-----|---------|--------|
| http://127.0.0.1:8000/ | Main Dashboard | All users |
| http://127.0.0.1:8000/login/ | Login Page | Public |
| http://127.0.0.1:8000/intake/ | New Device Intake | All users |
| http://127.0.0.1:8000/repair-station/ | Repair Station | All users |
| http://127.0.0.1:8000/reminders/ | Reminders | All users |
| http://127.0.0.1:8000/users/ | User Management | Admins only |
| http://127.0.0.1:8000/admin/ | Django Admin Panel | Admins only |

## First Time Setup Checklist

- [ ] Run `./setup.sh` to install dependencies
- [ ] **Create first admin user:** `poetry run python manage.py createsuperuser`
- [ ] **Log in** at http://127.0.0.1:8000/
- [ ] **Create operator users** via Users tab or admin panel
- [ ] **Test intake workflow** with a sample device

## Understanding User Roles

### Admin Users
- Can do everything operators can do
- Can access "Users" tab on main site
- Can access Django admin panel at `/admin`
- Can create and manage other users
- **Cannot change their own role** (security feature)

### Operator Users
- Can intake new devices
- Can update device status and add repair notes
- Can view dashboard, search, and filter devices
- Can check reminders
- **Cannot** access Users tab
- **Cannot** access admin panel

## Using the Application

### 1. First Login & User Setup (Admin Only)
1. Log in with the superuser account you created
2. Click "Users" tab in navigation
3. Click "Create User"
4. Fill in details (username, name, email, password)
5. Check "Admin User" for admins, leave unchecked for operators
6. Create accounts for your team

### 2. Reception: Add New Device (All Users)
1. Log in to the application
2. Click "New Intake" in the navigation
3. Fill out customer and device information
4. List any accessories in the accessories field
5. Submit - Device ID is auto-generated
6. Print the label and attach to device

### 3. Repair Station: Update Device (All Users)
1. Click "Repair Station"
2. Enter or scan the Device ID
3. Review device information and accessories
4. Click "Update Status / Add Notes"
5. Select status, add repairer name and notes
6. Save changes

### 4. Dashboard: View All Devices (All Users)
1. Go to home page (Dashboard)
2. Filter by status or intaker (who registered it)
3. Use search bar to find specific devices
4. Sort by different columns
5. Click "View" to see full device details

### 5. Reminders: Check Overdue Devices (All Users)
1. Click "Reminders"
2. See devices that have been in system > 14 days
3. Note any devices with accessories
4. Contact customers as needed

## Troubleshooting

**Server won't start:**
```bash
# Check if something is using port 8000
lsof -ti:8000

# If yes, kill it
kill $(lsof -ti:8000)

# Then start again
poetry run python manage.py runserver
```

**"No module named Django" error:**
```bash
# Make sure Poetry dependencies are installed
poetry install --sync

# Then run with Poetry
poetry run python manage.py runserver
```

**Operator can access admin panel:**
```bash
# Sync user roles to ensure is_staff matches is_admin
poetry run python manage.py sync_user_roles
```

**Database issues:**
```bash
# Reset database (WARNING: deletes all data)
rm db.sqlite3
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

**Permission denied when editing own role:**
This is a security feature! You cannot change your own admin role. Ask another admin to change it for you.

## Development Tips

**Want to use a different port?**
```bash
poetry run python manage.py runserver 8080
```

**Want to access from other devices on your network?**
```bash
poetry run python manage.py runserver 0.0.0.0:8000
```

**Need to install additional packages?**
```bash
poetry add package-name
```

**Activate Poetry shell for easier commands:**
```bash
poetry shell
# Now you can run: python manage.py runserver
# Without the "poetry run" prefix
```

## Security Notes

- **Admin self-protection:** Admins cannot change their own role to prevent accidental lockout
- **Role segregation:** Operators are completely blocked from admin panel
- **Password requirements:** Django enforces strong password policies
- **Change default passwords:** Always change the superuser password after setup

## Next Steps

1. **Create an admin user** with `createsuperuser` command
2. **Log in** and create operator accounts for your team
3. **Test the workflow** with sample devices
4. **Customize reminder threshold** if 14 days doesn't fit your needs
5. **Set up production deployment** when ready

---

**Need help?** Check the README.md for detailed documentation.
