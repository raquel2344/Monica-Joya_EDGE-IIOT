# SentinelEdge — Capstone Project
**Autonomous AI Agent + Generative AI for Industrial Edge & IIoT**

| | |
|---|---|
| **Course** | ITAI 3377 — IoT & Edge Computing |
| **Semester** | Spring 2026 |
| **Student** | Monica Joya (Raquel) |
| **School** | Houston City College — BAT in AI & Robotics |
| **Path** | Practical Path |
| **Submission name** | `CP_MonicaJoya_Individual_ITAI_3377` |

---

## What this project is

SentinelEdge is a virtual end-to-end IIoT system that monitors a simulated industrial centrifugal pump and decides — autonomously — when to schedule maintenance, reduce load, or shut the pump down. It demonstrates every required theme from the capstone brief in one runnable codebase:

- **IIoT devices** → simulated pump with vibration, temperature, pressure, and RPM sensors.
- **Edge computing** → all AI runs locally; no cloud dependency at inference time.
- **Generative AI** → synthetic fault-data generator (rebalances rare classes at training); plain-English maintenance reports (templated locally; pluggable to Groq `llama-3.3-70b-versatile` in production, the same backend used in InvestorInsight AI).
- **Autonomous agent** → hybrid policy combining ISO 10816 hard rules with ML signals (Isolation Forest anomaly score + Linear Regression vibration forecast).
- **Security** → HMAC-SHA256 signature on every sensor packet; gateway drops tampered messages.
- **Real-time UI** → Streamlit dashboard with live charts, decision log, and the latest generative report.

## Folder layout

```
Capstone/
├── src/
│   ├── sentinel_edge.py    # core agent: simulator, models, security, decision loop
│   └── dashboard.py        # Streamlit live UI for the recorded demo
├── data/                   # telemetry.csv + decisions.jsonl (generated on run)
├── docs/
│   └── architecture.svg    # system architecture diagram
├── demo/                   # MP4 demo will be saved here
├── journal/                # reflective learning journal
├── requirements.txt
└── README.md
```

## How to run (Mac M4 / Linux / Windows)

The first step uses Git sparse checkout so you only download the `Capstone/` folder instead of the entire `Monica-Joya_EDGE-IIOT` course repository.

```bash
# 1. Clone only the Capstone folder (sparse checkout)
git clone --filter=blob:none --no-checkout https://github.com/raquel2344/Monica-Joya_EDGE-IIOT.git
cd Monica-Joya_EDGE-IIOT
git sparse-checkout init --cone
git sparse-checkout set Capstone
git checkout main
cd Capstone

# 2. Create and activate a virtual env
python3 -m venv venv
source venv/bin/activate          # (Windows: venv\Scripts\activate)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Option A — Run the headless simulation (writes CSV + JSONL logs)
python src/sentinel_edge.py

# 4. Option B — Launch the live Streamlit dashboard (used for the recorded demo)
streamlit run src/dashboard.py
```

Open the dashboard in your browser at `http://localhost:8501`. Press **▶ Start** in the sidebar; the simulator ticks forward, AI inference runs each tick, and you'll see the autonomous agent escalate from CONTINUE → SCHEDULE_MAINTENANCE → REDUCE_LOAD → EMERGENCY_SHUTDOWN as the simulated pump degrades.

## What the recorded MP4 demo shows

1. The dashboard at idle (healthy nominal readings).
2. Simulator running — vibration, temperature, pressure trends.
3. The fault inject around tick 60 — anomaly score drops, forecast climbs.
4. The agent firing **SCHEDULE_MAINTENANCE** *before* the warning threshold (predictive win).
5. Escalation to **REDUCE_LOAD** in the warning band.
6. **EMERGENCY_SHUTDOWN** at ISO 10816 zone D.
7. The generative-AI maintenance report panel updating in real time.
8. The terminal showing the "tampered packet rejected" security check.

## Deliverables map (per assignment rubric)

| Deliverable | File / artifact |
|---|---|
| Project Proposal & Planning | `docs/proposal.pdf` (to be added) |
| System Architecture & Design | `docs/architecture.svg` + `docs/architecture.md` |
| Implementation & Testing | `src/sentinel_edge.py`, `src/dashboard.py`, `data/*` |
| Demo (MP4) | `demo/sentinelEdge_demo.mp4` |
| Reflective Learning Journal | `journal/reflective_journal.pdf` |

## Tech stack

- **Python 3.10+** (works with 3.11 like InvestorInsight AI on HF Spaces)
- **scikit-learn** — Isolation Forest, Linear Regression
- **NumPy / pandas** — numerical core, time series handling
- **Streamlit** — real-time browser UI
- **HMAC-SHA256** (stdlib) — packet authentication

## Acknowledgments

Reuses the LinearRegression-as-best-MASE finding from ITAI 3377 L06 group work with Cassy Cormier, Kolapo Mogaji, and Sufyan Rafiq. Architectural patterns (ML + hybrid rule policy + signed packets) inspired by SentinelAI work with Ahmet Burak Solak.
