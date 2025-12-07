# Repair Café - Deployment Checklist for 167.172.38.182

## Production Secrets (Keep Secure!)

```bash
SECRET_KEY: OAej7_4DqbqjNIVtfVrMVzTVmk_l4Hz1qbLcKBflAiO2m72l_i9X4OGLRn6ZSlrHoig
DB_PASSWORD: etBxrGnAP0e*NJUX69s*
DROPLET_IP: 167.172.38.182
```

---

## Phase 1: Local Code Preparation ✅ COMPLETED

- [x] Updated config/settings.py with environment variables
- [x] Updated pyproject.toml with production dependencies
- [x] Created .env.production.template
- [x] Updated poetry.lock
- [x] Generated production secrets

---

## Phase 2: Server Setup

### Step 2.1: Connect and Create User
```bash
# Connect as root
ssh root@167.172.38.182

# Update system
apt update && apt upgrade -y

# Create application user
adduser --disabled-password --gecos "" repaircafe
usermod -aG sudo repaircafe

# Set password for repaircafe user (if no SSH keys)
passwd repaircafe

# Exit and reconnect
exit
ssh repaircafe@167.172.38.182
```

**Note:** If you have SSH keys, you can set them up. Otherwise, use password authentication.

**Checklist:**
- [x] Connected to server as root
- [x] System updated
- [x] User 'repaircafe' created
- [x] Password set for repaircafe user
- [x] Successfully logged in as repaircafe

---

### Step 2.2: Install System Packages
```bash
# Python and build tools
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
sudo apt install -y build-essential libpq-dev curl git

# PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Nginx
sudo apt install -y nginx

# Verify installations
python3.11 --version
psql --version
nginx -v
```

**Checklist:**
- [ ] Python 3.11 installed
- [ ] Build tools installed
- [ ] PostgreSQL installed and running
- [ ] Nginx installed

---

### Step 2.3: Install Poetry
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Configure Poetry
poetry config virtualenvs.in-project true

# Verify
poetry --version
```

**Checklist:**
- [ ] Poetry installed
- [ ] Poetry added to PATH
- [ ] Poetry configured for local venv

---

### Step 2.4: Configure PostgreSQL
```bash
# Switch to postgres user
sudo -u postgres psql
```

**In PostgreSQL prompt, run:**
```sql
CREATE DATABASE repair_cafe_db;
CREATE USER repair_cafe_user WITH PASSWORD 'etBxrGnAP0e*NJUX69s*';
ALTER ROLE repair_cafe_user SET client_encoding TO 'utf8';
ALTER ROLE repair_cafe_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE repair_cafe_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE repair_cafe_db TO repair_cafe_user;
\q
```

**Test connection:**
```bash
psql -U repair_cafe_user -h localhost -d repair_cafe_db
# Enter password: etBxrGnAP0e*NJUX69s*
\q
```

**Checklist:**
- [ ] Database 'repair_cafe_db' created
- [ ] User 'repair_cafe_user' created with password
- [ ] Privileges granted
- [ ] Connection tested successfully

---

### Step 2.5: Create Project Directory
```bash
sudo mkdir -p /var/www/repair_cafe
sudo chown repaircafe:repaircafe /var/www/repair_cafe
cd /var/www/repair_cafe
```

**Checklist:**
- [ ] Directory /var/www/repair_cafe created
- [ ] Ownership set to repaircafe

---

## Phase 3: Deploy Application

### Step 3.1: Clone Code from GitHub

**On SERVER:**
```bash
cd /var/www/repair_cafe

# Clone repository
git clone https://github.com/yegoryeshchenko/repair_cafe.git .

# Verify files
ls -la

# Check current branch
git branch
```

**Note:** The `.` at the end clones directly into the current directory instead of creating a subdirectory.

**Checklist:**
- [ ] Repository cloned successfully
- [ ] Files visible in /var/www/repair_cafe
- [ ] On main branch

---

### Step 3.2: Install Dependencies
```bash
cd /var/www/repair_cafe

# Install dependencies
poetry install --only main --no-root

# Verify
poetry run python --version
poetry run python -c "import django; print(django.get_version())"
```

**Checklist:**
- [ ] Poetry dependencies installed
- [ ] Virtual environment created at .venv
- [ ] Django imports successfully

---

### Step 3.3: Create Production .env File
```bash
cd /var/www/repair_cafe
nano .env
```

**Paste this content:**
```bash
SECRET_KEY=OAej7_4DqbqjNIVtfVrMVzTVmk_l4Hz1qbLcKBflAiO2m72l_i9X4OGLRn6ZSlrHoig
DEBUG=False
ALLOWED_HOSTS=167.172.38.182

