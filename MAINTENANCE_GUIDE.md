# Repair Café - Maintenance & Update Guide

## Quick Reference: After Code Changes

### Scenario 1: Code Changes ONLY (Views, Templates, Settings, CSS, JS)
**What changed:** Python logic, HTML templates, CSS styles, JavaScript
**Database affected:** NO
**Data lost:** NO

```bash
# On LOCAL machine
git add .
git commit -m "Description of changes"
git push origin main

# On SERVER
cd /var/www/repair_cafe
git pull origin main
sudo systemctl restart gunicorn

# If CSS/JS changed, also restart Nginx
sudo systemctl restart nginx
```

**✅ Safe:** Your database and all user data remain untouched.

---

### Scenario 2: Static Files Changed (CSS, Images, JavaScript)
**What changed:** Files in `devices/static/`
**Database affected:** NO
**Data lost:** NO

```bash
# On LOCAL machine
git add .
git commit -m "Updated CSS/images"
git push origin main

# On SERVER
cd /var/www/repair_cafe
git pull origin main
export $(cat .env | xargs)
poetry run python manage.py collectstatic --no-input
sudo systemctl restart gunicorn
```

**✅ Safe:** Only static files are recopied, no database changes.

---

### Scenario 3: Dependencies Changed (pyproject.toml)
**What changed:** Added/updated Python packages
**Database affected:** NO
**Data lost:** NO

```bash
# On LOCAL machine
poetry lock
git add pyproject.toml poetry.lock
git commit -m "Updated dependencies"
git push origin main

# On SERVER
cd /var/www/repair_cafe
git pull origin main
poetry install --only main --no-root
sudo systemctl restart gunicorn
```

**✅ Safe:** Only installs new/updated packages.

---

### Scenario 4: Model Changes - NEW Field Added (Safe)
**What changed:** Added new field to Device or User model
**Database affected:** YES
**Data lost:** NO - Existing data preserved

```bash
# On LOCAL machine
# After editing models.py
poetry run python manage.py makemigrations
git add .
git commit -m "Added new field to Device model"
git push origin main

# On SERVER
cd /var/www/repair_cafe
git pull origin main
export $(cat .env | xargs)
poetry run python manage.py migrate  # This adds the new column
sudo systemctl restart gunicorn
```

**✅ Safe:** New column added, all existing data stays intact.

---

### Scenario 5: Model Changes - Field Removed (⚠️ CAUTION)
**What changed:** Removed field from model
**Database affected:** YES
**Data lost:** YES - Data in that field will be deleted

```bash
# On LOCAL machine
# BEFORE editing models.py - consider if you need that data!
# Maybe export it first or create a data migration

poetry run python manage.py makemigrations
git add .
git commit -m "Removed unused field"
git push origin main

# On SERVER - BACKUP FIRST!
cd /var/www/repair_cafe
/home/repaircafe/backup_database.sh  # BACKUP FIRST!

git pull origin main
export $(cat .env | xargs)
poetry run python manage.py migrate  # This drops the column
sudo systemctl restart gunicorn
```

**⚠️ Warning:** The field and its data will be permanently deleted. Always backup first!

---

### Scenario 6: Model Changes - Renamed Field
**What changed:** Renamed a field (e.g., `phone` → `phone_number`)
**Database affected:** YES
**Data lost:** NO if done correctly

**Option A: Django Auto-rename (Risky)**
```bash
# Django might ask: "Did you rename field X to Y?"
# Answer carefully!
```

**Option B: Manual (Safer)**
1. Add new field
2. Write data migration to copy data
3. Remove old field
4. This preserves all data

---

## What NEVER Affects the Database

These operations are **100% safe** and never touch your data:

✅ **Always Safe:**
- `git pull` - Downloads code
- `systemctl restart gunicorn` - Restarts application server
- `systemctl restart nginx` - Restarts web server
- `poetry install` - Installs packages
- `collectstatic` - Copies CSS/JS/images
- Editing `.env` file (then restart gunicorn)
- Editing settings.py (without model changes)
- Editing views.py, forms.py, urls.py
- Editing templates (HTML files)

---

## What CAN Affect the Database

❌ **Be Careful With:**

