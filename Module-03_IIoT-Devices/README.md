# Module 03: IIoT Devices and Sensors

**Course:** ITAI 3377 - IoT & Edge Computing
**Student:** Monica Joya
**Term:** Spring 2026

---

## Overview

This module was about the physical hardware of IIoT: sensors, actuators, controllers, and edge gateways. Module 02 set up edge computing as a paradigm. Module 03 grounded it in real components. The graded work was A03, a case study analysis on edge-computing video analytics, and L03, a hands-on lab simulating sensor data collection in a virtual IIoT environment.

---

## What I Learned

IIoT hardware breaks down into four roles that work as a pipeline. Sensors collect data from the physical world. Actuators turn decisions into physical action. Controllers run the logic between them. Edge gateways aggregate, pre-process, and forward data upward. Once I saw IIoT as a four-stage pipeline, every product, paper, and architecture diagram in this field became easier to read.

The most common industrial sensors are temperature (equipment monitoring, HVAC, process control), pressure (pipeline leaks, hydraulics, pumps), and vibration (predictive maintenance, fault detection). The Ullo and Sinha review broadened that picture by splitting sensors into active (transmitting their own signal, like radar or LiDAR) and passive (measuring naturally occurring signals, like temperature probes). The same paper introduced the smart sensor concept, which is a sensor with AI built in that decides what is worth transmitting on its own.

Actuators convert energy into motion or force. Electric motors give rotation. Hydraulic and pneumatic actuators move heavy loads. Solenoids drive valves and locking mechanisms. They show up in valve control, motorized conveyors, and robotic arm positioning.

Controllers receive sensor data, run logic, and command actuators. PLCs are the rugged industrial workhorse. DCS systems coordinate plant-wide processes. Embedded controllers live inside individual IIoT devices. AI-driven controllers extend this with predictive maintenance, anomaly detection, and real-time quality control.

Edge gateways are the bridge between the physical hardware and the cloud. They aggregate data from many sensors, pre-process it locally to filter outliers and standardize units, and translate between local protocols like Modbus and cloud protocols like MQTT or CoAP. This was the section that connected most directly to Module 04, where we actually implemented those protocols in L04.

A03 was the Barthélemy et al. paper on the Liverpool, Australia smart city pilot. NVIDIA Jetson TX2 with GPU acceleration, paired with a Pycom LoPy 4 for LoRaWAN, in a waterproof IP67 case. YOLO V3 for object detection and SORT for tracking, processing about 20 frames per second. Twenty visual sensors deployed across the town center, fifteen on existing CCTV and five mobile. On the Oxford Town Center benchmark, the sensor reached 69 percent mean accuracy. In one outdoor day in Liverpool, 20,399 unique objects were detected and tracked. The key design point was that raw video never left the device. Only metadata went to the cloud. Privacy compliance built into the architecture, not bolted on after.

L03 took the conceptual material and made it tactile. We simulated sensor data collection and transmission in a virtual IIoT environment, generating sensor readings and routing them through the data pipeline that the slides described in theory.

---

## Insights

The pipeline view is the right view. Sensors, actuators, controllers, gateways. Once that mental model clicked, every architecture diagram in this field became easier to read.

Privacy can be an architectural choice. The Liverpool case showed that if you process video on the device and transmit only metadata, you do not need new privacy policies. The architecture handles compliance automatically. That pattern generalizes well beyond traffic monitoring.

A sensor with AI built in is a different category of device from a plain sensor. The smart sensor decides what is worth transmitting and what to ignore. That is edge intelligence applied to the smallest device in the pipeline.

---

## Resources

- Course Slides: ITAI 3377 Module 03 - IIoT Devices and Sensors
- Barthélemy, J., Verstaevel, N., Forehead, H., & Perez, P. (2019). *Edge-Computing Video Analytics for Real-Time Traffic Monitoring in a Smart City.* Sensors, 19(9), 2048. (A03 case study source)
- Ullo, S. L., & Sinha, G. R. (2021). *Advances in IoT and Smart Sensors for Remote Sensing and Agriculture Applications.* Remote Sensing, 13(13), 2585.