DB_ENGINE=django.db.backends.postgresql
DB_NAME=repair_cafe_db
DB_USER=repair_cafe_user
DB_PASSWORD=etBxrGnAP0e*NJUX69s*
DB_HOST=localhost
DB_PORT=5432

# Security Settings (False for HTTP, True for HTTPS)
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

**Save:** Ctrl+X, then Y, then Enter

**Secure it:**
```bash
chmod 600 .env
cat .env  # Verify contents
```

**Checklist:**
- [ ] .env file created
- [ ] All values correct
- [ ] File permissions set to 600

---

### Step 3.4: Run Migrations and Setup
```bash
cd /var/www/repair_cafe

# Load environment variables
export $(cat .env | xargs)

# Run migrations
poetry run python manage.py migrate

# Collect static files
poetry run python manage.py collectstatic --no-input

# Verify static files
ls -la staticfiles/

# Create superuser
poetry run python manage.py createsuperuser
# Username: admin
# Email: admin@repaircafe.local
# Password: (choose a strong password and save it!)
```

**Checklist:**
- [ ] Migrations completed successfully
- [ ] Static files collected to staticfiles/
- [ ] Superuser created (save credentials!)

---

## Phase 4: Configure Gunicorn

### Step 4.1: Create Systemd Service
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

**Paste:**
```ini
[Unit]
Description=Gunicorn daemon for Repair Cafe
After=network.target

[Service]
Type=notify
User=repaircafe
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/var/www/repair_cafe
EnvironmentFile=/var/www/repair_cafe/.env
ExecStart=/var/www/repair_cafe/.venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/run/gunicorn/repair_cafe.sock \
          --timeout 60 \
          --access-logfile /var/log/gunicorn/access.log \
          --error-logfile /var/log/gunicorn/error.log \
          config.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**Save:** Ctrl+X, then Y, then Enter

---

### Step 4.2: Start Gunicorn
```bash
# Create log directory
sudo mkdir -p /var/log/gunicorn
sudo chown repaircafe:www-data /var/log/gunicorn

# Reload systemd
sudo systemctl daemon-reload

# Enable Gunicorn to start on boot
sudo systemctl enable gunicorn

# Start Gunicorn
sudo systemctl start gunicorn

# Check status (should show "active (running)")
sudo systemctl status gunicorn

# If errors, check logs:
sudo journalctl -u gunicorn -n 50
```

**Checklist:**
- [ ] Service file created
- [ ] Log directory created
- [ ] Gunicorn service enabled
- [ ] Gunicorn service started
- [ ] Status shows "active (running)" in green

---

## Phase 5: Configure Nginx

### Step 5.1: Create Nginx Config
```bash
sudo nano /etc/nginx/sites-available/repair_cafe
```

**Paste:**
```nginx
upstream repair_cafe_app {
    server unix:/run/gunicorn/repair_cafe.sock fail_timeout=0;
}

