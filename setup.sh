#!/bin/bash

echo "========================================"
echo "Repair Café Setup Script"
echo "========================================"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Install dependencies using venv's pip directly
echo "Installing dependencies..."
./venv/bin/pip install -r requirements.txt

# Create migrations
echo "Creating database migrations..."
./venv/bin/python manage.py makemigrations

# Run migrations
echo "Running database migrations..."
./venv/bin/python manage.py migrate

# Success message
echo ""
echo "========================================"
echo "✓ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Create an admin user:"
echo "   ./venv/bin/python manage.py createsuperuser"
echo ""
echo "2. Start the development server:"
echo "   ./venv/bin/python manage.py runserver"
echo ""
echo "3. Open your browser and go to:"
echo "   http://127.0.0.1:8000/"
echo ""
echo "4. Access admin interface at:"
echo "   http://127.0.0.1:8000/admin/"
echo ""
echo "========================================"
