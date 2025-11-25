# Quick Start Guide

## The Application is Already Running! 🎉

The Django development server is currently running at:
**http://127.0.0.1:8000/**

You can open this URL in your browser to start using the application.

## Important Commands

All commands should be run using the virtual environment's Python. Use these commands:

### Start the Server
```bash
./venv/bin/python manage.py runserver
```

### Create an Admin User
```bash
./venv/bin/python manage.py createsuperuser
```
You'll be prompted for:
- Username
- Email (optional, can press Enter to skip)
- Password (type twice)

### Stop the Server
Press `Ctrl+C` in the terminal where the server is running.

### Other Useful Commands

**Check if server is running:**
```bash
lsof -ti:8000
```

**Apply database migrations (after model changes):**
```bash
./venv/bin/python manage.py makemigrations
./venv/bin/python manage.py migrate
```

**Access Django shell:**
```bash
./venv/bin/python manage.py shell
```

**Create a database backup:**
```bash
cp db.sqlite3 db.sqlite3.backup
```

## URLs

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:8000/ | Main Dashboard |
| http://127.0.0.1:8000/intake/ | New Device Intake |
| http://127.0.0.1:8000/repair-station/ | Repair Station |
| http://127.0.0.1:8000/reminders/ | Reminders |
| http://127.0.0.1:8000/admin/ | Admin Interface |

## First Time Setup Checklist

- [x] Virtual environment created
- [x] Django installed
- [x] Database migrations applied
- [x] Server started
- [ ] **Create admin user** (run the command above)
- [ ] **Open browser** and go to http://127.0.0.1:8000/

## Using the Application

### 1. Reception: Add New Device
1. Click "New Intake" in the navigation
2. Fill out the form
3. Submit
4. Print the generated label

### 2. Repair Station: Update Device
1. Click "Repair Station"
2. Enter the Device ID
3. View device information
4. Click "Update Status / Add Notes"
5. Select status and add notes
6. Save

### 3. Dashboard: View All Devices
1. Go to home page (Dashboard)
2. Use filters to see specific statuses
3. Use search bar to find devices
4. Click "View" to see device details

### 4. Reminders: Check Overdue Devices
1. Click "Reminders"
2. See devices that have been waiting > 14 days
3. Contact customers if needed

## Troubleshooting

**Server won't start:**
```bash
# Check if something is using port 8000
lsof -ti:8000

# If yes, kill it
kill $(lsof -ti:8000)

# Then start again
./venv/bin/python manage.py runserver
```

**"No module named Django" error:**
```bash
# Make sure to use venv's python
./venv/bin/python manage.py runserver

# NOT just: python manage.py runserver
```

**Database issues:**
```bash
# Reset database (WARNING: deletes all data)
rm db.sqlite3
./venv/bin/python manage.py migrate
```

## Development Tips

**Want to use a different port?**
```bash
./venv/bin/python manage.py runserver 8080
```

**Want to access from other devices on your network?**
```bash
./venv/bin/python manage.py runserver 0.0.0.0:8000
```

**Need to install additional packages?**
```bash
./venv/bin/pip install package-name
```

## Next Steps

1. **Create an admin user** so you can access the admin interface
2. **Open the application** in your browser
3. **Add some test devices** to see how it works
4. **Customize** the styling or features as needed

---

**Need help?** Check the README.md for detailed documentation or PROJECT_OVERVIEW.md for technical details.