server {
    listen 80;
    server_name 167.172.38.182;
    client_max_body_size 10M;

    access_log /var/log/nginx/repair_cafe_access.log;
    error_log /var/log/nginx/repair_cafe_error.log;

    location /static/ {
        alias /var/www/repair_cafe/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_buffering off;
        proxy_pass http://repair_cafe_app;
    }

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

**Save:** Ctrl+X, then Y, then Enter

---

### Step 5.2: Enable Site
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/repair_cafe /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Should show:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# Restart Nginx
sudo systemctl restart nginx

# Enable on boot
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

**Checklist:**
- [ ] Nginx config created
- [ ] Symbolic link created
- [ ] Default site removed
- [ ] Nginx test passed
- [ ] Nginx restarted
- [ ] Status shows "active (running)"

---

### Step 5.3: Configure Firewall
```bash
# Allow SSH (CRITICAL - do this first!)
sudo ufw allow OpenSSH

# Allow HTTP
sudo ufw allow 'Nginx HTTP'

# Enable firewall
sudo ufw enable
# Type 'y' to confirm

# Check status
sudo ufw status verbose
```

**Expected output:**
```
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
Nginx HTTP                 ALLOW       Anywhere
OpenSSH (v6)               ALLOW       Anywhere (v6)
Nginx HTTP (v6)            ALLOW       Anywhere (v6)
```

**Checklist:**
- [ ] OpenSSH allowed
- [ ] Nginx HTTP allowed
- [ ] Firewall enabled
- [ ] Status shows correct rules

---

## Phase 6: Testing

### Step 6.1: Verify Services
```bash
# Check both services
sudo systemctl status gunicorn
sudo systemctl status nginx

# Test with curl
curl http://167.172.38.182/

# Should see HTML output (login page)
```

**Checklist:**
- [ ] Gunicorn running
- [ ] Nginx running
- [ ] Curl returns HTML

---

### Step 6.2: Browser Testing

**Open in your browser:**

1. **Homepage:** http://167.172.38.182/
   - Should see login page with styling

2. **Admin Panel:** http://167.172.38.182/admin/
   - Login with superuser credentials
   - Verify admin interface loads

3. **Test Application:**
   - Login to main app
   - Navigate to dashboard
   - Create a test device
   - Verify it saves correctly

**Checklist:**
- [ ] Login page loads with CSS
- [ ] Can login successfully
- [ ] Dashboard displays correctly
- [ ] Can create test device
- [ ] Static files (CSS, logo) load

---

### Step 6.3: Troubleshooting Commands

If something doesn't work:

```bash
# Check Gunicorn logs
sudo journalctl -u gunicorn -n 50
sudo tail -f /var/log/gunicorn/error.log

# Check Nginx logs
sudo tail -f /var/log/nginx/repair_cafe_error.log

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Check socket exists
ls -la /run/gunicorn/repair_cafe.sock

# Test database connection
cd /var/www/repair_cafe
export $(cat .env | xargs)
poetry run python manage.py shell
>>> from django.db import connection
>>> connection.ensure_connection()
>>> exit()
```

---

## Phase 7: Maintenance Setup

### Step 7.1: Database Backups
```bash
# Create backup script
nano /home/repaircafe/backup_database.sh
```

**Paste:**
```bash
#!/bin/bash
BACKUP_DIR="/home/repaircafe/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump -U repair_cafe_user -h localhost repair_cafe_db > "$BACKUP_DIR/repair_cafe_$DATE.sql"
gzip "$BACKUP_DIR/repair_cafe_$DATE.sql"
find $BACKUP_DIR -name "repair_cafe_*.sql.gz" -mtime +7 -delete
echo "Backup completed: repair_cafe_$DATE.sql.gz"
```

**Make executable:**
```bash
chmod +x /home/repaircafe/backup_database.sh

# Test it
./backup_database.sh
```

**Schedule daily backups:**
```bash
crontab -e
# Choose nano (option 1)
# Add this line:
0 2 * * * /home/repaircafe/backup_database.sh
```

**Checklist:**
- [ ] Backup script created
- [ ] Script tested successfully
- [ ] Cron job scheduled

---

## Phase 8: Future Updates

### When You Need to Update Code

**From LOCAL machine:**
```bash
cd /Users/YehorYeshchenko/Yehor/RepairCafee/repair_cafe
tar -czf repair_cafe.tar.gz --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='venv' --exclude='.venv' --exclude='db.sqlite3' --exclude='staticfiles' --exclude='.env*' .
scp repair_cafe.tar.gz repaircafe@167.172.38.182:/var/www/repair_cafe/
```

**On SERVER:**
```bash
cd /var/www/repair_cafe
tar -xzf repair_cafe.tar.gz
rm repair_cafe.tar.gz
export $(cat .env | xargs)
poetry install --only main
poetry run python manage.py migrate
poetry run python manage.py collectstatic --no-input
sudo systemctl restart gunicorn
```

---

## Quick Reference Commands

```bash
# View application logs
sudo journalctl -u gunicorn -f

# Restart application
sudo systemctl restart gunicorn

# Restart web server
sudo systemctl restart nginx

# Check service status
sudo systemctl status gunicorn nginx

# Manual database backup
/home/repaircafe/backup_database.sh

# Access database
psql -U repair_cafe_user -h localhost -d repair_cafe_db
```

---

## Success Criteria

✅ Your deployment is successful when:

- [ ] Application accessible at http://167.172.38.182
- [ ] Login page loads with proper styling (CSS)
- [ ] Admin can login and access dashboard
- [ ] Device creation works
- [ ] Static files (CSS, images) load correctly
- [ ] Services restart on server reboot
- [ ] Database backups configured and working

---

## Support

If you encounter issues:

1. Check the troubleshooting commands above
2. Review the logs
3. Verify all checklist items are complete
4. Ensure all credentials are correct in .env file

**Important Files:**
- Application: `/var/www/repair_cafe/`
- Environment: `/var/www/repair_cafe/.env`
- Gunicorn Service: `/etc/systemd/system/gunicorn.service`
- Nginx Config: `/etc/nginx/sites-available/repair_cafe`
- Logs: `/var/log/gunicorn/` and `/var/log/nginx/`
