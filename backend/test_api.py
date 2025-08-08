#!/usr/bin/env python3
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
        print(f"✓ Login successful - Token: {token[:20]}...")
        return token
    else:
        print(f"✗ Login failed: {response.status_code} - {response.text}")
        return None

def test_devices(token):
    """Test device endpoints"""
    print("Testing device endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # List devices
    response = requests.get(f"{BASE_URL}/devices/", headers=headers)
    if response.status_code == 200:
        devices = response.json()
        print(f"✓ Listed {len(devices)} devices")
    else:
        print(f"✗ Failed to list devices: {response.status_code}")
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
        print(f"✓ Created device: {device['name']}")
        device_id = device['id']
        
        # Test device polling
        response = requests.post(f"{BASE_URL}/devices/{device_id}/poll", headers=headers)
        if response.status_code == 200:
            print("✓ Device polling initiated")
        else:
            print(f"! Device polling failed: {response.status_code}")
    else:
        print(f"✗ Failed to create device: {response.status_code}")

def test_cameras(token):
    """Test camera endpoints"""
    print("Testing camera endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # List cameras
    response = requests.get(f"{BASE_URL}/cameras/", headers=headers)
    if response.status_code == 200:
        cameras = response.json()
        print(f"✓ Listed {len(cameras)} cameras")
    else:
        print(f"✗ Failed to list cameras: {response.status_code}")

def test_alerts(token):
    """Test alert endpoints"""
    print("Testing alert endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # List alerts
    response = requests.get(f"{BASE_URL}/alerts/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        alerts = data.get('alerts', [])
        print(f"✓ Listed {len(alerts)} alerts")
    else:
        print(f"✗ Failed to list alerts: {response.status_code}")

def main():
    """Run all API tests"""
    print("=== API Testing ===\n")
    
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
    
    print("\n=== Testing Complete ===")
    print("Check the Flask app logs for detailed information")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Flask app. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"✗ Test failed: {e}")
