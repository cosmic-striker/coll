#!/usr/bin/env python3
"""
Comprehensive Test Suite for Device Monitoring System
Tests all endpoints, APIs, and functionality including:
- Authentication & Authorization
- Device Management (CRUD operations)
- Camera Management (CRUD operations)
- Alert Management
- Status checks and health endpoints
- Error handling and edge cases
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Optional, List, Tuple
from colorama import init, Fore, Style
import sys

# Initialize colorama for colored output
init(autoreset=True)

class DeviceMonitoringTester:
    """Comprehensive testing class for Device Monitoring System"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.test_results: List[Tuple[str, bool, str]] = []
        self.created_resources: Dict[str, List[int]] = {
            'devices': [],
            'cameras': [],
            'alerts': []
        }
        
    def print_header(self, text: str):
        """Print formatted section header"""
        print(f"\n{'=' * 80}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{text:^80}{Style.RESET_ALL}")
        print(f"{'=' * 80}\n")
        
    def print_success(self, message: str):
        """Print success message"""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
        
    def print_error(self, message: str):
        """Print error message"""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
        
    def print_info(self, message: str):
        """Print info message"""
        print(f"{Fore.YELLOW}ℹ {message}{Style.RESET_ALL}")
        
    def record_test(self, test_name: str, passed: bool, details: str = ""):
        """Record test result"""
        self.test_results.append((test_name, passed, details))
        if passed:
            self.print_success(f"{test_name}: {details}")
        else:
            self.print_error(f"{test_name}: {details}")
            
    def get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """Get request headers with optional authentication"""
        headers = {'Content-Type': 'application/json'}
        if include_auth and self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers
        
    # ============================================================================
    # HEALTH & STATUS TESTS
    # ============================================================================
    
    def test_health_endpoints(self):
        """Test health check endpoints"""
        self.print_header("TESTING HEALTH & STATUS ENDPOINTS")
        
        # Test root health endpoint
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.record_test("Health Check (/health)", True, 
                               f"Status: {data.get('status')}")
            else:
                self.record_test("Health Check (/health)", False, 
                               f"Status code: {response.status_code}")
        except Exception as e:
            self.record_test("Health Check (/health)", False, str(e))
            
        # Test API health endpoint
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.record_test("API Health Check (/api/health)", True,
                               f"Status: {data.get('status')}, Version: {data.get('version')}")
            else:
                self.record_test("API Health Check (/api/health)", False,
                               f"Status code: {response.status_code}")
        except Exception as e:
            self.record_test("API Health Check (/api/health)", False, str(e))
            
    # ============================================================================
    # AUTHENTICATION TESTS
    # ============================================================================
    
    def test_login(self, username: str = "admin", password: str = "Admin@123"):
        """Test user login"""
        self.print_header("TESTING AUTHENTICATION")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={"username": username, "password": password},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                self.refresh_token = data.get('refresh_token')
                self.record_test("Login (POST /api/auth/login)", True,
                               f"User: {username}, Role: {data.get('role')}")
                return True
            else:
                self.record_test("Login (POST /api/auth/login)", False,
                               f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.record_test("Login (POST /api/auth/login)", False, str(e))
            return False
            
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={"username": "invalid", "password": "wrong"},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 401:
                self.record_test("Invalid Login", True, "Correctly rejected")
            else:
                self.record_test("Invalid Login", False,
                               f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.record_test("Invalid Login", False, str(e))
            
    def test_token_refresh(self):
        """Test token refresh"""
        if not self.refresh_token:
            self.print_info("Skipping token refresh test (no refresh token)")
            return
            
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/refresh",
                headers={'Authorization': f'Bearer {self.refresh_token}'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                self.record_test("Token Refresh (POST /api/auth/refresh)", True,
                               "New token received")
            else:
                self.record_test("Token Refresh (POST /api/auth/refresh)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Token Refresh (POST /api/auth/refresh)", False, str(e))
            
    def test_get_profile(self):
        """Test getting user profile"""
        try:
            response = requests.get(
                f"{self.base_url}/api/auth/profile",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.record_test("Get Profile (GET /api/auth/profile)", True,
                               f"User: {data.get('username')}, Role: {data.get('role')}")
            else:
                self.record_test("Get Profile (GET /api/auth/profile)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Get Profile (GET /api/auth/profile)", False, str(e))
            
    def test_get_users(self):
        """Test getting all users"""
        try:
            response = requests.get(
                f"{self.base_url}/api/auth/users",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.record_test("Get All Users (GET /api/auth/users)", True,
                               f"Found {len(data)} users")
            else:
                self.record_test("Get All Users (GET /api/auth/users)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Get All Users (GET /api/auth/users)", False, str(e))
            
    # ============================================================================
    # DEVICE MANAGEMENT TESTS
    # ============================================================================
    
    def test_device_operations(self):
        """Test all device CRUD operations"""
        self.print_header("TESTING DEVICE MANAGEMENT")
        
        # Test: Get all devices (initial state)
        try:
            response = requests.get(
                f"{self.base_url}/api/devices/",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                devices = response.json()
                self.record_test("Get All Devices (GET /api/devices/)", True,
                               f"Found {len(devices)} devices")
            else:
                self.record_test("Get All Devices (GET /api/devices/)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Get All Devices (GET /api/devices/)", False, str(e))
            
        # Test: Create new device (use unique IP with timestamp)
        timestamp = datetime.now().strftime('%H%M%S')
        device_data = {
            "name": f"Test Device {timestamp}",
            "device_type": "switch",
            "ip_address": f"192.168.100.{int(timestamp) % 255}",  # Unique IP based on timestamp
            "port": 161,
            "community": "public",
            "polling_interval": 60,
            "enabled": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/devices/",
                json=device_data,
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 201:
                device = response.json()
                device_id = device.get('id')
                self.created_resources['devices'].append(device_id)
                self.record_test("Create Device (POST /api/devices/)", True,
                               f"Created device ID: {device_id}")
            else:
                self.record_test("Create Device (POST /api/devices/)", False,
                               f"Status: {response.status_code}, Response: {response.text}")
                return
        except Exception as e:
            self.record_test("Create Device (POST /api/devices/)", False, str(e))
            return
            
        # Test: Get single device
        try:
            response = requests.get(
                f"{self.base_url}/api/devices/{device_id}",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                device = response.json()
                self.record_test("Get Single Device (GET /api/devices/<id>)", True,
                               f"Device: {device.get('name')}")
            else:
                self.record_test("Get Single Device (GET /api/devices/<id>)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Get Single Device (GET /api/devices/<id>)", False, str(e))
            
        # Test: Update device
        update_data = {
            "name": f"Updated Device {datetime.now().strftime('%H%M%S')}",
            "polling_interval": 120
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/api/devices/{device_id}",
                json=update_data,
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                device = response.json()
                self.record_test("Update Device (PUT /api/devices/<id>)", True,
                               f"Updated to: {device.get('name')}")
            else:
                self.record_test("Update Device (PUT /api/devices/<id>)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Update Device (PUT /api/devices/<id>)", False, str(e))
            
        # Test: Poll device
        try:
            response = requests.post(
                f"{self.base_url}/api/devices/{device_id}/poll",
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code in [200, 202]:
                result = response.json()
                self.record_test("Poll Device (POST /api/devices/<id>/poll)", True,
                               f"Status: {result.get('status', 'queued')}")
            else:
                self.record_test("Poll Device (POST /api/devices/<id>/poll)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Poll Device (POST /api/devices/<id>/poll)", False, str(e))
            
        # Test: Get device status
        try:
            response = requests.get(
                f"{self.base_url}/api/devices/status",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                status = response.json()
                self.record_test("Get Device Status (GET /api/devices/status)", True,
                               f"Total: {status.get('total_devices', 0)}")
            else:
                self.record_test("Get Device Status (GET /api/devices/status)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Get Device Status (GET /api/devices/status)", False, str(e))
            
    # ============================================================================
    # CAMERA MANAGEMENT TESTS
    # ============================================================================
    
    def test_camera_operations(self):
        """Test all camera CRUD operations"""
        self.print_header("TESTING CAMERA MANAGEMENT")
        
        # Test: Get all cameras (initial state)
        try:
            response = requests.get(
                f"{self.base_url}/api/cameras/",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                cameras = response.json()
                self.record_test("Get All Cameras (GET /api/cameras/)", True,
                               f"Found {len(cameras)} cameras")
            else:
                self.record_test("Get All Cameras (GET /api/cameras/)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Get All Cameras (GET /api/cameras/)", False, str(e))
            
        # Test: Create new camera (include IP address field)
        import random
        timestamp = datetime.now().strftime('%H%M%S')
        unique_ip_suffix = random.randint(100, 254)  # More random unique IP
        camera_data = {
            "name": f"Test Camera {timestamp}",
            "camera_type": "ip",
            "ip_address": f"10.0.{unique_ip_suffix}.{random.randint(1, 254)}",  # More unique IP
            "rtsp_url": f"rtsp://10.0.{unique_ip_suffix}.{random.randint(1, 254)}:554/stream",
            "username": "admin",
            "password": "admin123",
            "enabled": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/cameras/",
                json=camera_data,
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 201:
                camera = response.json()
                camera_id = camera.get('id')
                self.created_resources['cameras'].append(camera_id)
                self.record_test("Create Camera (POST /api/cameras/)", True,
                               f"Created camera ID: {camera_id}")
            else:
                self.record_test("Create Camera (POST /api/cameras/)", False,
                               f"Status: {response.status_code}, Response: {response.text}")
                return
        except Exception as e:
            self.record_test("Create Camera (POST /api/cameras/)", False, str(e))
            return
            
        # Test: Get single camera
        try:
            response = requests.get(
                f"{self.base_url}/api/cameras/{camera_id}",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                camera = response.json()
                self.record_test("Get Single Camera (GET /api/cameras/<id>)", True,
                               f"Camera: {camera.get('name')}")
            else:
                self.record_test("Get Single Camera (GET /api/cameras/<id>)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Get Single Camera (GET /api/cameras/<id>)", False, str(e))
            
        # Test: Update camera
        update_data = {
            "name": f"Updated Camera {datetime.now().strftime('%H%M%S')}",
            "enabled": False
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/api/cameras/{camera_id}",
                json=update_data,
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                camera = response.json()
                self.record_test("Update Camera (PUT /api/cameras/<id>)", True,
                               f"Updated to: {camera.get('name')}")
            else:
                self.record_test("Update Camera (PUT /api/cameras/<id>)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Update Camera (PUT /api/cameras/<id>)", False, str(e))
            
        # Test: Test camera connection
        try:
            response = requests.post(
                f"{self.base_url}/api/cameras/{camera_id}/test",
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code in [200, 202]:
                result = response.json()
                self.record_test("Test Camera (POST /api/cameras/<id>/test)", True,
                               f"Status: {result.get('status', 'queued')}")
            else:
                self.record_test("Test Camera (POST /api/cameras/<id>/test)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Test Camera (POST /api/cameras/<id>/test)", False, str(e))
            
        # Test: Get camera status
        try:
            response = requests.get(
                f"{self.base_url}/api/cameras/status",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                status = response.json()
                self.record_test("Get Camera Status (GET /api/cameras/status)", True,
                               f"Total: {status.get('total_cameras', 0)}")
            else:
                self.record_test("Get Camera Status (GET /api/cameras/status)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Get Camera Status (GET /api/cameras/status)", False, str(e))
            
    # ============================================================================
    # ALERT MANAGEMENT TESTS
    # ============================================================================
    
    def test_alert_operations(self):
        """Test all alert operations"""
        self.print_header("TESTING ALERT MANAGEMENT")
        
        # Test: Get all alerts
        try:
            response = requests.get(
                f"{self.base_url}/api/alerts/",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                alerts = response.json()
                self.record_test("Get All Alerts (GET /api/alerts/)", True,
                               f"Found {len(alerts)} alerts")
            else:
                self.record_test("Get All Alerts (GET /api/alerts/)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Get All Alerts (GET /api/alerts/)", False, str(e))
            
        # Test: Create new alert (with lower severity to avoid Celery trigger)
        alert_data = {
            "alert_type": "device_down",
            "severity": "info",  # Use 'info' instead of 'critical' to avoid Celery notification
            "message": f"Test alert created at {datetime.now().isoformat()}",
            "source": "test_suite"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/alerts/",
                json=alert_data,
                headers=self.get_headers(),
                timeout=15  # Increased timeout for alert creation
            )
            
            if response.status_code == 201:
                alert = response.json()
                alert_id = alert.get('id')
                self.created_resources['alerts'].append(alert_id)
                self.record_test("Create Alert (POST /api/alerts/)", True,
                               f"Created alert ID: {alert_id}")
            else:
                self.record_test("Create Alert (POST /api/alerts/)", False,
                               f"Status: {response.status_code}, Response: {response.text}")
                return
        except Exception as e:
            self.record_test("Create Alert (POST /api/alerts/)", False, str(e))
            return
            
        # Test: Get single alert
        try:
            response = requests.get(
                f"{self.base_url}/api/alerts/{alert_id}",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                alert = response.json()
                self.record_test("Get Single Alert (GET /api/alerts/<id>)", True,
                               f"Alert type: {alert.get('alert_type')}")
            else:
                self.record_test("Get Single Alert (GET /api/alerts/<id>)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Get Single Alert (GET /api/alerts/<id>)", False, str(e))
            
        # Test: Acknowledge single alert
        try:
            response = requests.post(
                f"{self.base_url}/api/alerts/{alert_id}/acknowledge",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                self.record_test("Acknowledge Alert (POST /api/alerts/<id>/acknowledge)", True,
                               "Alert acknowledged")
            else:
                self.record_test("Acknowledge Alert (POST /api/alerts/<id>/acknowledge)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Acknowledge Alert (POST /api/alerts/<id>/acknowledge)", False, str(e))
            
        # Test: Get alert summary
        try:
            response = requests.get(
                f"{self.base_url}/api/alerts/summary",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                summary = response.json()
                self.record_test("Get Alert Summary (GET /api/alerts/summary)", True,
                               f"Total: {summary.get('total_alerts', 0)}")
            else:
                self.record_test("Get Alert Summary (GET /api/alerts/summary)", False,
                               f"Status: {response.status_code}")
        except Exception as e:
            self.record_test("Get Alert Summary (GET /api/alerts/summary)", False, str(e))
            
        # Test: Acknowledge all alerts
        try:
            response = requests.post(
                f"{self.base_url}/api/alerts/acknowledge-all",
                json={},  # Send empty JSON body
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                self.record_test("Acknowledge All Alerts (POST /api/alerts/acknowledge-all)", True,
                               f"Acknowledged {result.get('count', 0)} alerts")
            else:
                self.record_test("Acknowledge All Alerts (POST /api/alerts/acknowledge-all)", False,
                               f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.record_test("Acknowledge All Alerts (POST /api/alerts/acknowledge-all)", False, str(e))
            
    # ============================================================================
    # CLEANUP & DELETION TESTS
    # ============================================================================
    
    def test_cleanup(self):
        """Clean up created test resources"""
        self.print_header("CLEANING UP TEST RESOURCES")
        
        # Delete test cameras
        for camera_id in self.created_resources['cameras']:
            try:
                response = requests.delete(
                    f"{self.base_url}/api/cameras/{camera_id}",
                    headers=self.get_headers(),
                    timeout=5
                )
                
                if response.status_code == 200:
                    self.record_test(f"Delete Camera ID {camera_id} (DELETE /api/cameras/<id>)", 
                                   True, "Deleted successfully")
                else:
                    self.record_test(f"Delete Camera ID {camera_id} (DELETE /api/cameras/<id>)", 
                                   False, f"Status: {response.status_code}")
            except Exception as e:
                self.record_test(f"Delete Camera ID {camera_id}", False, str(e))
                
        # Delete test devices
        for device_id in self.created_resources['devices']:
            try:
                response = requests.delete(
                    f"{self.base_url}/api/devices/{device_id}",
                    headers=self.get_headers(),
                    timeout=5
                )
                
                if response.status_code == 200:
                    self.record_test(f"Delete Device ID {device_id} (DELETE /api/devices/<id>)", 
                                   True, "Deleted successfully")
                else:
                    self.record_test(f"Delete Device ID {device_id} (DELETE /api/devices/<id>)", 
                                   False, f"Status: {response.status_code}")
            except Exception as e:
                self.record_test(f"Delete Device ID {device_id}", False, str(e))
                
    # ============================================================================
    # ERROR HANDLING TESTS
    # ============================================================================
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        self.print_header("TESTING ERROR HANDLING")
        
        # Test: Access without authentication
        try:
            response = requests.get(
                f"{self.base_url}/api/devices/",
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 401:
                self.record_test("Unauthorized Access", True, "Correctly rejected")
            else:
                self.record_test("Unauthorized Access", False,
                               f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.record_test("Unauthorized Access", False, str(e))
            
        # Test: Non-existent device
        try:
            response = requests.get(
                f"{self.base_url}/api/devices/99999",
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 404:
                self.record_test("Non-existent Device", True, "Correctly returned 404")
            else:
                self.record_test("Non-existent Device", False,
                               f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.record_test("Non-existent Device", False, str(e))
            
        # Test: Invalid device creation (missing required fields)
        try:
            response = requests.post(
                f"{self.base_url}/api/devices/",
                json={"name": "Incomplete Device"},
                headers=self.get_headers(),
                timeout=5
            )
            
            if response.status_code == 400:
                self.record_test("Invalid Device Creation", True, "Correctly rejected")
            else:
                self.record_test("Invalid Device Creation", False,
                               f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.record_test("Invalid Device Creation", False, str(e))
            
    # ============================================================================
    # MAIN TEST RUNNER
    # ============================================================================
    
    def run_all_tests(self):
        """Run all test suites"""
        start_time = time.time()
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
        print(f"{'DEVICE MONITORING SYSTEM - COMPREHENSIVE TEST SUITE':^80}")
        print(f"{'=' * 80}{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Base URL: {self.base_url}")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}\n")
        
        # Run test suites in order
        self.test_health_endpoints()
        
        # Login is required for other tests
        if not self.test_login():
            self.print_error("Login failed! Cannot continue with authenticated tests.")
            self.print_summary()
            return False
            
        self.test_invalid_login()
        self.test_token_refresh()
        self.test_get_profile()
        self.test_get_users()
        
        self.test_device_operations()
        self.test_camera_operations()
        self.test_alert_operations()
        
        self.test_error_handling()
        
        # Cleanup
        self.test_cleanup()
        
        # Print summary
        end_time = time.time()
        duration = end_time - start_time
        self.print_summary(duration)
        
        return True
        
    def print_summary(self, duration: float = 0):
        """Print test results summary"""
        self.print_header("TEST RESULTS SUMMARY")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for _, passed, _ in self.test_results if passed)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"{Fore.CYAN}Total Tests: {total_tests}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Passed: {passed_tests}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {failed_tests}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Success Rate: {success_rate:.2f}%{Style.RESET_ALL}")
        
        if duration > 0:
            print(f"{Fore.CYAN}Duration: {duration:.2f} seconds{Style.RESET_ALL}")
            
        # Print failed tests details
        if failed_tests > 0:
            print(f"\n{Fore.RED}{Style.BRIGHT}Failed Tests:{Style.RESET_ALL}")
            for test_name, passed, details in self.test_results:
                if not passed:
                    print(f"{Fore.RED}  ✗ {test_name}: {details}{Style.RESET_ALL}")
                    
        # Overall status
        print(f"\n{'=' * 80}")
        if failed_tests == 0:
            print(f"{Fore.GREEN}{Style.BRIGHT}{'ALL TESTS PASSED! ✓':^80}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}{'SOME TESTS FAILED! ✗':^80}{Style.RESET_ALL}")
        print(f"{'=' * 80}\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Comprehensive test suite for Device Monitoring System')
    parser.add_argument('--url', default='http://localhost:5000',
                       help='Base URL of the application (default: http://localhost:5000)')
    parser.add_argument('--username', default='admin',
                       help='Username for authentication (default: admin)')
    parser.add_argument('--password', default='Admin@123',
                       help='Password for authentication (default: Admin@123)')
    
    args = parser.parse_args()
    
    # Check if colorama is available
    try:
        from colorama import init, Fore, Style
    except ImportError:
        print("Warning: colorama not installed. Install it for colored output:")
        print("  pip install colorama")
        print("\nContinuing with plain text output...\n")
        
    # Run tests
    tester = DeviceMonitoringTester(base_url=args.url)
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
