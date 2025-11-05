#!/bin/bash
# Docker Setup Script for Linux/Mac

set -e

echo "=================================="
echo "Device Monitoring System - Docker Setup"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker from: https://www.docker.com/get-started"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker is installed"
echo "✓ Docker Compose is installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo "⚠️  Please edit .env file and set your SECRET_KEY and JWT_SECRET_KEY"
    echo ""
    read -p "Press Enter to continue..."
fi

# Create necessary directories
mkdir -p instance logs

echo "Building Docker images..."
docker-compose build

echo ""
echo "Starting services..."
docker-compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Services Status:"
docker-compose ps
echo ""
echo "Access the application at: http://localhost:5000"
echo ""
echo "Default Credentials:"
echo "  Admin:    admin / Admin@123"
echo "  Operator: operator / Operator@123"
echo "  Viewer:   viewer / Viewer@123"
echo ""
echo "Useful Commands:"
echo "  View logs:        docker-compose logs -f"
echo "  Stop services:    docker-compose stop"
echo "  Restart services: docker-compose restart"
echo "  Remove services:  docker-compose down"
echo ""
