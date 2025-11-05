#!/usr/bin/env python3
"""
Comprehensive Endpoint Testing Script

This script tests all API endpoints to ensure they are working correctly.
Run this after starting the server with start.py
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api"

# Test credentials
ADMIN_CREDS = {"username": "admin", "password": "Admin@123"}
OPERATOR_CREDS = {"username": "operator", "password": "Operator@123"}
VIEWER_CREDS = {"username": "viewer", "password": "Viewer@123"}

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message"""
    print(f"  {text}")

def test_health_check():
    """Test health check endpoints"""
    print_header("Testing Health Check Endpoints")
    
    try:
        # Test basic health check
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success(f"GET /health - Status: {response.status_code}")
            print_info(f"Response: {response.json()}")
        else:
            print_error(f"GET /health - Status: {response.status_code}")
        
        # Test API health check
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print_success(f"GET /api/health - Status: {response.status_code}")
            print_info(f"Response: {response.json()}")
        else:
            print_error(f"GET /api/health - Status: {response.status_code}")
        
        return True
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

def test_authentication():
    """Test authentication endpoints"""
    print_header("Testing Authentication Endpoints")
    
    tokens = {}
    
    try:
        # Test admin login
        print("\nTesting Admin Login:")
        response = requests.post(
            f"{API_URL}/auth/login",
            json=ADMIN_CREDS,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            tokens['admin'] = data.get('access_token')
            print_success(f"Admin login successful")
            print_info(f"Username: {data.get('user', {}).get('username')}")
            print_info(f"Role: {data.get('user', {}).get('role')}")
            print_info(f"Token: {tokens['admin'][:20]}...")
        else:
            print_error(f"Admin login failed - Status: {response.status_code}")
            print_info(f"Response: {response.text}")
        
        # Test operator login
        print("\nTesting Operator Login:")
        response = requests.post(
            f"{API_URL}/auth/login",
            json=OPERATOR_CREDS,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            tokens['operator'] = data.get('access_token')
            print_success(f"Operator login successful")
            print_info(f"Username: {data.get('user', {}).get('username')}")
            print_info(f"Role: {data.get('user', {}).get('role')}")
        else:
            print_error(f"Operator login failed - Status: {response.status_code}")
        
        # Test viewer login
        print("\nTesting Viewer Login:")
        response = requests.post(
            f"{API_URL}/auth/login",
            json=VIEWER_CREDS,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            tokens['viewer'] = data.get('access_token')
            print_success(f"Viewer login successful")
            print_info(f"Username: {data.get('user', {}).get('username')}")
            print_info(f"Role: {data.get('user', {}).get('role')}")
        else:
            print_error(f"Viewer login failed - Status: {response.status_code}")
        
        # Test profile endpoint
        if tokens.get('admin'):
            print("\nTesting Profile Endpoint:")
            response = requests.get(
                f"{API_URL}/auth/profile",
                headers={"Authorization": f"Bearer {tokens['admin']}"}
            )
            
            if response.status_code == 200:
                print_success(f"Profile retrieved successfully")
                print_info(f"Data: {response.json()}")
            else:
                print_error(f"Profile retrieval failed - Status: {response.status_code}")
        
        # Test list users (admin only)
        if tokens.get('admin'):
            print("\nTesting List Users (Admin):")
            response = requests.get(
                f"{API_URL}/auth/users",
                headers={"Authorization": f"Bearer {tokens['admin']}"}
            )
            
            if response.status_code == 200:
                users = response.json()
                print_success(f"Users list retrieved successfully")
                print_info(f"Total users: {len(users)}")
                for user in users:
                    print_info(f"  - {user['username']} ({user['role']})")
            else:
                print_error(f"List users failed - Status: {response.status_code}")
        
        return tokens
    
    except Exception as e:
        print_error(f"Authentication test failed: {str(e)}")
        return {}

def test_devices(token):
    """Test device endpoints"""
    print_header("Testing Device Endpoints")
    
    device_id = None
    
    try:
        # Test create device
        print("\nTesting Create Device:")
        device_data = {
            "name": "Test Switch",
            "ip_address": "192.168.1.100",
            "vendor": "Cisco",
            "device_type": "switch",
            "snmp_community": "public",
            "meta": {"location": "Server Room"}
        }
        
        response = requests.post(
            f"{API_URL}/devices/",
            json=device_data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 201:
            device = response.json()
            device_id = device.get('id')
            print_success(f"Device created successfully")
            print_info(f"Device ID: {device_id}")
            print_info(f"Name: {device.get('name')}")
            print_info(f"IP: {device.get('ip_address')}")
        else:
            print_error(f"Create device failed - Status: {response.status_code}")
            print_info(f"Response: {response.text}")
        
        # Test list devices
        print("\nTesting List Devices:")
        response = requests.get(
            f"{API_URL}/devices/",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            devices = response.json()
            print_success(f"Devices list retrieved successfully")
            print_info(f"Total devices: {len(devices)}")
            for dev in devices[:3]:  # Show first 3
                print_info(f"  - {dev['name']} ({dev['ip_address']}) - Status: {dev['status']}")
        else:
            print_error(f"List devices failed - Status: {response.status_code}")
        
        # Test get device
        if device_id:
            print("\nTesting Get Device:")
            response = requests.get(
                f"{API_URL}/devices/{device_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                device = response.json()
                print_success(f"Device retrieved successfully")
                print_info(f"Device: {json.dumps(device, indent=2)}")
            else:
                print_error(f"Get device failed - Status: {response.status_code}")
        
        # Test update device
        if device_id:
            print("\nTesting Update Device:")
            update_data = {
                "name": "Updated Test Switch",
                "vendor": "Cisco Systems"
            }
            
            response = requests.put(
                f"{API_URL}/devices/{device_id}",
                json=update_data,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                device = response.json()
                print_success(f"Device updated successfully")
                print_info(f"New name: {device.get('name')}")
            else:
                print_error(f"Update device failed - Status: {response.status_code}")
        
        # Test device status summary
        print("\nTesting Device Status Summary:")
        response = requests.get(
            f"{API_URL}/devices/status",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            status = response.json()
            print_success(f"Device status retrieved successfully")
            print_info(f"Total: {status.get('total')}")
            print_info(f"Online: {status.get('online')}")
            print_info(f"Offline: {status.get('offline')}")
            print_info(f"Unknown: {status.get('unknown')}")
        else:
            print_error(f"Device status failed - Status: {response.status_code}")
        
        # Test poll device
        if device_id:
            print("\nTesting Poll Device:")
            response = requests.post(
                f"{API_URL}/devices/{device_id}/poll",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code in [200, 202]:
                result = response.json()
                print_success(f"Device poll initiated")
                print_info(f"Response: {result}")
            else:
                print_error(f"Poll device failed - Status: {response.status_code}")
        
        return device_id
    
    except Exception as e:
        print_error(f"Device test failed: {str(e)}")
        return None

def test_cameras(token):
    """Test camera endpoints"""
    print_header("Testing Camera Endpoints")
    
    camera_id = None
    
    try:
        # Test create camera
        print("\nTesting Create Camera:")
        camera_data = {
            "name": "Front Door Camera",
            "ip_address": "192.168.1.200",
            "rtsp_url": "rtsp://192.168.1.200:554/stream",
            "username": "admin",
            "password": "password123",
            "location": "Main Entrance"
        }
        
        response = requests.post(
            f"{API_URL}/cameras/",
            json=camera_data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 201:
            camera = response.json()
            camera_id = camera.get('id')
            print_success(f"Camera created successfully")
            print_info(f"Camera ID: {camera_id}")
            print_info(f"Name: {camera.get('name')}")
            print_info(f"Location: {camera.get('location')}")
        else:
            print_error(f"Create camera failed - Status: {response.status_code}")
            print_info(f"Response: {response.text}")
        
        # Test list cameras
        print("\nTesting List Cameras:")
        response = requests.get(
            f"{API_URL}/cameras/",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            cameras = response.json()
            print_success(f"Cameras list retrieved successfully")
            print_info(f"Total cameras: {len(cameras)}")
            for cam in cameras[:3]:  # Show first 3
                print_info(f"  - {cam['name']} ({cam['ip_address']}) - Status: {cam['status']}")
        else:
            print_error(f"List cameras failed - Status: {response.status_code}")
        
        # Test get camera
        if camera_id:
            print("\nTesting Get Camera:")
            response = requests.get(
                f"{API_URL}/cameras/{camera_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                camera = response.json()
                print_success(f"Camera retrieved successfully")
                print_info(f"Camera: {camera.get('name')}")
            else:
                print_error(f"Get camera failed - Status: {response.status_code}")
        
        # Test camera status summary
        print("\nTesting Camera Status Summary:")
        response = requests.get(
            f"{API_URL}/cameras/status",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            status = response.json()
            print_success(f"Camera status retrieved successfully")
            print_info(f"Total: {status.get('total')}")
            print_info(f"Online: {status.get('online')}")
            print_info(f"Offline: {status.get('offline')}")
        else:
            print_error(f"Camera status failed - Status: {response.status_code}")
        
        return camera_id
    
    except Exception as e:
        print_error(f"Camera test failed: {str(e)}")
        return None

def test_alerts(token, device_id):
    """Test alert endpoints"""
    print_header("Testing Alert Endpoints")
    
    alert_id = None
    
    try:
        # Test create alert
        print("\nTesting Create Alert:")
        alert_data = {
            "device_id": device_id,
            "severity": "high",
            "message": "Test alert - device connectivity issue"
        }
        
        response = requests.post(
            f"{API_URL}/alerts/",
            json=alert_data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 201:
            alert = response.json()
            alert_id = alert.get('id')
            print_success(f"Alert created successfully")
            print_info(f"Alert ID: {alert_id}")
            print_info(f"Severity: {alert.get('severity')}")
            print_info(f"Message: {alert.get('message')}")
        else:
            print_error(f"Create alert failed - Status: {response.status_code}")
            print_info(f"Response: {response.text}")
        
        # Test list alerts
        print("\nTesting List Alerts:")
        response = requests.get(
            f"{API_URL}/alerts/",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            print_success(f"Alerts list retrieved successfully")
            print_info(f"Total alerts: {len(alerts)}")
            for alert in alerts[:3]:  # Show first 3
                print_info(f"  - [{alert['severity']}] {alert['message']}")
        else:
            print_error(f"List alerts failed - Status: {response.status_code}")
        
        # Test alerts summary
        print("\nTesting Alerts Summary:")
        response = requests.get(
            f"{API_URL}/alerts/summary",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            summary = response.json()
            print_success(f"Alerts summary retrieved successfully")
            print_info(f"Total: {summary.get('total')}")
            print_info(f"Unacknowledged: {summary.get('unacknowledged')}")
            print_info(f"Critical: {summary.get('critical')}")
            print_info(f"High: {summary.get('high')}")
        else:
            print_error(f"Alerts summary failed - Status: {response.status_code}")
        
        # Test acknowledge alert
        if alert_id:
            print("\nTesting Acknowledge Alert:")
            response = requests.post(
                f"{API_URL}/alerts/{alert_id}/acknowledge",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print_success(f"Alert acknowledged successfully")
                print_info(f"Response: {result.get('msg')}")
            else:
                print_error(f"Acknowledge alert failed - Status: {response.status_code}")
        
        return alert_id
    
    except Exception as e:
        print_error(f"Alert test failed: {str(e)}")
        return None

def cleanup(admin_token, device_id, camera_id, alert_id):
    """Clean up test data"""
    print_header("Cleaning Up Test Data")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Delete alert
    if alert_id:
        try:
            response = requests.delete(f"{API_URL}/alerts/{alert_id}", headers=headers)
            if response.status_code == 200:
                print_success(f"Deleted alert {alert_id}")
            else:
                print_warning(f"Could not delete alert {alert_id}")
        except:
            pass
    
    # Delete camera
    if camera_id:
        try:
            response = requests.delete(f"{API_URL}/cameras/{camera_id}", headers=headers)
            if response.status_code == 200:
                print_success(f"Deleted camera {camera_id}")
            else:
                print_warning(f"Could not delete camera {camera_id}")
        except:
            pass
    
    # Delete device
    if device_id:
        try:
            response = requests.delete(f"{API_URL}/devices/{device_id}", headers=headers)
            if response.status_code == 200:
                print_success(f"Deleted device {device_id}")
            else:
                print_warning(f"Could not delete device {device_id}")
        except:
            pass

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f"Device Monitoring System - Endpoint Testing")
    print(f"{'='*60}{Colors.ENDC}\n")
    print(f"Testing server at: {BASE_URL}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Test health check
    if not test_health_check():
        print_error("\n❌ Server is not responding. Please start the server first.")
        print_info("Run: python start.py")
        sys.exit(1)
    
    # Test authentication
    tokens = test_authentication()
    if not tokens.get('admin'):
        print_error("\n❌ Authentication failed. Cannot proceed with tests.")
        sys.exit(1)
    
    # Test devices
    device_id = test_devices(tokens.get('operator', tokens['admin']))
    
    # Test cameras
    camera_id = test_cameras(tokens.get('operator', tokens['admin']))
    
    # Test alerts
    alert_id = test_alerts(tokens.get('operator', tokens['admin']), device_id)
    
    # Cleanup
    cleanup(tokens['admin'], device_id, camera_id, alert_id)
    
    # Summary
    print_header("Test Summary")
    print_success("✓ All endpoint tests completed!")
    print_info(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info("\nNext steps:")
    print_info("  1. Check the application logs for any errors")
    print_info("  2. Access the web interface at http://localhost:5000")
    print_info("  3. Login with admin credentials")
    print_info("  4. Test the frontend functionality")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\nTest interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"\n\nTest failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
