#!/bin/bash

echo "========================================"
echo "Repair Café Setup Script"
echo "========================================"

# Install pyenv if not already installed
if ! command -v pyenv &> /dev/null; then
    echo "Installing pyenv..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "Homebrew not found. Please install Homebrew first: https://brew.sh"
            exit 1
        fi
        brew update
        brew install pyenv
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl https://pyenv.run | bash
    else
        echo "Unsupported OS. Please install pyenv manually: https://github.com/pyenv/pyenv#installation"
        exit 1
    fi

    # Add pyenv to shell
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

    echo "pyenv installed. You may need to restart your shell or run:"
    echo "  export PYENV_ROOT=\"\$HOME/.pyenv\""
    echo "  export PATH=\"\$PYENV_ROOT/bin:\$PATH\""
    echo "  eval \"\$(pyenv init -)\""
else
    echo "pyenv is already installed."
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
fi

# Install Poetry if not already installed
if ! command -v poetry &> /dev/null; then
    echo "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -

    # Add Poetry to PATH
    export PATH="$HOME/.local/bin:$PATH"

    echo "Poetry installed."
else
    echo "Poetry is already installed."
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install dependencies with Poetry
echo "Installing dependencies with Poetry..."
poetry install --sync

# Activate Poetry virtual environment
echo "Activating Poetry virtual environment..."
source "$(poetry env info --path)/bin/activate"

# Create migrations
echo "Creating database migrations..."
poetry run python manage.py makemigrations

# Run migrations
echo "Running database migrations..."
poetry run python manage.py migrate

# Success message
echo ""
echo "========================================"
echo "✓ Setup Complete!"
echo "========================================"
echo ""
echo "Starting development server..."
echo ""
echo "Access your application at:"
echo "  - Main site: http://127.0.0.1:8000/"
echo "  - Admin interface: http://127.0.0.1:8000/admin/"
echo ""
echo "Note: Create an admin user first with:"
echo "  poetry run python manage.py createsuperuser"
echo ""
echo "========================================"
echo ""

# Start the development server
poetry run python manage.py runserver
