# Repair Café - DigitalOcean Deployment Guide

This guide will walk you through deploying your Repair Café application to DigitalOcean step-by-step.

## Prerequisites

- DigitalOcean account with billing set up
- Basic familiarity with terminal/command line
- Your domain name (optional, but recommended)
- SSH key pair (we'll create one if you don't have it)

---

## Part 1: Prepare Your Local Machine

### Step 1.1: Generate SSH Key (if you don't have one)

On your local machine, open terminal and run:

```bash
# Check if you already have an SSH key
ls ~/.ssh/id_*.pub

# If no key exists, generate one
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter to accept default location
# Enter a passphrase (recommended) or press Enter twice for no passphrase

# Display your public key (you'll need this for DigitalOcean)
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output (starts with `ssh-ed25519` and ends with your email).

### Step 1.2: Prepare Environment Variables

Create a file locally to store your production secrets (DON'T commit this file):

```bash
cd /Users/YehorYeshchenko/Yehor/RepairCafee/repair_cafe
touch .env.production
```

Edit `.env.production` with these values (you'll fill them in later):

```bash
# Generate a new SECRET_KEY for production
SECRET_KEY=your-secret-key-here-change-this

# Database settings
DB_NAME=repair_cafe_db
DB_USER=repair_cafe_user
DB_PASSWORD=your-strong-database-password-here
DB_HOST=localhost
DB_PORT=5432

# Domain settings
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-droplet-ip

# Email settings (optional, for future notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

Generate a secure SECRET_KEY:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copy the output and use it as your SECRET_KEY.

---

## Part 2: Create DigitalOcean Droplet

### Step 2.1: Create a Droplet