| Command | What It Does | Data Loss Risk |
|---------|-------------|----------------|
| `python manage.py migrate` | Applies database schema changes | Low (if adding), High (if removing) |
| `python manage.py flush` | **DELETES ALL DATA** | **TOTAL DATA LOSS** |
| `python manage.py createsuperuser` | Creates new user | None (adds data) |
| Editing `models.py` then migrating | Changes database structure | Depends on change |
| `DROP DATABASE` in psql | **DELETES ENTIRE DATABASE** | **TOTAL DATA LOSS** |

---

## Database Backup Strategy

### Automatic Backups (Recommended)

#### Set Up Automated Daily Backups

**1. Create the backup script:**

```bash
# On SERVER
nano /home/repaircafe/backup_database.sh
```

**Paste this:**

```bash
#!/bin/bash
#
# Repair Café Database Backup Script
# Runs daily at 2 AM (configured in crontab)
#

BACKUP_DIR="/home/repaircafe/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="repair_cafe_db"
DB_USER="repair_cafe_user"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Set password from environment (stored in .pgpass)
export PGPASSWORD='etBxrGnAP0e*NJUX69s*'

# Dump database to SQL file
pg_dump -h localhost -U $DB_USER $DB_NAME > "$BACKUP_DIR/repair_cafe_$DATE.sql"

# Compress the backup
gzip "$BACKUP_DIR/repair_cafe_$DATE.sql"

# Delete backups older than 30 days
find $BACKUP_DIR -name "repair_cafe_*.sql.gz" -mtime +30 -delete

# Log the backup
echo "$(date): Backup completed - repair_cafe_$DATE.sql.gz" >> $BACKUP_DIR/backup.log

# Unset password
unset PGPASSWORD
```

**2. Make it executable:**

```bash
chmod +x /home/repaircafe/backup_database.sh
```

**3. Test it:**

```bash
/home/repaircafe/backup_database.sh
ls -lh /home/repaircafe/backups/
```

**4. Schedule automatic backups:**

```bash
crontab -e
```

**Add this line:**

```bash
# Daily database backup at 2 AM
0 2 * * * /home/repaircafe/backup_database.sh

# Weekly backup at Sunday 3 AM (extra safety)
0 3 * * 0 /home/repaircafe/backup_database.sh
```

**Save:** Ctrl+X, then Y, then Enter

---

### Manual Backup (Before Risky Operations)

**Before any risky operation, create a manual backup:**

```bash
# On SERVER
cd /home/repaircafe
mkdir -p backups
export PGPASSWORD='etBxrGnAP0e*NJUX69s*'
pg_dump -h localhost -U repair_cafe_user repair_cafe_db > backups/manual_backup_$(date +%Y%m%d_%H%M%S).sql
gzip backups/manual_backup_*.sql
unset PGPASSWORD

echo "Backup created in /home/repaircafe/backups/"
ls -lh backups/
```

---

### Restore from Backup

**If something goes wrong, restore from backup:**

```bash
# On SERVER
cd /home/repaircafe/backups

# List available backups
ls -lh

# Choose a backup file, unzip it
gunzip repair_cafe_20251206_020000.sql.gz

# Stop the application
sudo systemctl stop gunicorn

# Drop and recreate the database
sudo -u postgres psql
DROP DATABASE repair_cafe_db;
CREATE DATABASE repair_cafe_db;
GRANT ALL PRIVILEGES ON DATABASE repair_cafe_db TO repair_cafe_user;
\q

# Restore the backup
export PGPASSWORD='etBxrGnAP0e*NJUX69s*'
psql -h localhost -U repair_cafe_user -d repair_cafe_db < repair_cafe_20251206_020000.sql
unset PGPASSWORD

# Restart the application
sudo systemctl start gunicorn
```

**✅ Your data is now restored to the backup point!**

---

## DigitalOcean Backups

### DigitalOcean Droplet Backups (Optional, Costs Extra)

**What DigitalOcean Offers:**

1. **Droplet Snapshots (Manual)**
   - **Cost:** Free
   - **What:** Complete image of your entire server
   - **How:** DigitalOcean Control Panel → Droplets → Snapshots
   - **Use:** Before major system changes

2. **Automated Backups**
   - **Cost:** 20% of droplet cost (~$1.20/month for $6 droplet)
   - **What:** Weekly automatic backups
   - **Retention:** 4 backups kept
   - **Enable:** DigitalOcean Control Panel → Droplets → Enable Backups

3. **Volume Snapshots**
   - **Cost:** $0.05/GB/month
   - **What:** Backup of attached storage volumes
   - **Use:** If you add extra storage

