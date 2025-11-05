@echo off
REM Device Monitoring System - Test Script
REM This script tests all API endpoints

echo ========================================
echo Device Monitoring System - Testing
echo ========================================
echo.
echo Make sure the server is running before testing!
echo.

python test_endpoints.py

pause