1. Log in to [DigitalOcean](https://cloud.digitalocean.com)
2. Click **"Create"** button (top right)
3. Select **"Droplets"**

### Step 2.2: Configure Droplet Settings

**Choose an image:**
- Select **Ubuntu 22.04 (LTS) x64**

**Choose Size:**
- **Basic Plan** (for small to medium usage)
- **Regular** CPU option
- **$6/month** ($0.009/hour) - 1GB RAM, 25GB SSD (recommended minimum)
- OR **$12/month** - 2GB RAM, 50GB SSD (better for production)

**Choose a datacenter region:**
- Select the region closest to your users (e.g., Frankfurt, Amsterdam, New York)

**Authentication:**
- Select **"SSH Key"** (more secure)
- Click **"New SSH Key"**
- Paste your public key from Step 1.1
- Name it something recognizable like "my-laptop"
- Click **"Add SSH Key"**

**Choose a hostname:**
- Name it something meaningful like `repair-cafe-prod`

**Advanced Options (click "Advanced Options"):**
- ✅ Enable **Monitoring** (free, useful for tracking resources)

### Step 2.3: Create and Wait

1. Click **"Create Droplet"**
2. Wait 1-2 minutes for droplet to be created
3. Note down the **IP address** shown (e.g., `157.245.x.x`)

---

## Part 3: Initial Server Setup

### Step 3.1: Connect to Your Droplet

From your local terminal:

```bash
ssh root@YOUR_DROPLET_IP
```

Replace `YOUR_DROPLET_IP` with your actual IP address.

Type `yes` when asked about authenticity, then you should be logged in.

### Step 3.2: Update System

```bash
# Update package list
apt update

# Upgrade all packages
apt upgrade -y
```

### Step 3.3: Create Application User

Don't run the application as root. Create a dedicated user:

```bash
# Create user named 'repairacafe'
adduser repairacafe

# When prompted:
# - Enter a password (save it somewhere safe)
# - Full Name: Repair Cafe App
# - Press Enter for other fields

# Add user to sudo group
usermod -aG sudo repairacafe

# Switch to the new user
su - repairacafe
```

You're now logged in as `repairacafe` user.

---

## Part 4: Install Required Software

### Step 4.1: Install Python 3.11

```bash
# Add deadsnakes PPA for newer Python versions
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.11 and required packages
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# Verify installation
python3.11 --version
```

### Step 4.2: Install PostgreSQL

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib libpq-dev -y

# Verify it's running
sudo systemctl status postgresql
```

Press `q` to exit the status view.

### Step 4.3: Install Nginx

```bash
# Install Nginx web server
sudo apt install nginx -y

# Verify it's running
sudo systemctl status nginx
```

Press `q` to exit.

### Step 4.4: Install Git

```bash
sudo apt install git -y
```

### Step 4.5: Install Poetry

```bash
# Install Poetry (Python dependency manager)
curl -sSL https://install.python-poetry.org | python3.11 -

# Add Poetry to PATH
echo 'export PATH="/home/repairacafe/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
poetry --version
```

---

## Part 5: Configure PostgreSQL Database

### Step 5.1: Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql
```

You're now in PostgreSQL prompt. Run these commands:

```sql
-- Create database
CREATE DATABASE repair_cafe_db;

-- Create user with password (use a strong password!)
CREATE USER repair_cafe_user WITH PASSWORD 'your-strong-password-here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE repair_cafe_db TO repair_cafe_user;

-- Grant schema privileges (PostgreSQL 15+)
\c repair_cafe_db
GRANT ALL ON SCHEMA public TO repair_cafe_user;

-- Exit PostgreSQL
\q
```

Replace `your-strong-password-here` with the password you set in your `.env.production` file.

### Step 5.2: Test Database Connection

```bash
# Test connection
psql -h localhost -U repair_cafe_user -d repair_cafe_db

# Enter password when prompted
# If successful, you'll see the psql prompt

# Exit
\q
```

---

## Part 6: Deploy Application Code

### Step 6.1: Set Up Application Directory

```bash
# Create directory for the application
mkdir -p ~/apps
cd ~/apps

# Clone your repository (replace with your actual repo URL)
# If you're using GitHub:
git clone https://github.com/yourusername/repair_cafe.git

# OR if you haven't pushed to GitHub yet, we'll upload manually (see Step 6.2)
```

### Step 6.2: Option A - Manual Upload (if not using Git)

From your **local machine** terminal (open a new terminal window):

```bash
# Navigate to your project directory
cd /Users/YehorYeshchenko/Yehor/RepairCafee/repair_cafe

# Create a tarball (exclude unnecessary files)
tar -czf repair_cafe.tar.gz \
  --exclude='.git' \
  --exclude='db.sqlite3' \
  --exclude='__pycache__' \
  --exclude='.venv' \
  --exclude='*.pyc' \
  --exclude='.env*' \
  .

# Upload to droplet
scp repair_cafe.tar.gz repairacafe@YOUR_DROPLET_IP:~/apps/

# Clean up
rm repair_cafe.tar.gz
```

Back on the **droplet**:

```bash
cd ~/apps
tar -xzf repair_cafe.tar.gz
mv repair_cafe repair_cafe_temp
mkdir repair_cafe
mv repair_cafe_temp/* repair_cafe/
rm -rf repair_cafe_temp repair_cafe.tar.gz
cd repair_cafe
```

### Step 6.3: Create Production Environment File

```bash
cd ~/apps/repair_cafe

# Create .env file for production
nano .env
```

Paste this content (update with your actual values):

```bash
SECRET_KEY=your-generated-secret-key-from-step-1-2
DEBUG=False
ALLOWED_HOSTS=your-droplet-ip,your-domain.com

# Database
DB_NAME=repair_cafe_db
DB_USER=repair_cafe_user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432

# Optional: Email settings
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

### Step 6.4: Update Django Settings

```bash
nano config/settings.py
```

Add these imports at the top (after existing imports):

```python
import os
from pathlib import Path
```

Replace the SECRET_KEY, DEBUG, and ALLOWED_HOSTS sections with:

```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production-123456789')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else []
```

Replace the DATABASES section with:

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'repair_cafe_db'),
        'USER': os.environ.get('DB_USER', 'repair_cafe_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

Add these at the bottom of the file:

```python
# Static files configuration
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

---

## Part 7: Install Dependencies and Set Up Application

### Step 7.1: Install Python Dependencies

```bash
cd ~/apps/repair_cafe

# Configure Poetry to create virtual environment in project
poetry config virtualenvs.in-project true

# Install dependencies
poetry install --no-dev
```

### Step 7.2: Install Additional Required Package

```bash
# Install PostgreSQL adapter
poetry add psycopg2-binary
```

### Step 7.3: Load Environment Variables

```bash
# Export environment variables from .env file
export $(cat .env | xargs)
```

### Step 7.4: Run Database Migrations

```bash
# Run migrations
poetry run python manage.py migrate
```

### Step 7.5: Collect Static Files

```bash
# Collect all static files
poetry run python manage.py collectstatic --noinput
```

### Step 7.6: Create Superuser

```bash
# Create first admin user
poetry run python manage.py createsuperuser

# Enter username, email, and password when prompted
```

### Step 7.7: Test Application

```bash
# Test that the application runs
poetry run python manage.py runserver 0.0.0.0:8000
```

From your local browser, visit: `http://YOUR_DROPLET_IP:8000`

If you see the login page, it works! Press `Ctrl+C` to stop the server.

---

## Part 8: Set Up Gunicorn (Application Server)

### Step 8.1: Install Gunicorn

```bash
cd ~/apps/repair_cafe
poetry add gunicorn
```

### Step 8.2: Test Gunicorn

```bash
poetry run gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```

Visit `http://YOUR_DROPLET_IP:8000` - you should see your app (without CSS yet).

Press `Ctrl+C` to stop.

### Step 8.3: Create Gunicorn Systemd Service

```bash
sudo nano /etc/systemd/system/repair-cafe.service
```

Paste this content:

```ini
[Unit]
Description=Repair Cafe Gunicorn daemon
After=network.target

[Service]
User=repairacafe
Group=www-data
WorkingDirectory=/home/repairacafe/apps/repair_cafe
EnvironmentFile=/home/repairacafe/apps/repair_cafe/.env

ExecStart=/home/repairacafe/apps/repair_cafe/.venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/repairacafe/apps/repair_cafe/repair_cafe.sock \
    --access-logfile /home/repairacafe/apps/repair_cafe/logs/gunicorn-access.log \
    --error-logfile /home/repairacafe/apps/repair_cafe/logs/gunicorn-error.log \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

### Step 8.4: Create Logs Directory

```bash
mkdir -p ~/apps/repair_cafe/logs
```

### Step 8.5: Start and Enable Service

```bash
# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Start the service
sudo systemctl start repair-cafe

# Check status
sudo systemctl status repair-cafe

# Enable service to start on boot
sudo systemctl enable repair-cafe
```

If you see "active (running)" in green, it's working!

---

## Part 9: Configure Nginx (Web Server)

### Step 9.1: Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/repair-cafe
```

Paste this content (replace `YOUR_DROPLET_IP` with your actual IP):

```nginx
server {
    listen 80;
    server_name YOUR_DROPLET_IP your-domain.com www.your-domain.com;

    client_max_body_size 10M;

    location = /favicon.ico {
        alias /home/repairacafe/apps/repair_cafe/devices/static/logo.png;
        access_log off;
        log_not_found off;
    }

    location /static/ {
        alias /home/repairacafe/apps/repair_cafe/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/repairacafe/apps/repair_cafe/repair_cafe.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

### Step 9.2: Enable the Site

```bash
# Create symbolic link to enable site
sudo ln -s /etc/nginx/sites-available/repair-cafe /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t
```

You should see "syntax is ok" and "test is successful".

### Step 9.3: Restart Nginx

```bash
sudo systemctl restart nginx
```

### Step 9.4: Configure Firewall

```bash
# Allow Nginx through firewall
sudo ufw allow 'Nginx Full'

# Allow SSH (IMPORTANT! Don't lock yourself out)
sudo ufw allow OpenSSH

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

## Part 10: Test Your Deployment

### Step 10.1: Visit Your Application

Open your browser and go to: `http://YOUR_DROPLET_IP`

You should see your Repair Café login page with proper styling!

### Step 10.2: Log In

Use the superuser credentials you created in Step 7.6.

### Step 10.3: Verify Features

- Navigate through the interface
- Create a test device intake
- Check that all pages load correctly

---

## Part 11: Set Up SSL/HTTPS (Recommended)

### Step 11.1: Set Up Domain (if you have one)

If you have a domain name:

1. Go to your domain registrar (Namecheap, GoDaddy, etc.)
2. Create an **A record** pointing to your droplet IP:
   - Type: `A`
   - Name: `@` (or your subdomain)
   - Value: `YOUR_DROPLET_IP`
   - TTL: Automatic or 3600
3. Wait 5-60 minutes for DNS propagation

### Step 11.2: Install Certbot (for free SSL)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y
```

### Step 11.3: Obtain SSL Certificate

```bash
# Get certificate (replace with your actual domain)
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Follow prompts:
# - Enter your email
# - Agree to terms
# - Decide on email sharing (optional)
# - Choose redirect option: Select 2 (redirect HTTP to HTTPS)
```

### Step 11.4: Test Auto-Renewal

```bash
# Test renewal
sudo certbot renew --dry-run
```

If successful, your certificates will auto-renew.

---

## Part 12: Post-Deployment Tasks

### Step 12.1: Set Up Automated Backups

Create a backup script:

```bash
nano ~/backup_database.sh
```

Paste:

```bash
#!/bin/bash
BACKUP_DIR="/home/repairacafe/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -h localhost -U repair_cafe_user repair_cafe_db > "$BACKUP_DIR/repair_cafe_$DATE.sql"

# Keep only last 7 days of backups
find $BACKUP_DIR -name "repair_cafe_*.sql" -mtime +7 -delete

echo "Backup completed: repair_cafe_$DATE.sql"
```

Make it executable:

```bash
chmod +x ~/backup_database.sh
```

Set up daily backups with cron:

```bash
crontab -e
```

Select nano (usually option 1), then add:

```bash
# Daily database backup at 2 AM
0 2 * * * /home/repairacafe/backup_database.sh
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

### Step 12.2: Monitor Logs

View application logs:

```bash
# Gunicorn error log
tail -f ~/apps/repair_cafe/logs/gunicorn-error.log

# Gunicorn access log
tail -f ~/apps/repair_cafe/logs/gunicorn-access.log

# Nginx error log
sudo tail -f /var/log/nginx/error.log

# System service log
sudo journalctl -u repair-cafe -f
```

Press `Ctrl+C` to exit.

---

## Part 13: Updating Your Application

When you need to update your code:

### Step 13.1: Update Code

```bash
# Connect to droplet
ssh repairacafe@YOUR_DROPLET_IP

# Navigate to project
cd ~/apps/repair_cafe

# If using Git:
git pull origin main

# If uploading manually, upload new files as in Step 6.2
```

### Step 13.2: Update Dependencies (if needed)

```bash
poetry install --no-dev
```

### Step 13.3: Run Migrations (if models changed)

```bash
export $(cat .env | xargs)
poetry run python manage.py migrate
```

### Step 13.4: Collect Static Files (if CSS/JS changed)

```bash
poetry run python manage.py collectstatic --noinput
```

### Step 13.5: Restart Application

```bash
sudo systemctl restart repair-cafe
```

### Step 13.6: Verify

Visit your site and test the changes.

---

## Troubleshooting

### Application Won't Start

```bash
# Check service status
sudo systemctl status repair-cafe

# View recent logs
sudo journalctl -u repair-cafe -n 50

# Check Gunicorn logs
tail -n 50 ~/apps/repair_cafe/logs/gunicorn-error.log
```

### 502 Bad Gateway Error

```bash
# Check if Gunicorn is running
sudo systemctl status repair-cafe

# Check socket file exists
ls -la ~/apps/repair_cafe/repair_cafe.sock

# Restart service
sudo systemctl restart repair-cafe

# Restart Nginx
sudo systemctl restart nginx
```

### Static Files Not Loading

```bash
# Re-collect static files
cd ~/apps/repair_cafe
export $(cat .env | xargs)
poetry run python manage.py collectstatic --noinput

# Check permissions
sudo chown -R repairacafe:www-data ~/apps/repair_cafe/staticfiles
sudo chmod -R 755 ~/apps/repair_cafe/staticfiles

# Restart Nginx
sudo systemctl restart nginx
```

### Database Connection Error

```bash
# Test database connection
psql -h localhost -U repair_cafe_user -d repair_cafe_db

# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify .env file has correct credentials
cat ~/apps/repair_cafe/.env
```

### Can't Access via IP Address

```bash
# Check firewall
sudo ufw status

# Make sure Nginx is running
sudo systemctl status nginx

# Check if port 80 is open
sudo netstat -tulpn | grep :80
```

---

## Cost Estimate

**Monthly Costs:**
- Droplet (1GB RAM): $6/month
- OR Droplet (2GB RAM): $12/month
- Backups (optional): $1.20-$2.40/month (20% of droplet cost)
- **Total: $6-15/month**

**One-time:**
- Domain name (optional): $10-15/year

---

## Security Best Practices

1. **Change default SSH port** (optional but recommended)
2. **Set up fail2ban** to prevent brute force attacks
3. **Keep system updated**: `sudo apt update && sudo apt upgrade` weekly
4. **Monitor logs** regularly for suspicious activity
5. **Use strong passwords** for all accounts
6. **Keep backups** of your database
7. **Don't share .env file** - it contains secrets

---

## Need Help?

- **DigitalOcean Community:** https://www.digitalocean.com/community
- **Django Documentation:** https://docs.djangoproject.com/
- **Nginx Documentation:** https://nginx.org/en/docs/

---

## Quick Command Reference

```bash
# Restart application after code changes
sudo systemctl restart repair-cafe

# View application logs
sudo journalctl -u repair-cafe -f

# Restart Nginx
sudo systemctl restart nginx

# Manual database backup
~/backup_database.sh

# Connect to database
psql -h localhost -U repair_cafe_user -d repair_cafe_db

# Run Django management commands
cd ~/apps/repair_cafe
export $(cat .env | xargs)
poetry run python manage.py <command>
```

---

## Congratulations!

Your Repair Café application is now deployed and running on DigitalOcean!

You can now:
- Access it via your droplet IP or domain name
- Log in with your admin credentials
- Create operator accounts for your team
- Start managing device repairs
