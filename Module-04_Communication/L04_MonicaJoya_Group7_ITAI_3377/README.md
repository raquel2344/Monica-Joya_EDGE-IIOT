Lab 04 Conceptual Design of an IIoT Sensor Network & Protocol Experimentation

**Course:** ITAI 3377 – IoT & Edge Computing  
**Date:** February 18, 2026

## Team Members
- Monica Joya  
- Cassy Cormier  
- Kolapo Mogaji  
- Sufyan Rafiq

---

## Project Overview

This project simulates an Industrial Internet of Things (IIoT) sensor network using three communication protocols: **MQTT**, **CoAP**, and **OPC UA**. Each protocol generates random temperature and humidity sensor data every second. A real-time visualization script subscribes to the MQTT data stream and plots it using Matplotlib.

---

## Project Structure

```
iiot_simulation/
├── README.md
├── mqtt_sensor_simulation.py
├── coap_sensor_simulation.py
├── opcua_sensor_simulation.py
├── data_visualization.py
├── visualizations/
│   ├── mqtt_visualization.png
│   ├── coap_visualization.png
│   ├── opcua_visualization.png
│   └── visualization_demo.mp4
└── comparison_report.pdf
```

---

## Setup Instructions

### 1. Create and Activate a Virtual Environment

```bash
cd iiot_simulation
python -m venv venv
```

**Activate:**

- macOS/Linux: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

### 2. Install Python Dependencies

```bash
pip install pandas numpy paho-mqtt aiocoap asyncua matplotlib
```

### 3. Install Mosquitto MQTT Broker

Download and install from [mosquitto.org](https://mosquitto.org/download/).

---

## How to Run

### Step 1 – Start the MQTT Broker

Open a terminal and run:

```bash
mosquitto
```

### Step 2 – Run Sensor Simulations

Open separate terminal windows (with the virtual environment activated) and run:

```bash
python mqtt_sensor_simulation.py
python coap_sensor_simulation.py
python opcua_sensor_simulation.py
```

### Step 3 – Run the Data Visualization

```bash
python data_visualization.py
```

This opens a live-updating chart showing temperature and humidity data coming from the MQTT sensor simulation.

---

## Protocols Used

| Protocol | Transport | Use Case |
|----------|-----------|----------|
| MQTT | TCP (pub/sub) | Lightweight messaging for constrained devices |
| CoAP | UDP (request/response) | RESTful communication for low-power IoT |
| OPC UA | TCP (client/server) | Industrial automation and interoperability |

---

## Notes

- All simulations generate random temperature (20–25°C) and humidity (30–50%) values every second.
- The visualization script subscribes to the MQTT broker and plots the last 100 data points in real time.
- Ensure the virtual environment is activated before running any scripts.
