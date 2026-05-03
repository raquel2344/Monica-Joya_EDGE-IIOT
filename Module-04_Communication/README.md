# Module 04: IIoT Communication and Networking

**Course:** ITAI 3377 - IoT & Edge Computing
**Student:** Monica Joya
**Term:** Spring 2026

---

## Overview

This module was about how IIoT devices actually talk to each other and to the cloud. Before this module, I thought of IIoT as sensors plus AI. Module 04 forced me to look at the network layer in between, which is what makes the rest of the system work. The graded work was A04 (reflective journal) and L04, the Group 7 hands-on project where we simulated an IIoT sensor network using MQTT, CoAP, and OPC UA.

---

## What I Learned

Networks are made of nodes (the devices), links (the connections), and protocols (the rules). Layering protocols means each layer handles one job, so changing one does not break the others. The IIoT question is which protocol fits a constrained device on an unreliable network.

The u-blox MQTT-SN paper made the answer concrete with a single comparison: a 12-byte "Hello World" message costs 26 bytes total over MQTT-SN, but 5,676 bytes over HTTPS. That is a factor of 473 versus a factor of 2. For a battery-powered sensor sending small messages all day, that compounds into years of battery life difference.

MQTT is the protocol I worked with most in L04. It uses a publish-subscribe model where clients publish to topics and other clients subscribe through a broker, never talking to each other directly. It has three QoS levels for delivery guarantees. It runs over TCP and uses text for topic names, which adds some overhead. MQTT-SN exists for very constrained devices, with topic aliasing, sleep modes, and no TCP/IP dependency.

CoAP is the main alternative for very constrained environments. It is RESTful, uses UDP instead of TCP, and supports observable resources where clients get pushed updates when something changes. It pairs well with 6LoWPAN. It wins on efficiency but has weaker congestion control and limited interoperability with non-CoAP devices.

OPC UA is the heavyweight. It exists because industrial systems need vendor interoperability and rich data semantics, not just byte efficiency. The thing I had not appreciated before reading the OPC Foundation document was that OPC UA does not just move bytes. It carries an object-oriented model of what the data means, with browsing, methods, and read/write semantics built in. It runs across PCs, embedded controllers, cloud servers, and PLCs. It supports message signing, X.509 certificate authentication, and auditing. In a SCADA or MES context, that means a robot from one vendor and a CNC from another can expose data in a model a third system can actually understand.

The protocol comparison from the AIMultiple article showed the range-rate tradeoff cleanly. Bluetooth and Zigbee are short-range and modest-rate. Wi-Fi is short-range and very fast. Cellular is long-range with variable rates. LoRaWAN and Sigfox are very long-range with very low rates. NFC is essentially touch-range. As range goes up, data rate goes down. Picking a protocol is mostly choosing where on that curve the application sits.

Security matters in IIoT for three reasons: more connected devices means more attack surface, the data is operationally sensitive, and a breach can cause physical harm or production shutdown, not just data leaks. The essential measures are encryption, authentication, access control, and continuous monitoring. The u-blox paper added an angle I had not considered: SSL/TLS adds about 6 KB of overhead per message, while MQTT-SN with private APN authentication keeps it around 26 bytes. On a power-constrained device, the security model is also a battery model.

5G and 6G provide bandwidth and latency that some IIoT use cases need to exist at all. URLLC targets latency low enough for autonomous vehicles and emergency-response sensors. Beamforming directs signal to the device. Massive MIMO uses many antennas in parallel. Millimeter waves open higher frequency bands at the cost of range. Together these give industrial real-time applications a viable cellular option.

---

## Insights

The protocol is a design decision, not a default. Before this module I would have picked MQTT for any IoT project without thinking. The numbers showed me that protocol choice has real consequences. MQTT for cloud-bound telemetry, CoAP for very constrained devices, OPC UA where vendor interoperability matters, lighter cellular protocols where the network is the constraint.

Security is not a feature you bolt on later. The 6 KB versus 26 bytes comparison reframed it for me. On a battery-powered device, the security choice is also an energy choice. It has to be planned with the protocol, not added after.

L04 made the concepts concrete. Implementing MQTT, CoAP, and OPC UA side by side gave me three protocols I now have actual hands-on memory of, not just definitions.

---

## Resources

- Course Slides: ITAI 3377 Module 04 - IIoT Communication and Networking
- u-blox / Hayes, N. *Solving the complexity of communicating between IoT devices and the enterprise.* Whitepaper on MQTT and MQTT-SN.
- OPC Foundation. *Unified Architecture.* opcfoundation.org/about/opc-technologies/opc-ua
- Dilmegani, C. (2024). *Top 9 IoT Communication Protocols & Their Features.* AIMultiple Research.
- Verma, N., Singh, S., & Prasad, D. (2021). *A Review on existing IoT Architecture and Communication Protocols used in Healthcare Monitoring System.* J. Inst. Eng. India Ser. B, 103(1), 245–257.