**⚠️ Important:** DigitalOcean backups are **entire server images**, NOT just your database. They:
- Include all files, configurations, installed software
- Are slower to restore (recreates entire droplet)
- Are useful for disaster recovery
- Should be used IN ADDITION to database backups, not instead

---

## Recommended Backup Strategy

### 3-2-1 Backup Rule

**3 copies:**
1. Live database (on server)
2. Automated daily backups (on server in `/home/repaircafe/backups/`)
3. Weekly copy downloaded to your local machine

**2 different formats:**
1. SQL dumps (database backups)
2. DigitalOcean snapshots (entire server)

**1 offsite copy:**
- Download weekly backups to your local computer

---

### Weekly Offsite Backup (Recommended)

**From your LOCAL machine, download backups weekly:**

```bash
# Every week, download the backups
scp repaircafe@167.172.38.182:/home/repaircafe/backups/*.sql.gz ~/Desktop/repair_cafe_backups/

# Keep at least 4 weeks of backups locally
```

This protects against:
- Droplet deletion
- DigitalOcean account issues
- Catastrophic server failure

---

## Monitoring Your Backups

### Check Backup Status

```bash
# On SERVER
ls -lh /home/repaircafe/backups/

# Check backup log
tail -20 /home/repaircafe/backups/backup.log

# Verify latest backup is recent
stat /home/repaircafe/backups/*.sql.gz | grep Modify
```

### Test Restore (Monthly Recommended)

Once a month, test that you can restore a backup:

1. Create a test database
2. Restore a backup into it
3. Verify the data looks correct
4. Drop the test database

This ensures your backups actually work!

---

## Data Safety Checklist

Before ANY risky operation:

- [ ] Create manual backup
- [ ] Test that backup was created successfully
- [ ] Document what you're about to do
- [ ] Know how to restore if something goes wrong
- [ ] Have recent automated backup (check timestamp)
- [ ] Consider creating a DigitalOcean snapshot

---

## Summary: What to Run After Code Changes

### Simple Code Change (No Models)
```bash
git pull origin main
sudo systemctl restart gunicorn
```

### With Model Changes
```bash
/home/repaircafe/backup_database.sh  # Backup first!
git pull origin main
export $(cat .env | xargs)
poetry run python manage.py migrate
sudo systemctl restart gunicorn
```

### With Static Files
```bash
git pull origin main
export $(cat .env | xargs)
poetry run python manage.py collectstatic --no-input
sudo systemctl restart gunicorn
```

### With New Dependencies
```bash
git pull origin main
poetry install --only main --no-root
sudo systemctl restart gunicorn
```

---

## Quick Commands Reference

```bash
# Backup database manually
/home/repaircafe/backup_database.sh

# List backups
ls -lh /home/repaircafe/backups/

# Check backup log
tail -20 /home/repaircafe/backups/backup.log

# Deploy code changes
cd /var/www/repair_cafe && git pull origin main && sudo systemctl restart gunicorn

# View application logs
sudo journalctl -u gunicorn -f

# Check if services are running
sudo systemctl status gunicorn nginx postgresql

# Restart everything
sudo systemctl restart gunicorn nginx
```

---

## Getting Help

If something goes wrong:

1. **Don't panic** - Your backups are there
2. **Check logs** - `sudo journalctl -u gunicorn -n 100`
3. **Check status** - `sudo systemctl status gunicorn`
4. **Restore from backup** if needed (see above)
5. **Contact support** if you're stuck

---

## Your Current Backup Status

✅ **Script created:** `/home/repaircafe/backup_database.sh`
⏳ **Automated schedule:** Need to set up (see above)
⏳ **DigitalOcean backups:** Not enabled (optional, costs $1-2/month)
⏳ **Offsite backups:** Not set up (download weekly)

**Next steps:**
1. Set up cron job for daily backups
2. Download one backup to your local machine now
3. Consider enabling DigitalOcean automated backups

## Key Commands for Next Session

```bash
# Connect to server
ssh root@167.172.38.182

# After setup, connect as app user
ssh repaircafe@167.172.38.182

# Check service status
sudo systemctl status gunicorn nginx

# View logs
sudo journalctl -u gunicorn -f
sudo tail -f /var/log/nginx/repair_cafe_error.log

# Restart services
sudo systemctl restart gunicorn nginx
