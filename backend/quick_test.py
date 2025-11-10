import requests
import sys

BASE_URL = "http://localhost:5000/api"

print("Testing Settings and Logout Issues...\n")
print("="*60)

# Test 1: Login
print("\n1. Testing Login...")
try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "admin", "password": "Admin@123"},
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"✓ Login successful")
        print(f"  Token: {token[:50]}...")
    else:
        print(f"✗ Login failed: {response.status_code}")
        print(f"  Response: {response.text}")
        sys.exit(1)
except Exception as e:
    print(f"✗ Login error: {str(e)}")
    sys.exit(1)

headers = {"Authorization": f"Bearer {token}"}

# Test 2: Check Settings Endpoint
print("\n2. Testing Settings Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/settings/", headers=headers, timeout=5)
    if response.status_code == 200:
        print(f"✓ Settings endpoint working!")
        print(f"  Response: {response.json()}")
    else:
        print(f"✗ Settings failed: {response.status_code}")
        print(f"  Response: {response.text}")
except Exception as e:
    print(f"✗ Settings error: {str(e)}")

# Test 3: Check Profile (for logout page)
print("\n3. Testing Profile Endpoint (used by settings page)...")
try:
    response = requests.get(f"{BASE_URL}/auth/profile", headers=headers, timeout=5)
    if response.status_code == 200:
        profile = response.json()
        print(f"✓ Profile endpoint working!")
        print(f"  User: {profile['username']} ({profile['role']})")
    else:
        print(f"✗ Profile failed: {response.status_code}")
        print(f"  Response: {response.text}")
except Exception as e:
    print(f"✗ Profile error: {str(e)}")

# Test 4: List all registered routes
print("\n4. Checking Registered Routes...")
try:
    response = requests.get(f"http://localhost:5000/api/health", timeout=5)
    if response.status_code == 200:
        print(f"✓ API is accessible")
    else:
        print(f"? Health check returned: {response.status_code}")
except Exception as e:
    print(f"✗ Health check error: {str(e)}")

print("\n" + "="*60)
print("Test Complete!")
print("\nIf you see errors above, please share them so I can fix the issue.")
print("="*60)
