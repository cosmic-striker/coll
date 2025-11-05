#!/bin/bash
# Manual Setup Script for Linux/Mac

set -e

echo "=================================="
echo "Device Monitoring System - Manual Setup"
echo "=================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.9 or higher from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION is installed"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo "⚠️  Please edit .env file and set your SECRET_KEY and JWT_SECRET_KEY"
fi

# Create necessary directories
mkdir -p instance logs

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the application: python start.py"
echo ""
echo "Or use the start script:"
echo "  ./start.sh"
echo ""
echo "Default Credentials:"
echo "  Admin:    admin / Admin@123"
echo "  Operator: operator / Operator@123"
echo "  Viewer:   viewer / Viewer@123"
echo ""
