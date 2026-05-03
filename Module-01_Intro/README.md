# Module 01: AI in Edge and IoT Devices

**Course:** ITAI 3377 - IoT & Edge Computing
**Student:** Monica Joya
**Term:** Spring 2026

---

## Overview

This is where the course started. Module 01 was the introduction to everything that came after, and looking back from where I am now, it lined up the four big ideas that the rest of the semester would unpack one at a time: edge computing, the Industrial Internet of Things, 5/6G networks for real-time AI, and the impact of AI across industries.

Module 01 had two parts. The first was the course introduction deck, which framed the conceptual landscape. The second was a separate deck on open source tools, walking through Node-RED, ThingsBoard, Eclipse Mosquitto, Docker, Edge Impulse, and GitHub. Those tools would not be theoretical for long. By Module 04 I was hands-on with Mosquitto and ThingsBoard in a real lab, and GitHub was the backbone of every assignment from then on.

This README captures both the framing and the foreshadowing. It is the most introductory of all my module READMEs because the module itself was an introduction.

---

## What I Learned

### Edge vs Cloud Computing

The first conceptual distinction in the course was simple but important. Cloud computing means processing data on remote servers, used in applications where large-scale processing is required. Edge computing means processing data closer to where it is generated, which reduces latency and bandwidth requirements and makes real-time processing possible.

That two-line definition does not seem like much, but it is the seed of everything else in the course. Every later module asked some version of the question, where should this decision happen, and how soon does it need to be made. The answer always traced back to this first cut between cloud and edge.

### IoT vs IIoT

The second distinction was sharper than I expected. IoT and IIoT sound similar, but they are aimed at different worlds.

IoT, the Internet of Things, is the consumer-facing version. It connects everyday objects to the internet to make life more convenient. The examples in the slides were Amazon Echo, Google Nest, smartwatches, Fitbit. The focus is convenience, efficiency, and automation in everyday life.

IIoT, the Industrial Internet of Things, is the industry-facing version. It connects machines, sensors, and control systems in factories, energy grids, and other industrial settings. The examples were automated assembly lines, robotic arms, and temperature, pressure, and vibration sensors in manufacturing plants. The focus is operational efficiency, reliability, productivity, and reduced downtime.

The distinction matters because the constraints are different. A consumer wearable can tolerate a missed reading or a delayed response. An industrial vibration sensor on a turbine probably cannot. That is why edge computing matters more in IIoT than in regular IoT, and it is why this course is specifically about IIoT and edge, not IoT in general.

### Why Edge and IIoT Matter in Modern Industries

The slides framed the value of combining edge with IIoT in three ways: real-time data processing, improved operational efficiency, and reduced downtime.

Real-time processing means decisions can happen as data arrives, rather than after a round trip to the cloud. Operational efficiency comes from predictive maintenance, asset tracking, and remote equipment monitoring, all of which require continuous local awareness. Reduced downtime comes from being able to predict and prevent failures rather than just respond to them.

These three benefits show up again and again in later modules. Module 06 went deep on AI analytics. Module 07 was specifically about real-time AI. Each one was a more detailed answer to a question that Module 01 had already raised at the headline level.

### 5/6G Networks for Real-Time AI

The slides introduced 5G and 6G as the network layer that makes real-time AI at the edge actually possible. The two characteristics that matter are high-speed connectivity and low latency. Without those, the rest of the architecture cannot meet its real-time goals.

The slides also flagged the challenges. Network congestion, hardware limitations, and network security are all real problems, and the solutions involve faster hardware, efficient routing protocols, and security measures like firewalls and intrusion detection systems. Connectivity is not free or automatic. It has to be engineered.

I did not realize at the time how much this would matter for Module 04, where the entire focus was communication protocols and how IIoT systems actually move data around. Module 01 set up the why. Module 04 went into the how.

### AI's Impact Across Industries

The third major theme of the course introduction was how AI transforms industries. The slides used three examples: manufacturing, energy, and healthcare.

In manufacturing, AI is used for predictive maintenance, quality control, and supply chain optimization. In energy, it is used for predicting equipment maintenance needs, detecting faults in energy systems, and optimizing energy production. In healthcare, it is used for disease diagnosis from medical images, drug discovery, and personalized treatment.

This breadth was important to see at the start. AI in IIoT is not one application. It is a pattern, repeated across industries with different sensors, different decisions, and different stakes, but the same underlying shape: collect data at the edge, process it intelligently, and act on it quickly.

### Co-creation in AIoT

