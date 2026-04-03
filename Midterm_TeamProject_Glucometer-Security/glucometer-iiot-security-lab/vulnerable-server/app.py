"""
Glucometer IIoT Vulnerable Server
=================================
EDUCATIONAL PURPOSE ONLY - Contains intentional security vulnerabilities

This simulates a cloud backend for an AI-integrated glucometer system.
Vulnerabilities are marked with [VULN] comments.
"""

from fastapi import FastAPI, HTTPException, Query, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
import sqlite3
import random
import uvicorn

app = FastAPI(
    title="Glucometer Cloud API (Vulnerable)",
    description="Educational pen testing target - DO NOT USE IN PRODUCTION",
    version="1.0.0"
)

# [VULN V7] CORS Misconfiguration - allows any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # VULNERABLE: Should be specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [VULN V1] Hardcoded secrets - easily extractable
API_KEY = "glucometer-secret-key-12345"
JWT_SECRET = "super-secret-jwt-key"  # VULNERABLE: Weak, hardcoded secret
JWT_ALGORITHM = "HS256"

# [VULN] Hardcoded credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"  # VULNERABLE: Weak password

# Database setup
def init_db():
    conn = sqlite3.connect("glucometer.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            glucose_level REAL,
            timestamp TEXT,
            device_id TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            ssn TEXT,
            diagnosis TEXT
        )
    """)
    # Insert sample data
    cursor.execute("DELETE FROM readings")
    cursor.execute("DELETE FROM patients")
    for i in range(10):
        cursor.execute(
            "INSERT INTO readings (patient_id, glucose_level, timestamp, device_id) VALUES (?, ?, ?, ?)",
            (f"P{i}", random.uniform(70, 180), datetime.now().isoformat(), f"DEV{i}")
        )
    cursor.execute("INSERT INTO patients (name, ssn, diagnosis) VALUES (?, ?, ?)", 
                   ("John Doe", "123-45-6789", "Type 2 Diabetes"))
    cursor.execute("INSERT INTO patients (name, ssn, diagnosis) VALUES (?, ?, ?)", 
                   ("Jane Smith", "987-65-4321", "Pre-diabetic"))
    conn.commit()
    conn.close()

init_db()

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class GlucoseReading(BaseModel):
    patient_id: str
    glucose_level: float
    device_id: str

class AIRequest(BaseModel):
    glucose_value: float

# Helper functions
def create_token(username: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {
        "sub": username,
        "exp": expire,
        "role": "user"  # [VULN V3] Role in token can be manipulated
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception as e:
        # [VULN V6] Verbose error message leaks information
        raise HTTPException(status_code=401, detail=f"Token error: {str(e)}")

# Routes

@app.get("/")
def root():
    return {
        "service": "Glucometer Cloud API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": ["/api/login", "/api/readings", "/api/patients", "/api/predict"]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "database": "connected"}

@app.post("/api/login")
def login(request: LoginRequest):
    """
    [VULN V5] No rate limiting - can be brute forced
    [VULN] Timing attack possible - different response times
    """
    if request.username == ADMIN_USERNAME and request.password == ADMIN_PASSWORD:
        token = create_token(request.username)
        return {"access_token": token, "token_type": "bearer"}
    # [VULN V6] Reveals whether username or password is wrong
    if request.username != ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid username")
    raise HTTPException(status_code=401, detail="Invalid password")

@app.get("/api/readings")
def get_readings(patient_id: Optional[str] = Query(None)):
    """
    [VULN V4] SQL Injection - patient_id is not sanitized
    """
    conn = sqlite3.connect("glucometer.db")
    cursor = conn.cursor()
    
    if patient_id:
        # VULNERABLE: String concatenation allows SQL injection
        query = f"SELECT * FROM readings WHERE patient_id = '{patient_id}'"
        try:
            cursor.execute(query)
        except Exception as e:
            # [VULN V6] Leaks SQL error details
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    else:
        cursor.execute("SELECT * FROM readings")
    
    rows = cursor.fetchall()
    conn.close()
    
    return {
        "count": len(rows),
        "readings": [
            {"id": r[0], "patient_id": r[1], "glucose_level": r[2], "timestamp": r[3], "device_id": r[4]}
            for r in rows
        ]
    }

@app.get("/api/patients")
def get_patients(token: dict = Depends(verify_token)):
    """
    [VULN V3] Only checks token validity, not role
    Should require admin role but doesn't verify
    """
    conn = sqlite3.connect("glucometer.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    conn.close()
    
    # Returns sensitive PII including SSN
    return {
        "patients": [
            {"id": r[0], "name": r[1], "ssn": r[2], "diagnosis": r[3]}
            for r in rows
        ]
    }

@app.post("/api/readings")
def add_reading(reading: GlucoseReading, x_api_key: Optional[str] = Header(None)):
    """
    [VULN V1] API key check is weak
    [VULN V2] No input validation on glucose values
    """
    # Weak API key check
    if x_api_key != API_KEY:
        # [VULN V6] Reveals the expected header name
        raise HTTPException(status_code=403, detail="Invalid X-API-Key header")
    
    # [VULN V2] No validation - accepts any glucose value including impossible ones
    # Real glucose should be 20-600 mg/dL, but we accept anything
    
    conn = sqlite3.connect("glucometer.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO readings (patient_id, glucose_level, timestamp, device_id) VALUES (?, ?, ?, ?)",
        (reading.patient_id, reading.glucose_level, datetime.now().isoformat(), reading.device_id)
    )
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": "Reading added"}

@app.post("/api/predict")
def predict_glucose(request: AIRequest, x_api_key: Optional[str] = Header(None)):
    """
    Simulated AI model endpoint
    [VULN V2] No input validation - accepts adversarial inputs
    """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    glucose = request.glucose_value
    
    # [VULN] No bounds checking - adversarial inputs can manipulate predictions
    # A real model would be fooled by values outside training distribution
    
    if glucose < 0:
        # Adversarial input: negative glucose (impossible)
        prediction = "MODEL CONFUSED - Unexpected input"
        confidence = 0.1
    elif glucose > 1000:
        # Adversarial input: extremely high value
        prediction = "MODEL CONFUSED - Out of distribution"
        confidence = 0.2
    elif glucose < 70:
        prediction = "Hypoglycemia risk - Recommend eating"
        confidence = 0.85
    elif glucose > 180:
        prediction = "Hyperglycemia risk - Recommend insulin"
        confidence = 0.82
    else:
        prediction = "Normal range - No action needed"
        confidence = 0.95
    
    return {
        "input_glucose": glucose,
        "prediction": prediction,
        "confidence": confidence,
        "model_version": "LSTM-v1.0"
    }

@app.get("/api/debug")
def debug_info():
    """
    [VULN V6] Debug endpoint left enabled in production
    Leaks sensitive system information
    """
    return {
        "api_key_hint": API_KEY[:10] + "...",  # Partial key leak
        "jwt_algorithm": JWT_ALGORITHM,
        "database": "glucometer.db",
        "python_version": "3.x",
        "endpoints_count": 8
    }

if __name__ == "__main__":
    print("\n" + "="*60)
    print("GLUCOMETER VULNERABLE SERVER - EDUCATIONAL USE ONLY")
    print("="*60)
    print("Server starting on http://localhost:8080")
    print("This server contains INTENTIONAL vulnerabilities!")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8080)
