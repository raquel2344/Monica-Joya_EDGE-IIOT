# Module 08: Cybersecurity for AI in IIoT and Edge

**Course:** ITAI 3377 - IoT & Edge Computing
**Student:** Monica Joya
**Term:** Spring 2026

---

## Overview

This is the module that finally made every other module feel less abstract. It forced me to look at sensors, communication, preprocessing, real-time analytics, and generative AI through one question: how does it get attacked, and what do you do about it. This was also the module my team built our Midterm project around, a cybersecurity plan and penetration testing simulation for an AI-integrated glucometer IIoT system. The deliverable scored 95 out of 100.

---

## What I Learned

IIoT vulnerabilities live at five layers. Device level: weak default configurations, no secure boot, insufficient authentication, limited compute, physical access risks. Real attacks here include device hijacking (taking control without changing basic functionality, hard to detect, and once one device is compromised it spreads) and BrickerBot-style permanent denial of service that damages firmware so the device has to be replaced. Network level: insecure protocols, man in the middle, denial of service, poor segmentation. Data level: integrity, privacy, encryption, storage, and in-transit vulnerabilities. Application level: insecure APIs, insufficient input validation, outdated software, improper access controls, and vulnerabilities in the AI and ML models themselves. Human factor: lack of awareness, insider threats, social engineering, misconfiguration, weak policies. The most secure system fails if a person hands over a password.

Best practices fall into seven categories I now use as a checklist. Secure by design with secure boot using cryptographic code signing so a device only runs trusted code. The UK PSTI Act, which became the world's first IoT security law on April 29, 2024, takes the same position from the regulatory side, requiring manufacturers to ban universal default passwords, publish vulnerability disclosure points, and state security update timelines. Authentication and access control with MFA, role-based access, regular audits, and mutual authentication. Encryption and data protection through end-to-end encryption, data at rest, secure key management, and data minimization, with the GlobalPlatform Secure Channel Protocol filling the gap for constrained NB-IoT devices that cannot rely on TLS. Network security through segmentation, firewalls, intrusion detection, and VPN with MFA for remote access. The joint CISA, FBI, NSA, and UK NCSC advisory about pro-Russia hacktivist attacks on water and wastewater facilities specifically recommended disconnecting internet-exposed HMIs and requiring VPN with MFA for any remote access. Secure software development with penetration testing, secure coding, and patch management. Physical security through tamper-evident seals, environmental controls, and secure disposal. Security monitoring through SIEM, an actual incident response plan, drills, and post-incident analysis.

AI introduces its own attack surface. Training data has to be protected through anonymization, synthetic data generation, secure collection and storage, and data poisoning prevention. Data poisoning corrupts training data so the model learns the wrong thing, hard to detect and hard to undo. AI decision integrity has to handle adversarial inputs designed to trick the model even when the data is clean. And ethically, an AI making industrial decisions has to be transparent enough that humans can audit it, especially when the decision affects safety.

Risk assessment uses NIST RMF, ISO 31000, FAIR, and OCTAVE. Threat modeling uses STRIDE, attack trees, and data flow diagrams, plus AI-specific threat models. The five mitigation strategies are simple but useful: acceptance (decide it is small enough to live with), avoidance (do not do the thing), transfer (insurance, third-party hosting, contracts), reduction (add controls), and a documented risk treatment plan combining the above. Risk management is continuous, reassessed regularly, integrated into DevSecOps.

Two case studies set the pattern. Stuxnet targeted Iran's nuclear centrifuges by modifying PLC code while feeding fake "everything is normal" data back to operators. The lesson is that an attacker who reaches the control layer can cause physical damage that looks invisible until the equipment fails. Mirai built a botnet from default-password IoT devices and launched one of the largest DDoS attacks ever recorded. The lesson is that a fleet of cheap unsecured devices is itself a weapon. Manufacturing has been the most attacked industry for three straight years at 25.7 percent of all cyberattacks, with malware accounting for 45 percent of incidents. The reasons are tight IT/OT integration, low tolerance for downtime which makes ransomware especially effective, and a long tail of legacy equipment never designed to be networked.

Future trends worth watching: quantum-resistant cryptography because today's encryption falls to quantum eventually, AI-driven security automation to defend the AI itself, edge AI for real-time threat detection on the device, blockchain for tamper-evident logs and decentralized identity, and Zero Trust architecture where you never trust and always verify even inside the perimeter.

---

## Insights

The module gave me a complete blueprint for the Midterm. Device threats (the glucometer hardware), network threats (the device-to-cloud path), data threats (patient health information), application threats (the AI model interpreting readings), and human factor threats (clinician workflows). STRIDE for threat modeling. NIST-aligned risk treatment plan. Penetration test simulation as practical proof. We worked faster because we were filling in a structure, not starting from a blank page.

The regulatory picture is catching up. The UK PSTI Act and the GlobalPlatform Secure Channel Protocol changed my view. The era of shipping insecure IoT devices and hoping nobody notices is closing fast. Cybersecurity skills in IIoT are going to be a baseline expectation.

The pro-Russia hacktivist advisory was the most uncomfortable reading in the module. Not because the techniques were sophisticated, but because the targets were water treatment and food and agriculture facilities in real towns. Maxed-out set points, alarms turned off, operators locked out. That is the gap between IIoT security as a course topic and IIoT security as a thing that affects whether people can drink the water.

---

## Resources

- Course Slides: ITAI 3377 Module 08 - Cybersecurity for AI in IIoT and Edge
- CISA, FBI, NSA, EPA, DOE, USDA, FDA, Multi-State ISAC, Canadian Centre for Cyber Security, & UK NCSC. (2024, May 2). *Defending OT Operations Against Ongoing Pro-Russia Hacktivist Activity.*
- GlobalPlatform. (2024). *Secure Channel Protocol for constrained NB-IoT devices.*
- UK Department for Science, Innovation and Technology. (2024, April 29). *Product Security and Telecommunications Infrastructure (PSTI) Act 2022.*
- Alvarez, M. (2024). *Manufacturing Is #1 in Cyber Attacks for Third Straight Year.* IndustryWeek.
- Rambus. (n.d.). *Industrial IoT: Threats and Countermeasures.*