One slide that stood out, even though it was less technical than the others, was the one on co-creation. The argument was that AIoT projects are too complex for any one company to build alone. They require diverse expertise across IT, OT, AI, and hardware, and they benefit from data federation across domains, joint AI/ML development, and shared platform ecosystems.

The four drivers the slides listed were complexity, innovation, speed, and risk mitigation. Combining strengths across companies leads to faster development, novel solutions, and shared investment. This is not just business theory. It explains why so many of the case studies later in the course involved partnerships between hardware companies, software companies, and end-user industries.

### Open Source Tools

The second deck introduced the toolkit. Six tools, each with a specific role in an AIoT system.

**Node-RED** is a visual programming tool for IoT applications. Drag and drop nodes onto a canvas, wire them together, and you have a flow that reads sensor data, processes it, and sends it somewhere. It runs on Windows, Mac, and Linux, installs through npm after Node.js is set up, and opens in a browser.

**ThingsBoard** is an open source IoT platform for data collection, processing, and visualization. It provides a web-based dashboard where you can register devices, ingest their data over MQTT, and build custom widgets and charts to visualize what is happening in real time.

**Eclipse Mosquitto** is a lightweight MQTT broker. MQTT is a publish-subscribe messaging protocol that is the de facto standard for IoT communication. The broker is the middleman that routes messages between publishers and subscribers. Mosquitto provides the `mosquitto_pub` and `mosquitto_sub` command-line tools for testing.

**Docker** is a containerization platform. It packages applications and all their dependencies into portable containers that run consistently across different environments, whether cloud, on-premises, or hybrid. Containers are how you actually deploy IoT services in a way that does not break when the environment changes.

**Edge Impulse** is the machine learning piece. It lets you collect sensor data, label it, train a model on it, and deploy that model to an edge device like an Arduino, Raspberry Pi, or Android phone. The pipeline is end to end, from data acquisition to live classification on a microcontroller.

**GitHub** is version control and collaboration. Everything I built in this course lived in GitHub repos, and pull requests, issues, and branches are the working language of any modern software project.

Each of these tools earned a deeper place in a later module. The course introduction was just the first time I saw their names.

---

## Insights

### The Whole Course Is One Long Answer to Module 01's Questions

I did not realize this until I started writing READMEs for the later modules, but Module 01 is structured as a set of questions that the rest of the course answers in detail. What is edge computing and why does it matter? Module 02. What devices do the work? Module 03. How do they communicate? Module 04. How do we clean and analyze the data? Modules 05 and 06. How do we make it real-time? Module 07. How do we keep it safe? Module 08. How do we generate new content with it? Module 09. How does it tie back to the cloud? Module 10. What rules govern it? Module 11. How do agents fit in? Module 12. The introduction was the whole course, compressed.

### IoT vs IIoT Is the Distinction That Made the Course Make Sense

I came in thinking I was learning about IoT in general. The slides made it clear pretty quickly that this is specifically about industrial systems, where the stakes are higher, the data volumes are larger, the latency tolerances are tighter, and the consequences of failure are more serious. That reframing changed how I read every later module. A smart factory is not just a smart home with bigger machines. It is a different category of system, with different design constraints, and the course is built around those constraints.

### The Tools Deck Was a Roadmap I Did Not Recognize at the Time

When I first saw Node-RED, ThingsBoard, Mosquitto, Docker, Edge Impulse, and GitHub listed as the tools for the course, they were just names on a slide. By the end of the course, every one of them had become something I had actually used. Mosquitto and ThingsBoard powered my L04 IIoT sensor simulation. GitHub holds every repo I built. Docker is implicit in how anything modern gets deployed. Edge Impulse is the cousin of TFLite, which I used in L02. Looking back at this slide deck after doing the work feels different from looking at it before. The names are no longer abstract.

---

## Resources

- Course Slides: ITAI 3377 Module 01 - AI in Edge and IoT Devices (Course Introduction)
- Course Slides: ITAI 3377 Module 01 - AI at the Edge and IoT, Open Source Tools
- Node-RED documentation: https://nodered.org/docs/
- ThingsBoard documentation: https://thingsboard.io/docs/
- Eclipse Mosquitto: https://mosquitto.org/documentation/
- Docker: https://docs.docker.com/get-started/
- Edge Impulse: https://docs.edgeimpulse.com/
- GitHub: https://docs.github.com/
- Companion modules in this repo: Module 02 (Edge Computing & AI), Module 03 (IIoT Devices), Module 04 (Communication)
