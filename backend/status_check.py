#!/usr/bin/env python3
"""
Backend Status Check
"""
import requests
import json

def check_status():
    try:
        # Login
        login_response = requests.post('http://localhost:5000/api/auth/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        
        if login_response.status_code != 200:
            print("✗ Authentication failed")
            return
        
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Check endpoints
        devices = requests.get('http://localhost:5000/api/devices/', headers=headers).json()
        cameras = requests.get('http://localhost:5000/api/cameras/', headers=headers).json()
        alerts = requests.get('http://localhost:5000/api/alerts/', headers=headers).json()
        
        print("=== Backend Status Summary ===")
        print(f"✓ Authentication: Working")
        print(f"✓ Database: Working") 
        print(f"✓ API Endpoints: Working")
        print(f"✓ Devices: {len(devices)} registered")
        print(f"✓ Cameras: {len(cameras)} registered")
        print(f"✓ Alerts: {len(alerts.get('alerts', []))} total")
        print()
        print("✓ Backend is fully operational!")
        print()
        print("API Base URL: http://localhost:5000/api")
        print("Admin Login: admin / admin123")
        
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Flask app. Make sure it's running.")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    check_status()
