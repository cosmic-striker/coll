#!/usr/bin/env python3
"""
Local Testing Script for Backend Application

This script helps test the Flask backend locally without Docker.
It will:
1. Check Python environment
2. Install dependencies (if needed)
3. Set up local database
4. Start the Flask application
5. Provide testing instructions
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("   Please use Python 3.8 or higher")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask', 'flask_jwt_extended', 'flask_sqlalchemy', 
        'flask_migrate', 'werkzeug', 'cryptography'
    ]
    
    missing = []
    installed = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            installed.append(package)
        except ImportError:
            missing.append(package)
    
    print(f"✅ Installed packages: {len(installed)}")
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        return False
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Set up environment variables for local testing"""
    env_vars = {
        'FLASK_ENV': 'development',
        'FLASK_DEBUG': 'true',
        'SECRET_KEY': 'local-dev-secret-key-change-in-production',
        'JWT_SECRET_KEY': 'local-dev-jwt-secret-key',
        'DATABASE_URL': 'sqlite:///local_devices.db',
        'CELERY_BROKER_URL': 'redis://localhost:6379/0',
        'CELERY_RESULT_BACKEND': 'redis://localhost:6379/0',
        'ALERT_EMAIL_FROM': 'test@localhost.local',
        'ALERT_EMAIL_TO': 'admin@localhost.local'
    }
    
    print("Setting up environment variables...")
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"  {key}={value}")
    
    return True

def init_database():
    """Initialize SQLite database"""
    print("Initializing database...")
    
    # Remove existing database for fresh start
    db_file = 'local_devices.db'
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"  Removed existing database: {db_file}")
    
    try:
        # Import and initialize Flask app
        sys.path.insert(0, os.getcwd())
        from app import create_app, db
        from app.models import User, Device, Camera, Alert
        
        app = create_app()
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("  ✅ Database tables created")
            
            # Create default admin user
            admin_user = User(
                username='admin',
                email='admin@localhost.local',
                role='admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            
            # Create test operator user
            operator_user = User(
                username='operator',
                email='operator@localhost.local',
                role='operator'
            )
            operator_user.set_password('operator123')
            db.session.add(operator_user)
            
            # Create test viewer user
            viewer_user = User(
                username='viewer',
                email='viewer@localhost.local',
                role='viewer'
            )
            viewer_user.set_password('viewer123')
            db.session.add(viewer_user)
            
            # Create sample devices
            sample_device = Device(
                name='Test-Switch-01',
                ip_address='192.168.1.10',
                vendor='Cisco',
                device_type='switch',
                snmp_community='public',
                status='unknown'
            )
            db.session.add(sample_device)
            
            sample_router = Device(
                name='Test-Router-01',
                ip_address='192.168.1.1',
                vendor='Cisco',
                device_type='router',
                snmp_community='public',
                status='unknown'
            )
            db.session.add(sample_router)
            
            # Create sample camera
            sample_camera = Camera(
                name='Test-Camera-01',
                ip_address='192.168.1.20',
                rtsp_url='rtsp://192.168.1.20:554/stream1',
                username='admin',
                password='password',
                location='Test Location',
                status='unknown'
            )
            db.session.add(sample_camera)
            
            # Create sample alert
            sample_alert = Alert(
                device_id=1,
                severity='info',
                message='System initialized with test data',
                acknowledged=False
            )
            db.session.add(sample_alert)
            
            db.session.commit()
            print("  ✅ Sample data created")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Database initialization failed: {e}")
        return False

def check_redis():
    """Check if Redis is available (optional for local testing)"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis is available")
        return True
    except Exception:
        print("⚠️  Redis not available - background tasks will not work")
        print("   To install Redis:")
        print("   - Windows: Download from https://github.com/microsoftarchive/redis/releases")
        print("   - macOS: brew install redis")
        print("   - Linux: sudo apt-get install redis-server")
        return False

def create_test_script():
    """Create API testing script"""
    test_script = '''#!/usr/bin/env python3
"""
API Testing Script

Test the backend API endpoints locally.
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_login():
    """Test user authentication"""
    print("Testing login...")
    
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"✅ Login successful - Token: {token[:20]}...")
        return token
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None

