"""
Comprehensive endpoint testing script for Device Monitoring System
Tests all API endpoints and generates a report
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"
TEST_RESULTS = []

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def log_test(endpoint, method, status, expected, result, error=None):
    """Log test result"""
    passed = status == expected
    TEST_RESULTS.append({
        'endpoint': endpoint,
        'method': method,
        'status': status,
        'expected': expected,
        'passed': passed,
        'result': result,
        'error': error
    })
    
    icon = "[OK]" if passed else "[ERROR]"
    color = Colors.GREEN if passed else Colors.RED
    print(f"{color}{icon}{Colors.RESET} {method:6} {endpoint:40} - Status: {status} (Expected: {expected})")
    if error:
        print(f"     Error: {error}")

def test_auth_endpoints(session):
    """Test authentication endpoints"""
    print(f"\n{Colors.BLUE}=== Testing Authentication Endpoints ==={Colors.RESET}")
    
    # Test login
    response = session.post(f"{BASE_URL}/auth/login", json={
        'username': 'admin',
        'password': 'admin123'
    })
    log_test('/auth/login', 'POST', response.status_code, 200, response.json())
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        session.headers.update({'Authorization': f'Bearer {token}'})
    
    # Test profile
    response = session.get(f"{BASE_URL}/auth/profile")
    log_test('/auth/profile', 'GET', response.status_code, 200, response.json() if response.ok else None)
    
    # Test list users (admin only)
    response = session.get(f"{BASE_URL}/auth/users")
    log_test('/auth/users', 'GET', response.status_code, 200, response.json() if response.ok else None)
    
    # Test create user
    response = session.post(f"{BASE_URL}/auth/users", json={
        'username': f'testuser_{datetime.now().timestamp()}',
        'email': f'test_{datetime.now().timestamp()}@example.com',
        'password': 'Test1234',
        'role': 'viewer'
    })
    log_test('/auth/users', 'POST', response.status_code, 201, response.json() if response.ok else None)
    
    created_user_id = response.json().get('id') if response.ok else None
    
    # Test update user
    if created_user_id:
        response = session.put(f"{BASE_URL}/auth/users/{created_user_id}", json={
            'role': 'operator'
        })
        log_test(f'/auth/users/{created_user_id}', 'PUT', response.status_code, 200, response.json() if response.ok else None)
    
    # Test delete user
    if created_user_id:
        response = session.delete(f"{BASE_URL}/auth/users/{created_user_id}")
        log_test(f'/auth/users/{created_user_id}', 'DELETE', response.status_code, 200, response.json() if response.ok else None)

def test_device_endpoints(session):
    """Test device endpoints"""
    print(f"\n{Colors.BLUE}=== Testing Device Endpoints ==={Colors.RESET}")
    
    # Test create device
    response = session.post(f"{BASE_URL}/devices/", json={
        'name': f'Test Device {datetime.now().timestamp()}',
        'ip_address': f'192.168.1.{int(datetime.now().timestamp()) % 255}',
        'vendor': 'Test Vendor',
        'device_type': 'router',
        'snmp_community': 'public'
    })
    log_test('/devices/', 'POST', response.status_code, 201, response.json() if response.ok else None)
    
    device_id = response.json().get('id') if response.ok else None
    
    # Test list devices
    response = session.get(f"{BASE_URL}/devices/")
    log_test('/devices/', 'GET', response.status_code, 200, len(response.json()) if response.ok else None)
    
    # Test get device
    if device_id:
        response = session.get(f"{BASE_URL}/devices/{device_id}")
        log_test(f'/devices/{device_id}', 'GET', response.status_code, 200, response.json() if response.ok else None)
    
    # Test update device
    if device_id:
        response = session.put(f"{BASE_URL}/devices/{device_id}", json={
            'name': 'Updated Test Device',
            'vendor': 'Updated Vendor'
        })
        log_test(f'/devices/{device_id}', 'PUT', response.status_code, 200, response.json() if response.ok else None)
    
    # Test device status summary
    response = session.get(f"{BASE_URL}/devices/status")
    log_test('/devices/status', 'GET', response.status_code, 200, response.json() if response.ok else None)
    
    # Test poll device
    if device_id:
        response = session.post(f"{BASE_URL}/devices/{device_id}/poll")
        # May return 500 if Celery is not running, which is acceptable
        log_test(f'/devices/{device_id}/poll', 'POST', response.status_code, [200, 500], response.json() if response.ok else None)
    
    # Test delete device
    if device_id:
        response = session.delete(f"{BASE_URL}/devices/{device_id}")
        log_test(f'/devices/{device_id}', 'DELETE', response.status_code, 200, response.json() if response.ok else None)

def test_camera_endpoints(session):
    """Test camera endpoints"""
    print(f"\n{Colors.BLUE}=== Testing Camera Endpoints ==={Colors.RESET}")
    
    # Test create camera
    response = session.post(f"{BASE_URL}/cameras/", json={
        'name': f'Test Camera {datetime.now().timestamp()}',
        'ip_address': f'192.168.2.{int(datetime.now().timestamp()) % 255}',
        'rtsp_url': 'rtsp://192.168.2.100:554/stream',
        'username': 'admin',
        'password': 'password',
        'location': 'Test Location'
    })
    log_test('/cameras/', 'POST', response.status_code, 201, response.json() if response.ok else None)
    
    camera_id = response.json().get('id') if response.ok else None
    
    # Test list cameras
    response = session.get(f"{BASE_URL}/cameras/")
    log_test('/cameras/', 'GET', response.status_code, 200, len(response.json()) if response.ok else None)
    
    # Test get camera
    if camera_id:
        response = session.get(f"{BASE_URL}/cameras/{camera_id}")
        log_test(f'/cameras/{camera_id}', 'GET', response.status_code, 200, response.json() if response.ok else None)
    
    # Test update camera
    if camera_id:
        response = session.put(f"{BASE_URL}/cameras/{camera_id}", json={
            'name': 'Updated Test Camera',
            'location': 'Updated Location'
        })
        log_test(f'/cameras/{camera_id}', 'PUT', response.status_code, 200, response.json() if response.ok else None)
    
    # Test camera status summary
    response = session.get(f"{BASE_URL}/cameras/status")
    log_test('/cameras/status', 'GET', response.status_code, 200, response.json() if response.ok else None)
    
    # Test get camera stream
    if camera_id:
        response = session.get(f"{BASE_URL}/cameras/{camera_id}/stream")
        log_test(f'/cameras/{camera_id}/stream', 'GET', response.status_code, 200, response.json() if response.ok else None)
    
    # Test camera connection test
    if camera_id:
        response = session.post(f"{BASE_URL}/cameras/{camera_id}/test")
        # May return 500 if test fails, which is acceptable
        log_test(f'/cameras/{camera_id}/test', 'POST', response.status_code, [200, 500], response.json() if response.ok else None)
    
    # Test delete camera
    if camera_id:
        response = session.delete(f"{BASE_URL}/cameras/{camera_id}")
        log_test(f'/cameras/{camera_id}', 'DELETE', response.status_code, 200, response.json() if response.ok else None)

def test_alert_endpoints(session):
    """Test alert endpoints"""
    print(f"\n{Colors.BLUE}=== Testing Alert Endpoints ==={Colors.RESET}")
    
    # Create a test device for alerts
    device_response = session.post(f"{BASE_URL}/devices/", json={
        'name': 'Alert Test Device',
        'ip_address': '192.168.99.99',
        'vendor': 'Test',
        'device_type': 'test'
    })
    device_id = device_response.json().get('id') if device_response.ok else None
    
    # Test create alert
    response = session.post(f"{BASE_URL}/alerts/", json={
        'device_id': device_id,
        'severity': 'high',
        'message': f'Test alert created at {datetime.now()}'
    })
    log_test('/alerts/', 'POST', response.status_code, 201, response.json() if response.ok else None)
    
    alert_id = response.json().get('id') if response.ok else None
    
    # Test list alerts
    response = session.get(f"{BASE_URL}/alerts/")
    log_test('/alerts/', 'GET', response.status_code, 200, response.json().get('pagination') if response.ok else None)
    
    # Test get alert
    if alert_id:
        response = session.get(f"{BASE_URL}/alerts/{alert_id}")
        log_test(f'/alerts/{alert_id}', 'GET', response.status_code, 200, response.json() if response.ok else None)
    
    # Test alerts summary
    response = session.get(f"{BASE_URL}/alerts/summary")
    log_test('/alerts/summary', 'GET', response.status_code, 200, response.json() if response.ok else None)
    
    # Test acknowledge alert
    if alert_id:
        response = session.post(f"{BASE_URL}/alerts/{alert_id}/acknowledge")
        log_test(f'/alerts/{alert_id}/acknowledge', 'POST', response.status_code, 200, response.json() if response.ok else None)
    
    # Test acknowledge all alerts
    response = session.post(f"{BASE_URL}/alerts/acknowledge-all", json={
        'severity': 'high'
    })
    log_test('/alerts/acknowledge-all', 'POST', response.status_code, 200, response.json() if response.ok else None)
    
    # Test delete alert
    if alert_id:
        response = session.delete(f"{BASE_URL}/alerts/{alert_id}")
        log_test(f'/alerts/{alert_id}', 'DELETE', response.status_code, 200, response.json() if response.ok else None)
    
    # Clean up test device
    if device_id:
        session.delete(f"{BASE_URL}/devices/{device_id}")

def print_summary():
    """Print test summary"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}=== Test Summary ==={Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    total = len(TEST_RESULTS)
    passed = sum(1 for r in TEST_RESULTS if r['passed'])
    failed = total - passed
    
    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
    print(f"Success Rate: {(passed/total*100):.1f}%\n")
    
    if failed > 0:
        print(f"{Colors.RED}Failed Tests:{Colors.RESET}")
        for result in TEST_RESULTS:
            if not result['passed']:
                print(f"  - {result['method']:6} {result['endpoint']:40} (Status: {result['status']}, Expected: {result['expected']})")
                if result.get('error'):
                    print(f"    Error: {result['error']}")

def main():
    """Main test runner"""
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}Device Monitoring System - API Endpoint Testing{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"Testing server at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})

    # Ensure requests have a sensible default timeout to avoid hanging tests
    # Wrap the session.request method to add a default timeout when one is not provided.
    _orig_request = session.request
    def _request_with_timeout(method, url, **kwargs):
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 8
        return _orig_request(method, url, **kwargs)
    session.request = _request_with_timeout
    
    try:
        # Run all endpoint tests
        test_auth_endpoints(session)
        test_device_endpoints(session)
        test_camera_endpoints(session)
        test_alert_endpoints(session)
        
        # Print summary
        print_summary()
        
        # Save results to file
        with open('test_results.json', 'w') as f:
            json.dump(TEST_RESULTS, f, indent=2)
        print(f"\n{Colors.GREEN}[OK]{Colors.RESET} Test results saved to test_results.json")
        
    except requests.exceptions.ConnectionError:
        print(f"\n{Colors.RED}[ERROR]{Colors.RESET} Could not connect to server at {BASE_URL}")
        print("Please ensure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR]{Colors.RESET} Test execution failed: {str(e)}")

if __name__ == '__main__':
    main()
