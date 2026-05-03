# Module 06: AI-Driven Data Analytics for IIoT

**Course:** ITAI 3377 - IoT & Edge Computing
**Student:** Monica Joya
**Term:** Spring 2026

---

## Overview

This is where the course turned from data plumbing to actual AI analytics. The L06 lab was hands-on Nixtla work for time series forecasting, and that is the part I keep coming back to.

---

## What I Learned

AI analytics in IIoT pays off through operational efficiency, better decision-making, reliability, innovation, and cost reduction. The hard part is that IIoT data is genuinely tough to analyze. High dimensionality from thousands of sensors, temporal patterns at frequencies from milliseconds to hours, heterogeneous types, quality issues like missing values and sensor drift, real-time streaming requirements, and the imbalance problem where rare equipment failures hide in vast amounts of normal data.

Implementation challenges are technical (integration, scalability, edge resources), organizational (IT and OT collaboration, change management, ROI), and operational (legacy systems, regulatory compliance, model monitoring). The IT and OT convergence point came up again in Module 08 cybersecurity. Everything is connected now, and the organizational structures from when those worlds were separate have to catch up.

Every major ML paradigm shows up in IIoT. Supervised for fault diagnosis, quality assessment, and predicting remaining useful life. Unsupervised for clustering operation modes. Semi-supervised for the common industrial case of small labeled data and a much larger unlabeled pile. Reinforcement learning for control strategies, with DDPG, PPO, SAC, and multi-agent approaches showing up again in the autonomous AGV thesis I analyzed for A09. Hybrid models like Physics-Informed Neural Networks combine first-principles physics with data-driven components. Transfer learning adapts a model trained on one process to a related one. Federated learning trains across decentralized devices without moving the data.

The CMU reading on federated learning reframed it for me. I had been thinking of it as a privacy feature. It is also a systems engineering response to expensive communication that forces small model updates, hardware heterogeneity, statistical heterogeneity where data on each device is not identically distributed, and privacy where even model updates can leak information without secure multiparty computation or differential privacy. The IIoT use case is a near-perfect fit: predictive maintenance trained across multiple factories without exposing any factory's operational data.

Anomaly detection has three types worth keeping separate. Point anomalies are single deviating values. Contextual anomalies look normal in general but are wrong in context, like a temperature fine for day shift but wrong for night. Collective anomalies are groups that are abnormal together even though no individual point is. Methods come in three layers: statistical (Z-score, ARIMA, Hotelling's T-squared), classical ML (SVMs, Isolation Forests, K-means, PCA), and deep learning (autoencoders, LSTMs, CNNs). Deep learning reportedly detects subtle failures 72 percent earlier than traditional methods and reduces false alarms by up to 85 percent. The tradeoff is that statistical is simple and explainable but limited, deep learning is powerful but opaque and data-hungry, and hybrid is best for safety-critical systems where regulators want explainability.

Nixtla was the lab tool. Open-source Python library for time series forecasting and anomaly detection wrapping state-of-the-art models. Probabilistic forecasting with uncertainty quantification, multi-horizon forecasting, anomaly detection using generative models, AutoML for model selection. The big advantage for IIoT is the uncertainty quantification. Predictive maintenance is not just "what will happen" but "how confident are we." A point estimate is not enough when you are deciding whether to take an industrial system offline.

Predictive maintenance ranks four strategies from least to most sophisticated. Reactive (fix after it breaks) is cheapest until it isn't. Preventive (fixed schedule) wastes effort on equipment that did not need it. Condition-based (sensor thresholds) is better but threshold tuning is hard. Predictive (forecast the failure with ML) is hardest to build but has the highest payoff.

Two case study numbers worth remembering. Automotive assembly used predictive quality control with computer vision and sensor fusion to cut defect rates 32 percent and speed inspections 45 percent. Wind farm optimization used turbine performance prediction with transfer learning across locations to increase energy output 8 percent and cut maintenance costs 21 percent.

---

## Insights

Pick the method that fits the problem. Statistical methods are still right for a lot of anomaly detection. Deep learning is right when patterns are too complex for hand-tuned features. Hybrid models are right when regulators or operators need explainability. The worst engineering decision is picking the most impressive technique and bending the problem to fit it.

Probabilistic forecasting beats point forecasting. A model that says "this turbine has an 85 percent probability of failing between days 9 and 14" is more useful than one that says "it will fail in 12 days." Uncertainty bands let humans make calibrated calls about whether to trust the model.

Module 06 is the analytics layer that everything else either feeds into or builds on. Module 05 supplies the clean data. Module 07 supplies the real-time delivery. Module 08 supplies security. Module 10 supplies the cloud and hybrid architecture. When analytics work, every layer below is doing its job. When they fail, the failure is usually somewhere lower in the stack.

---

## Resources

- Course Slides: ITAI 3377 Module 06 - AI-Driven Data Analytics for IIoT
- Li, T. (2019). *Federated Learning: Challenges, Methods, and Future Directions.* CMU Machine Learning Blog.
- Mathai, C. (n.d.). *Artificial Intelligence of Things: When AI and IoT Meet.* OnLogic.
- de Haro-Olmo, F. J. et al. (2023). *ELI: an IoT-aware big data pipeline with data curation and data quality.* PeerJ Computer Science, 9:e1605.
- Nixtla open-source library: https://github.com/Nixtla/nixtla
