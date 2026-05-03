# Module 09: Generative AI for Edge and IIoT

**Course:** ITAI 3377 - IoT & Edge Computing
**Student:** Monica Joya
**Term:** Spring 2026

---

## Overview

This module shifted the course from how we collect and protect industrial data to how we generate it, and from cloud-heavy AI to small models that can actually run on edge devices. The graded work was A09, my analysis of Hjulström's KTH thesis on autonomous agents for AGVs in Industry 4.0.

---

## What I Learned

Three architectures came up most. GANs use a generator and discriminator competing until the generator's synthetic data is indistinguishable from real, which is what Siemens used for gas turbine design. VAEs use a probabilistic encoder-decoder pair to generate variations on existing data while keeping structure intact. Transformers use self-attention for sequence processing and power most modern LLMs and increasingly the small ones too.

Generative AI has five main use cases in IIoT. Synthetic data creation builds complete industrial datasets that look real but contain no proprietary information, useful for training models for new factory setups before they exist or simulating rare failures. Data augmentation expands existing datasets to handle rare events that almost never show up in production. Anomaly generation creates realistic failure scenarios so detection systems can be trained on them without waiting for things to actually break. Predictive maintenance generates equipment-degradation data so scheduling models can learn the patterns. Process optimization explores parameter spaces too large to test physically, and one chemical process example reported a 30 percent energy reduction.

Generative AI also improves digital twins by filling in missing data in real time, increasing fidelity, and enabling what-if scenario analysis. The challenges are real-time performance on the edge and managing model drift as the physical system changes.

TinyAgents were the biggest topic in the module. An AI agent is an autonomous entity that perceives its environment and acts to achieve specific goals. TinyAgents are these agents running on small language models that fit on constrained edge devices: Phi-2 at 2.7B parameters, Llama 3 8B, MobileGPT. The benefits are familiar from the rest of the course. Local processing cuts latency from seconds to milliseconds, bandwidth drops 80 to 95 percent, sensitive data stays on device, and the system keeps working through network disruptions.

Model compression makes this possible. Knowledge distillation trains a small student model to mimic a large teacher and gets up to 10x size reduction. Quantization drops numerical precision (FP32 to INT8 cuts size 75 percent). Pruning removes connections that contribute little (40 to 80 percent parameter reduction is realistic). Parameter sharing reuses weights across components.

The Berkeley TinyAgent reading made all of this concrete. The team fine-tuned TinyLlama-1.1B and Wizard-2-7B for function calling on Mac, generated 80,000 training examples synthetically using GPT-4-Turbo for about $500, and used 4-bit quantization with a group size of 32. The result was a 1.1B parameter model that achieved 80.06 percent success on its function calling benchmark, beating GPT-4-Turbo's 79.08 percent on the same task. The whole thing runs locally on a MacBook M3 Pro. They also introduced Tool RAG: instead of putting every available tool in the prompt every time, they trained a small DeBERTa-v3 classifier to predict which tools the user query needs. That cut prompt size roughly in half while improving accuracy.

The MIT Technology Review article gave me the cleanest definition. AI agents are AI models and algorithms that can autonomously make decisions in a dynamic world. The Princeton paper cited three characteristics: they pursue difficult goals without step-by-step instructions, they can be instructed in natural language and act without supervision, and they can use tools like web search, programming, or planning. The article drew a useful split between software agents that run on computers and use apps and embodied agents that operate in 3D worlds or robots. The current wave is driven by language models and tool use. The previous wave around 2016 was AlphaGo built on RL. The new generation is much more general where the older ones were built for one specific task. The article was also honest about limits: coding agents can write code but cannot reliably test it, agents lose track of long tasks because their context windows are limited, models still hallucinate, and embodied agents lack training data. The whole field is roughly where self-driving cars were a decade ago.

For A09, I analyzed Hjulström's KTH thesis on autonomous agents for AGVs in Industry 4.0. The thesis trained three AGV agents in a 10x10 grid world using Double Deep Q-Network reinforcement learning. The agents had to move objects between task squares and recharge at charging stations without crashing or running out of battery. After about 200,000 training episodes the system completed all 300 test tasks (100 per agent) with zero collisions and zero battery depletions, averaging only 2.59 extra steps per task beyond the optimal path.

The Kang et al. paper was the most technical of the readings but tied many module threads together. They proposed a Tiny MADRL framework for migrating UAV digital twins between roadside units in real time, set up as a Stackelberg game where roadside units act as leaders setting bandwidth prices and UAVs act as followers buying bandwidth. They used dynamic structured pruning on the actor network to remove the least important neurons, making the model small enough for edge deployment while converging faster than standard PPO. The takeaway is that pruning is not just research. It is the practical reason we can put DRL agents on real edge hardware.

The slides closed with ethics and trends. Data privacy and security, bias and fairness, transparency, environmental impact, and job displacement. The Edge AI timeline projects TinyML for predictive maintenance becoming widespread by 2026, autonomous decision-making at the edge standard by 2028, and edge-cloud hybrid architectures dominating by 2030. Cross-industry impact estimates: 30-40 percent efficiency in smart manufacturing, 15-25 percent consumption reduction in energy management, 20-35 percent waste reduction in supply chain.

The Siemens gas turbine case pulled it together. Their generator proposed new turbine designs based on patterns from successful past designs, and the discriminator evaluated proposals against high-performing real turbines. Design time dropped from months to weeks, new designs had higher output and lower emissions, and the AI suggested unconventional configurations human engineers had not considered. Different technique, same idea as Hjulström's AGV reinforcement learning. Let the agent explore solutions humans would not have tried.

---

## Insights

The Berkeley result was the most useful realization for me. A 1.1B parameter model can outperform GPT-4-Turbo on a specific function-calling benchmark by training it on the right data instead of training it on everything. That changes how I think about edge deployment. The point is not to make a small version of a big model. The point is to specialize a small model for the actual task.

The case study connection was strong. Hjulström's AGV thesis is a multi-agent DRL system. Combining it with pruning from the UAV Metaverses paper and synthetic data generation from the slides gives a complete recipe for putting intelligent industrial agents on the edge. That ties directly to the ESP32-S3 edge AI work I want to come back to.

Module 09 sits in the middle of the course's edge AI thread and shows what edge AI actually looks like when all the pieces come together: small models, generative techniques, multi-agent systems, and tool use, all running locally instead of in the cloud.

---

## Resources

- Course Slides: ITAI 3377 Module 09 - Generative AI for Edge and IIoT
- Hjulström, L. (2022). *Autonomous agents in Industry 4.0: A self-optimizing approach for automated guided vehicles in Industry 4.0 environments* [Bachelor's thesis, KTH Royal Institute of Technology].
- MIT Technology Review. (2024, July 5). *What are AI agents?*
- Kang, J. et al. (2024). *Tiny Multi-Agent DRL for Twins Migration in UAV Metaverses.* arXiv:2401.09680v2.
- Erdogan, L. E. et al. (2024, May 29). *TinyAgent: Function Calling at the Edge.* Berkeley Artificial Intelligence Research (BAIR) Blog.