def test_devices(token):
    """Test device endpoints"""
    print("Testing device endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # List devices
    response = requests.get(f"{BASE_URL}/devices/", headers=headers)
    if response.status_code == 200:
        devices = response.json()
        print(f"✅ Listed {len(devices)} devices")
    else:
        print(f"❌ Failed to list devices: {response.status_code}")
        return
    
    # Create new device
    new_device = {
        "name": "API-Test-Device",
        "ip_address": "192.168.1.100",
        "vendor": "Test Vendor",
        "device_type": "test"
    }
    
    response = requests.post(f"{BASE_URL}/devices/", json=new_device, headers=headers)
    if response.status_code == 201:
        device = response.json()
        print(f"✅ Created device: {device['name']}")
        device_id = device['id']
        
        # Test device polling
        response = requests.post(f"{BASE_URL}/devices/{device_id}/poll", headers=headers)
        if response.status_code == 200:
            print("✅ Device polling initiated")
        else:
            print(f"⚠️  Device polling failed: {response.status_code}")
    else:
        print(f"❌ Failed to create device: {response.status_code}")

def test_cameras(token):
    """Test camera endpoints"""
    print("Testing camera endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # List cameras
    response = requests.get(f"{BASE_URL}/cameras/", headers=headers)
    if response.status_code == 200:
        cameras = response.json()
        print(f"✅ Listed {len(cameras)} cameras")
    else:
        print(f"❌ Failed to list cameras: {response.status_code}")

def test_alerts(token):
    """Test alert endpoints"""
    print("Testing alert endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # List alerts
    response = requests.get(f"{BASE_URL}/alerts/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        alerts = data.get('alerts', [])
        print(f"✅ Listed {len(alerts)} alerts")
    else:
        print(f"❌ Failed to list alerts: {response.status_code}")

def main():
    """Run all API tests"""
    print("=== API Testing ===\\n")
    
    # Test authentication
    token = test_login()
    if not token:
        print("Cannot proceed without authentication")
        return
    
    print()
    
    # Test all endpoints
    test_devices(token)
    print()
    test_cameras(token)
    print()
    test_alerts(token)
    
    print("\\n=== Testing Complete ===")
    print("Check the Flask app logs for detailed information")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask app. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed: {e}")
'''
    
    with open('test_api.py', 'w') as f:
        f.write(test_script)
    
    print("✅ Created API test script: test_api.py")

def main():
    """Main function to set up local testing environment"""
    print("=== Local Backend Testing Setup ===\n")
    
    # Check Python version
    if not check_python_version():
        return 1
    
    print()
    
    # Check/install dependencies
    if not check_dependencies():
        print("Installing missing dependencies...")
        if not install_dependencies():
            return 1
    
    print()
    
    # Set up environment
    setup_environment()
    print()
    
    # Initialize database
    if not init_database():
        return 1
    
    print()
    
    # Check Redis (optional)
    redis_available = check_redis()
    print()
    
    # Create test script
    create_test_script()
    print()
    
    # Final instructions
    print("=== Setup Complete! ===")
    print()
    print("To start the Flask application:")
    print("  python run.py")
    print()
    print("To test the API (in another terminal):")
    print("  python test_api.py")
    print()
    print("Default users created:")
    print("  Admin:    username=admin,    password=admin123")
    print("  Operator: username=operator, password=operator123") 
    print("  Viewer:   username=viewer,   password=viewer123")
    print()
    print("API will be available at: http://localhost:5000/api")
    print()
    
    if not redis_available:
        print("⚠️  Note: Background tasks (polling) won't work without Redis")
        print("   The Flask app will still work for CRUD operations")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
