# Module 07: Real-Time AI Applications in IIoT and Edge

**Course:** ITAI 3377 - IoT & Edge Computing
**Student:** Monica Joya
**Term:** Spring 2026

---

## Overview

This module is where the course shifted from "what is edge AI" to "what does it have to do, and how fast does it have to do it." The L07 lab on Age of Information and reliability gave me the math behind it.

---

## What I Learned

Real time splits into three categories. Hard real time means missing a deadline equals system failure: emergency shutoff, autonomous vehicle braking, safety interlocks. Soft real time means missing a deadline degrades performance but does not break the system: streaming analytics, most quality control. Near real time means small delays are acceptable: dashboards, predictive maintenance alerts. The KPIs are latency, throughput, power, reliability, and the accuracy-versus-speed tradeoff. None of those metrics live alone. Pushing on one usually moves another.

Five core application areas, each with a concrete example I want to remember. Real-time monitoring uses sensors and TensorFlow Lite to flag overheating before a breakdown. Real-time control adjusts physical systems in the loop, like an oil refinery lowering valve pressure when a sensor detects a spike, preventing leaks and saving roughly $100,000 per incident. Predictive maintenance like GE Predix forecasts engine failures before a flight is grounded. Quality control like Tesla's automated visual inspection catches defects during assembly. Smart manufacturing like Bosch's predictive analytics dynamically adjusts assembly lines for a reported 10 percent productivity gain. Autonomous vehicles, smart cities, and traffic management all share the same shape: sensor in, AI decides, system acts, no human in the loop for the time-critical part.

Designing a real-time AI system is a checklist. Requirements with real numbers (latency under 10 ms, accuracy at 95 percent, scalability to N devices). Data collection with a designed answer for what happens when a sensor fails. Model development with lightweight architectures like MobileNet or TinyML, trained centrally and optimized through quantization, pruning, and knowledge distillation. Edge infrastructure (Raspberry Pi for cheap, Jetson when you need power) where moving inference from cloud to edge typically drops latency from 200 ms to 20 ms. Communication protocols matched to the timing budget: MQTT for lightweight messaging, OPC UA for industrial systems, DDS for real-time, 5G with Time Sensitive Networking for ultra-low latency.

Operations matter as much as design. Real-time pipelines stream sensor data straight to the AI, run inference on the edge device, and integrate the output back into actuators. Monitoring tracks model and device performance, with thresholds like 90 percent accuracy triggering retraining. CI/CD for edge AI means automated testing, over-the-air updates, version control for models, and rollback when an update fails. Real-time AI is not deploy-and-forget. The case study was a smart factory with edge computer vision on 20 cameras and Jetson devices, hitting 95 percent defect detection and a 30 percent waste reduction.

Explainable AI is the part I had thought least about before this module. Real-time AI making industrial decisions has to be interpretable, both to build trust with operators and to satisfy regulatory and safety requirements. LIME and SHAP work for complex models. Decision trees and linear models are transparent by construction. The tradeoff is accuracy versus interpretability. The practical answer is hybrid models with human-in-the-loop oversight.

The L07 lab was where this got concrete. The Farag paper splits IIoT traffic into two flows with different real-time requirements. AoI-oriented traffic is periodic monitoring data where the goal is to keep the controller's view of the system fresh. The metric is Age of Information, the time since the last received packet was generated. AoI is not the same as delay or throughput. The strategies that minimize delay do not necessarily minimize AoI. Deadline-oriented traffic is event-triggered data like emergency alarms that must arrive within a hard deadline or get dropped. The metric is Packet Loss Probability. The headline result is the tradeoff between them. You cannot freely minimize both at once. With high capture capability you can decrease AoI while keeping PLP low and let everyone transmit together. With low capture capability, increasing transmission probability decreases AoI only by sacrificing PLP, and the right move is scheduled access like round-robin instead of contention.

The Relay2 reading on Edge AI and Wi-Fi added a useful framing. Time-sensitive applications belong on the edge. Data-intensive applications belong in the cloud. They are complementary, not interchangeable. A real industrial system uses both.

---

## Insights

Real time is a system property, not a model property. Latency, reliability, and freshness are design constraints, not nice-to-haves. The Farag paper made it concrete because it forced me to reason about a tradeoff curve instead of optimizing one number.

The tradeoff mindset carries over. The AoI-versus-PLP tradeoff is the same shape as many other engineering decisions. Real systems are rarely about maximizing one metric. They are about picking the right point on the curve given the application's actual requirements.

This is where many earlier modules meet. Communication protocols connect to L04. Security implementation connects to Module 08. CI/CD for edge AI is going to matter when I come back to my ESP32-S3 portfolio idea. Module 07 is where the abstract ideas turn into actual design decisions.

---

## Resources

- Course Slides: ITAI 3377 Module 07 - Real-Time AI Applications in IIoT and Edge
- Farag, H., Ali, S. M., & Stefanovic, C. (2023). *On the Analysis of AoI-Reliability Tradeoff in Heterogeneous IIoT Networks.* arXiv:2311.13336v1.
- Jaber, S. (2024). *AI at the Edge: Technology Accelerated by Wi-Fi Services.* Wevolver and Relay2.
