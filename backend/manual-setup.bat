@echo off
REM Manual Setup Script for Windows

echo ==================================
echo Device Monitoring System - Manual Setup
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.9 or higher from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% is installed
echo.

REM Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from example...
    copy .env.example .env
    echo Created .env file
    echo Please edit .env file and set your SECRET_KEY and JWT_SECRET_KEY
)

REM Create necessary directories
if not exist instance mkdir instance
if not exist logs mkdir logs

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo To start the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run the application: python start.py
echo.
echo Or use the START.bat script
echo.
echo Default Credentials:
echo   Admin:    admin / Admin@123
echo   Operator: operator / Operator@123
echo   Viewer:   viewer / Viewer@123
echo.
pause
