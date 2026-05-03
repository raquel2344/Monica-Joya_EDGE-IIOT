# Module 05: Data Acquisition and Preprocessing

**Course:** ITAI 3377 - IoT & Edge Computing
**Student:** Monica Joya
**Term:** Spring 2026

---

## Overview

This module covered the engineering work that happens before AI ever touches the data. No graded assignments. Just slides and three readings.

---

## What I Learned

There are two ways to collect IIoT sensor data. Batch processing gathers data over time and processes it all at once, which works for inventory and transaction logs where decisions can wait. Real-time processing handles data as it arrives, which is required for healthcare monitoring or traffic management. Sampling rate sits underneath both. Higher rates give more detail but cost more storage and compute. The right rate captures what the application actually cares about, not the highest the sensor supports.

Preprocessing splits into filtering, aggregation, and feature extraction. Filtering removes unwanted noise, low-pass keeps slow trends, high-pass does the opposite, band-pass isolates a specific range. Aggregation condenses data into summaries like averages, sums, and max/min over a window. Feature extraction turns raw readings into model-ready inputs through statistical, time-domain, and frequency-domain features.

Cleaning is about finding and fixing problems before they propagate. Missing data gets imputed or deleted. Noise gets smoothed. Values get normalized to a common scale. Outliers get flagged or removed. The de Haro-Olmo smart farm pipeline made this concrete: 45.8 percent of their offline sensor data did not meet quality thresholds and was discarded. If almost half the raw data is unusable, cleaning is not optional.

Transformation usually means normalization (scale to 0-1), scaling (adjust feature magnitudes), and encoding (turn categorical labels into numbers).

Storage is a local-versus-cloud tradeoff. Local is low-latency, works offline, keeps data private, but capacity is limited. Cloud is massive and scalable, but depends on connectivity and adds latency and privacy considerations. Real systems are hybrid: time-critical data stays local, long-term and aggregated data goes to the cloud.

The Tawakuli paper made the case for moving preprocessing to the edge. Their distributed approach reported 71 percent energy reduction and 58 percent bandwidth reduction compared to centralizing in the cloud. If each edge device cleans, filters, and aggregates its own data before transmission, the network only carries what is needed.

---

## Insights

Preprocessing is not a single step. It is a sequence of decisions, how to sample, what to filter, how to handle missing values, where to store, what to transform, and each one has downstream consequences that are not obvious until you see them.

Quality beats quantity. The 45.8 percent discard rate from the smart farm case is the number I want to remember. Better to invest in cleaner acquisition than to scale up a noisy pipeline and hope analytics will sort it out.

Edge preprocessing pays for itself. The 71 percent energy and 58 percent bandwidth reductions show this is not just a latency play. It is a sustainability and cost play too.

---

## Resources

- Course Slides: ITAI 3377 Module 05 - Data Acquisition and Preprocessing
- Talking IoT. (2024). *Data Acquisition and Pre-Processing in AIoT.*
- Tawakuli, A., Kaiser, D., & Engel, T. (2022). *Transforming IoT Data Preprocessing: A Holistic, Normalized and Distributed Approach.* DATA '22.
- de Haro-Olmo, F. J., Valencia-Parra, A., Varela-Vaca, A. J., Alvarez-Bermejo, J. A., & Gomez-Lopez, M. T. (2023). *ELI: an IoT-aware big data pipeline with data curation and data quality.* PeerJ Computer Science, 9:e1605.
