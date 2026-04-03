# Module 05: Data Acquisition and Preprocessing

**Course:** ITAI 3377 - IoT & Edge Computing  
**Student:** Monica Joya  
**Term:** Spring 2026

---

## Overview

This module focused on the critical early stages of any AIoT data pipeline: how data gets collected from sensors and how it gets cleaned up before analysis. I learned that the quality of preprocessing directly impacts the performance of AI models downstream. If bad data goes in, bad predictions come out.

---

## What I Learned

### Data Collection Strategies

I learned there are two main approaches to collecting data from IoT sensors:

**Batch Data Collection** involves gathering data over time and processing it all at once. This works well for applications that do not need instant responses, like financial transaction logs or inventory management systems. The tradeoff is that you get less immediate insight, but the processing is more efficient.

**Real-time Data Collection** means collecting and processing data immediately as it arrives. This is essential for applications where decisions need to happen fast, like healthcare monitoring, traffic management, or financial trading systems. The tradeoff here is that it requires more resources and a constant connection.

### Data Sampling Rates

Sampling rate refers to how often we collect data points from a sensor. I learned that higher sampling rates give you more detail but require more storage and processing power. Lower sampling rates save resources but might miss important changes in the data. The key is finding the right balance for your specific application.

### Data Preprocessing Techniques

I learned about three main preprocessing techniques:

**Filtering** removes unwanted noise from sensor data. There are different types depending on what you need:
- Low-pass filters keep slow-changing trends and remove rapid fluctuations
- High-pass filters keep rapid changes and remove slow drifts
- Band-pass filters isolate signals within a specific frequency range

**Aggregation** condenses data into summaries. Common methods include averaging values over time, summing totals within a window, or finding the maximum and minimum values. This reduces storage needs and speeds up analysis.

**Feature Extraction** transforms raw sensor readings into meaningful inputs for AI models. This includes statistical features like mean and variance, time-domain features like peaks, and frequency-domain features using techniques like Fast Fourier Transform.

### Data Cleaning

Data cleaning is about finding and fixing problems in your dataset. The main techniques I learned include:

- Handling missing data through imputation (filling in estimates) or deletion
- Reducing noise through smoothing and filtering
- Normalizing data to put everything on the same scale
- Detecting and removing outliers that could throw off analysis

### Data Transformation

Before feeding data into AI models, it often needs to be transformed:

- **Normalization** scales values to a common range, usually 0 to 1
- **Scaling** adjusts the magnitude of features to a standard deviation
- **Encoding** converts categorical data like labels into numerical values

### Data Storage Options

I learned about the tradeoffs between local and cloud storage:

**Local Storage on Edge Devices** offers reduced latency, works without internet, and keeps data private. However, capacity is limited and costs more per unit of storage.

**Cloud Storage** provides massive capacity, easy scaling, and powerful management tools. The downsides are that it depends on connectivity, can add latency, and raises privacy concerns.

### Edge Devices vs Traditional IoT

This module also clarified the difference between edge devices and traditional IoT devices. Edge devices like Raspberry Pi or NVIDIA Jetson can process data locally and make decisions in real-time. Traditional IoT devices mainly collect and transmit data to the cloud for processing elsewhere. Edge computing reduces latency and bandwidth usage, which matters a lot for time-sensitive applications.

---

## Key Takeaways

1. Data preprocessing is not optional. It directly affects how well AI models perform.

2. The choice between batch and real-time collection depends on how quickly decisions need to be made.

3. Filtering, aggregation, and feature extraction each serve different purposes in preparing data for analysis.

4. There is always a tradeoff between data granularity, storage costs, and processing requirements.

5. Distributed preprocessing at the edge can reduce bandwidth usage and improve response times compared to sending everything to the cloud.

6. Security and privacy need to be considered at every stage, from collection through storage.

---

## Connection to Other Modules

This module builds directly on Module 04, where I learned about IIoT communication protocols like MQTT, CoAP, and OPC UA. Those protocols handle how data moves across networks. This module covers what happens to that data once it arrives.

The preprocessing concepts here also connect forward to Module 06, where I will apply AI-driven analytics to IoT data. Clean, well-prepared data is essential for accurate predictions and meaningful insights.

---

## Reflection

What stood out to me most was realizing how much work happens before data ever reaches an AI model. I used to think of data collection as simple, but there are real engineering decisions at every step: how often to sample, what filtering to apply, where to store data, and how to handle missing values.

I also found the edge vs cloud tradeoffs interesting. In many real-world scenarios, you need a hybrid approach where some processing happens locally for speed and some happens in the cloud for heavier analysis. The ELI pipeline framework I read about in the research papers showed how tools like CHAMALEON for data curation and DMN4DQ for data quality assessment can be integrated into a Big Data pipeline specifically for IoT environments.

The concept of using DAGs (Directed Acyclic Graphs) to represent preprocessing pipelines was new to me. It makes sense as a way to organize the order of operations and identify dependencies between preprocessing steps.

---

## References

- Course slides: ITAI 3377 Module 05 - Data Acquisition and Preprocessing
- Talking IoT. (2024). Data Acquisition and Pre-Processing in AIoT. https://talkingiot.io/data-acquisition-and-pre-processing-in-aiot
- Tawakuli, A., Kaiser, D., & Engel, T. (2022). Transforming IoT Data Preprocessing: A Holistic, Normalized and Distributed Approach. DATA '22. https://doi.org/10.1145/3560905.3567762
- de Haro-Olmo, F. J., et al. (2023). ELI: an IoT-aware big data pipeline with data curation and data quality. PeerJ Computer Science. https://doi.org/10.7717/peerj-cs.1605
