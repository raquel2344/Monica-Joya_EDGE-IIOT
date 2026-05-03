# Module 02: Foundations of Edge Computing and AI

**Course:** ITAI 3377 - IoT & Edge Computing
**Student:** Monica Joya
**Term:** Spring 2026

---

## Overview

This module was where edge computing stopped being a buzzword for me and started being a real architecture. The hands-on work was L02, the MNIST edge deployment lab, my first time taking a model trained in the cloud, compressing it, and running it on a simulated edge device.

---

## What I Learned

Edge computing matters for four reasons: latency, bandwidth, security, and scalability. The latency one became real for me through the IEEE survey's example of an emergency machine stop, where a cloud round trip is too slow to prevent injury. Bandwidth matters because smart factory equipment can generate gigabytes of sensor data per second, and you cannot ship all of that to the cloud without serious cost and delay. Security improves because data closer to its source has fewer chances to leak in transit. Scalability matters because the world is heading for 25 billion IoT devices by 2030, and cloud-only architectures cannot handle that.

The basic three-layer architecture is edge, fog, cloud. The IEEE survey took it further and split the edge into Far-Edge (millisecond decisions next to sensors), Mid-Edge (gateways doing seconds-to-minutes analysis), and Near-Edge (regional servers doing hours-level optimization). The cloud handles day-level decisions. The point is that different decisions belong at different layers, matched to their time budget.

The Liverpool smart city project was the case study that made this concrete. NVIDIA Jetson TX2 sensors running YOLO V3 and SORT, twenty units installed using existing CCTV systems, 69 percent pedestrian detection accuracy at 19.57 frames per second. The privacy point stood out as much as the performance: because inference happened on the device, no raw video ever left the camera. Only metadata was transmitted. That is privacy by architecture, stronger than any encryption scheme.

AI at the edge means deploying models directly on local devices for real-time decisions. The benefits are speed, lower bandwidth, privacy, adaptive learning, and resilience when the network drops. The challenges are limited device computing power and a bigger attack surface. The slides specifically called out Zero Trust, AI-based anomaly detection on IoT networks, and federated learning as the security responses.

ML at the edge handles predictive maintenance and surveillance. DL at the edge handles image recognition and speech, but it requires optimized models. TensorFlow Lite and TinyML are the frameworks that make DL on edge devices possible. That is exactly what I did in L02: trained a CNN on MNIST in full TensorFlow, then converted to TFLite to fit on a simulated edge device.

The Forbes article gave me the analogy I keep using. If IoT is the nervous system, AIoT is the brain. IoT connects the dots, AIoT draws the picture. The IBM article added the distinction between edge AI (one device making local decisions) and distributed AI (many edge devices coordinated together at scale).

---

## Insights

Different decisions belong at different layers. Edge computing is not just faster cloud computing. It is a way of placing each decision where its time budget can actually be met.

Privacy by architecture beats privacy by policy. If raw video never leaves the camera, there is nothing to intercept. The system cannot betray data it never had.

L02 was the smallest working example of every concept in the module. Train in the cloud with full resources, compress, push to a constrained device, run inference there. Every more complex case I read about, autonomous vehicles, surveillance, predictive maintenance, follows the same shape.

---

## Resources

- Course Slides: ITAI 3377 Module 02 - Foundations of Edge Computing and AI
- Qiu, T., Chi, J., Zhou, X., Ning, Z., Atiquzzaman, M., & Wu, D. O. (2020). *Edge Computing in Industrial Internet of Things: Architecture, Advances and Challenges.* IEEE Communications Surveys & Tutorials, 22(4), 2462-2488.
- IBM. *What is edge AI?* https://www.ibm.com/topics/edge-ai
- Manthena, P. R. (2024, May 1). *What Companies Should Know About The Rise Of AIoT.* Forbes.
- Boesch, G. (2023). *Artificial Intelligence of Things (AIoT) in 2024.* Viso.ai. https://viso.ai/edge-ai/artificial-intelligence-of-things-aiot
- Companion lab in this folder: L02 - MNIST Edge AI Deployment (`MINST_Edge_repo/`)
