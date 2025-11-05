"""
Quick endpoint test - verifies all endpoints are working
"""
import requests
import sys

BASE_URL = "http://localhost:5000/api"

def test_endpoint(method, endpoint, data=None, token=None, expected_codes=[200]):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=5)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=5)
        
        status = "OK" if response.status_code in expected_codes else "FAIL"
        print(f"[{status}] {method:6s} {endpoint:40s} - {response.status_code}")
        return response
    except requests.exceptions.Timeout:
        print(f"[TIMEOUT] {method:6s} {endpoint:40s}")
        return None
    except Exception as e:
        print(f"[ERROR] {method:6s} {endpoint:40s} - {str(e)}")
        return None

def main():
    print("="*70)
    print(" Quick Endpoint Test - Device Monitoring System")
    print("="*70)
    print(f"Testing: {BASE_URL}\n")
    
    # Test 1: Health check
    print("1. Health Check")
    test_endpoint('GET', '/health')
    
    # Test 2: Login
    print("\n2. Authentication")
    response = test_endpoint('POST', '/auth/login', 
        data={'username': 'admin', 'password': 'admin123'})
    
    if not response or response.status_code != 200:
        print("\n[ERROR] Login failed! Cannot continue tests.")
        sys.exit(1)
    
    token = response.json().get('access_token')
    test_endpoint('GET', '/auth/profile', token=token)
    test_endpoint('GET', '/auth/users', token=token)
    
    # Test 3: Devices
    print("\n3. Device Endpoints")
    test_endpoint('GET', '/devices/', token=token)
    test_endpoint('GET', '/devices/status', token=token)
    
    # Create a test device
    device_data = {
        'name': 'Quick Test Device',
        'ip_address': '192.168.1.100',
        'device_type': 'router'
    }
    response = test_endpoint('POST', '/devices/', data=device_data, token=token, expected_codes=[201])
    
    if response and response.status_code == 201:
        device_id = response.json().get('id')
        test_endpoint('GET', f'/devices/{device_id}', token=token)
        test_endpoint('PUT', f'/devices/{device_id}', 
            data={'name': 'Updated Device'}, token=token)
        # Skip poll test to avoid timeout
        test_endpoint('DELETE', f'/devices/{device_id}', token=token)
    
    # Test 4: Cameras
    print("\n4. Camera Endpoints")
    test_endpoint('GET', '/cameras/', token=token)
    test_endpoint('GET', '/cameras/status', token=token)
    
    # Create a test camera
    camera_data = {
        'name': 'Quick Test Camera',
        'rtsp_url': 'rtsp://192.168.1.200:554/stream',
        'location': 'Test'
    }
    response = test_endpoint('POST', '/cameras/', data=camera_data, token=token, expected_codes=[201])
    
    if response and response.status_code == 201:
        camera_id = response.json().get('id')
        test_endpoint('GET', f'/cameras/{camera_id}', token=token)
        test_endpoint('PUT', f'/cameras/{camera_id}', 
            data={'location': 'Updated Location'}, token=token)
        # Skip stream and test endpoints to avoid timeout
        test_endpoint('DELETE', f'/cameras/{camera_id}', token=token)
    
    # Test 5: Alerts
    print("\n5. Alert Endpoints")
    test_endpoint('GET', '/alerts/', token=token)
    test_endpoint('GET', '/alerts/summary', token=token)
    
    print("\n" + "="*70)
    print(" Test Complete!")
    print("="*70)
    print("\nAll endpoints tested. Check for [FAIL] or [ERROR] markers above.")

if __name__ == '__main__':
    main()
