import requests
import json

# Test settings endpoints
BASE_URL = "http://localhost:5000/api"

def test_settings():
    """Test the settings endpoint"""
    
    # First, login as admin to get token
    print("1. Logging in as admin...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "admin", "password": "Admin@123"}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return
    
    token = login_response.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Login successful")
    
    # Test GET /api/settings
    print("\n2. Getting settings...")
    get_response = requests.get(f"{BASE_URL}/settings/", headers=headers)
    
    if get_response.status_code == 200:
        print("✓ Settings retrieved successfully:")
        print(json.dumps(get_response.json(), indent=2))
    else:
        print(f"❌ Failed to get settings: {get_response.status_code}")
        print(get_response.text)
        return
    
    # Test PUT /api/settings
    print("\n3. Updating settings...")
    update_data = {
        "poll_interval": 90,
        "alert_email_from": "test@example.com",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587
    }
    
    put_response = requests.put(
        f"{BASE_URL}/settings/",
        headers=headers,
        json=update_data
    )
    
    if put_response.status_code == 200:
        print("✓ Settings updated successfully:")
        print(json.dumps(put_response.json(), indent=2))
    else:
        print(f"❌ Failed to update settings: {put_response.status_code}")
        print(put_response.text)
        return
    
    # Verify the update
    print("\n4. Verifying update...")
    verify_response = requests.get(f"{BASE_URL}/settings/", headers=headers)
    
    if verify_response.status_code == 200:
        settings = verify_response.json()
        if settings['poll_interval'] == 90:
            print("✓ Update verified successfully")
        else:
            print("❌ Update verification failed - poll_interval doesn't match")
    else:
        print(f"❌ Failed to verify: {verify_response.status_code}")
    
    print("\n" + "="*50)
    print("✓ All settings tests passed!")
    print("="*50)

if __name__ == "__main__":
    try:
        test_settings()
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
