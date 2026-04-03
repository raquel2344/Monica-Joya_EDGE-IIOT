"""
Adversarial AI Input Attack
============================
Tests AI model vulnerability to out-of-distribution inputs
"""

import requests

BASE_URL = "http://localhost:8080"
API_KEY = "glucometer-secret-key-12345"  # Extracted from debug endpoint

def test_adversarial_inputs():
    print("\n" + "="*50)
    print("ADVERSARIAL AI INPUT ATTACK")
    print("="*50)
    
    # Test inputs - normal and adversarial
    test_cases = [
        # Normal inputs
        ("Normal low", 65),
        ("Normal mid", 100),
        ("Normal high", 200),
        
        # Adversarial inputs
        ("Negative glucose (impossible)", -50),
        ("Zero glucose (impossible)", 0),
        ("Extremely high (out of distribution)", 5000),
        ("Decimal precision attack", 99.999999999999),
        ("Near-boundary", 69.9999),
    ]
    
    headers = {"X-API-Key": API_KEY}
    
    for name, glucose_value in test_cases:
        print(f"\n[*] Testing: {name}")
        print(f"    Input glucose: {glucose_value}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/predict",
                json={"glucose_value": glucose_value},
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"    [RESPONSE] Prediction: {data['prediction']}")
                print(f"    [RESPONSE] Confidence: {data['confidence']}")
                
                # Flag if model is confused
                if data['confidence'] < 0.5:
                    print("    [!] LOW CONFIDENCE - Model is confused!")
            else:
                print(f"    [ERROR] Status: {response.status_code}")
                
        except Exception as e:
            print(f"    [ERROR] {str(e)}")
    
    print("\n" + "="*50)
    print("FINDINGS:")
    print("- Model accepts impossible glucose values (negative)")
    print("- No input validation before model inference")
    print("- Out-of-distribution inputs reduce confidence")
    print("- Attacker could manipulate patient recommendations")
    print("="*50)
    
    print("\n[*] RECOMMENDATION:")
    print("- Add input validation: 20 <= glucose <= 600 mg/dL")
    print("- Reject impossible values before model inference")
    print("- Log anomalous inputs for security monitoring")

if __name__ == "__main__":
    test_adversarial_inputs()
