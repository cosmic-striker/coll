@echo off
REM Docker Setup Script for Windows

echo ==================================
echo Device Monitoring System - Docker Setup
echo ==================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed
    echo Please install Docker Desktop from: https://www.docker.com/get-started
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker Compose is not installed
    echo Please install Docker Desktop which includes Docker Compose
    pause
    exit /b 1
)

echo Docker is installed
echo Docker Compose is installed
echo.

REM Check if .env file exists
if not exist .env (
    echo No .env file found. Creating from example...
    copy .env.example .env
    echo Created .env file
    echo Please edit .env file and set your SECRET_KEY and JWT_SECRET_KEY
    echo.
    pause
)

REM Create necessary directories
if not exist instance mkdir instance
if not exist logs mkdir logs

echo Building Docker images...
docker-compose build

echo.
echo Starting services...
docker-compose up -d

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo Services Status:
docker-compose ps
echo.
echo Access the application at: http://localhost:5000
echo.
echo Default Credentials:
echo   Admin:    admin / Admin@123
echo   Operator: operator / Operator@123
echo   Viewer:   viewer / Viewer@123
echo.
echo Useful Commands:
echo   View logs:        docker-compose logs -f
echo   Stop services:    docker-compose stop
echo   Restart services: docker-compose restart
echo   Remove services:  docker-compose down
echo.
pause
