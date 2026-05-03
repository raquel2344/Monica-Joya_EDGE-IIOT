"""
SentinelEdge Live Dashboard
============================
Streamlit app for the recorded demo. Run with:
    streamlit run src/dashboard.py

The dashboard ticks the simulator forward one step at a time so the
viewer can see telemetry update, the AI flag anomalies, the autonomous
agent issue actions, and the generative AI write a plain-English
report -- all in real time.
"""

from __future__ import annotations

import time
from collections import deque
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import streamlit as st

from sentinel_edge import (
    AnomalyDetector,
    AutonomousAgent,
    IndustrialPumpSimulator,
    SyntheticDataGenerator,
    VibrationForecaster,
    NOMINAL_VIBRATION_MM_S,
    WARNING_VIBRATION,
    CRITICAL_VIBRATION,
    generate_maintenance_report,
    sign_payload,
    verify_payload,
)


st.set_page_config(
    page_title="SentinelEdge | Autonomous IIoT Agent",
    page_icon="⚙️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .big-metric { font-size: 2.4rem; font-weight: 700; }
    .ok    { color: #16a34a; }
    .warn  { color: #d97706; }
    .crit  { color: #dc2626; }
    .info  { color: #2563eb; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def build_pipeline():
    """Train models once per session."""
    sim = IndustrialPumpSimulator(seed=42)
    detector = AnomalyDetector()
    forecaster = VibrationForecaster()
    syngen = SyntheticDataGenerator()

    feats, vibs = [], []
    for _ in range(50):
        r = sim.step()
        feats.append([r.vibration_mm_s, r.temperature_c, r.pressure_bar])
        vibs.append(r.vibration_mm_s)
    for fault in ["bearing_wear", "cavitation", "imbalance"]:
        for row in syngen.generate_fault_window(fault, 12):
            feats.append([row["vibration_mm_s"],
                          row["temperature_c"],
                          row["pressure_bar"]])
    detector.fit(feats)
    forecaster.fit(vibs)

    return detector, forecaster, vibs


def _action_color(severity: str) -> str:
    return {
        "NORMAL": "ok",
        "INFO": "info",
        "WARNING": "warn",
        "CRITICAL": "crit",
    }.get(severity, "info")


def main():
    st.title("⚙️ SentinelEdge")
    st.caption(
        "Autonomous AI Agent + Generative AI for Industrial Edge & IIoT  •  "
        "Capstone Project • ITAI 3377 • Monica Joya • HCC Spring 2026"
    )

    # Sidebar controls
    with st.sidebar:
        st.header("Demo controls")
        if "running" not in st.session_state:
            st.session_state.running = False
        if "tick" not in st.session_state:
            st.session_state.tick = 0
        if "history" not in st.session_state:
            st.session_state.history = []
        if "decisions" not in st.session_state:
            st.session_state.decisions = []
        if "sim" not in st.session_state:
            st.session_state.sim = IndustrialPumpSimulator(seed=99)
        if "vib_window" not in st.session_state:
            st.session_state.vib_window = deque(maxlen=60)

        col_a, col_b = st.columns(2)
        if col_a.button("▶ Start"):
            st.session_state.running = True
        if col_b.button("⏸ Pause"):
            st.session_state.running = False
        if st.button("↻ Reset"):
            st.session_state.tick = 0
            st.session_state.history = []
            st.session_state.decisions = []
            st.session_state.sim = IndustrialPumpSimulator(seed=99)
            st.session_state.vib_window = deque(maxlen=60)
            st.session_state.running = False

        speed = st.slider("Tick interval (sec)", 0.05, 1.0, 0.25, 0.05)
        st.divider()
        st.subheader("Architecture")
        st.markdown(
            "- **Sensors:** vibration, temperature, pressure, RPM\n"
            "- **Edge AI:** Isolation Forest + Linear Regression forecast\n"
            "- **GenAI:** synthetic data + plain-English maintenance reports\n"
            "- **Security:** HMAC-SHA256 on every packet\n"
            "- **Agent:** hybrid rule + ML autonomous policy"
        )

    detector, forecaster, _ = build_pipeline()
    agent = AutonomousAgent()

    # Tick the simulator if running
    if st.session_state.running and st.session_state.tick < 200:
        reading = st.session_state.sim.step()

        payload = reading.to_dict()
        sig = sign_payload(payload)
        auth_ok = verify_payload(payload, sig)

        feats = [reading.vibration_mm_s,
                 reading.temperature_c,
                 reading.pressure_bar]
        pred, ascore = detector.score(feats)
        st.session_state.vib_window.append(reading.vibration_mm_s)
        forecast = forecaster.forecast(list(st.session_state.vib_window))

        decision = agent.decide(reading, pred, ascore, forecast)
        report = generate_maintenance_report(reading, forecast, ascore,
                                             decision.action)

        st.session_state.history.append({
            "tick": st.session_state.tick,
            "timestamp": reading.timestamp,
            "vibration_mm_s": reading.vibration_mm_s,
            "temperature_c": reading.temperature_c,
            "pressure_bar": reading.pressure_bar,
            "rpm": reading.rpm,
            "fault_mode": reading.fault_mode,
            "anomaly_score": ascore,
            "forecast": forecast,
            "action": decision.action,
            "severity": decision.severity,
            "auth_ok": auth_ok,
            "report": report,
        })
        if decision.action != "CONTINUE":
            st.session_state.decisions.append({
                "tick": st.session_state.tick,
                "action": decision.action,
                "severity": decision.severity,
                "rationale": decision.rationale,
                "report": report,
            })
        st.session_state.tick += 1

    # Top-line metrics
    if st.session_state.history:
        latest = st.session_state.history[-1]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Vibration (mm/s)", f"{latest['vibration_mm_s']:.2f}",
                  delta=f"{latest['vibration_mm_s'] - NOMINAL_VIBRATION_MM_S:+.2f} vs nominal")
        c2.metric("Temperature (°C)", f"{latest['temperature_c']:.1f}")
        c3.metric("Pressure (bar)", f"{latest['pressure_bar']:.2f}")
        c4.metric("Tick", st.session_state.tick)

        sev = latest["severity"]
        klass = _action_color(sev)
        st.markdown(
            f"<div class='big-metric {klass}'>"
            f"Action: {latest['action']}  •  Severity: {sev}"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Charts
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)

        st.subheader("Vibration with thresholds")
        chart_df = df[["tick", "vibration_mm_s", "forecast"]].set_index("tick")
        chart_df["warning_band"] = WARNING_VIBRATION
        chart_df["critical_band"] = CRITICAL_VIBRATION
        st.line_chart(chart_df)

        c_left, c_right = st.columns(2)
        with c_left:
            st.subheader("Temperature & Pressure")
            tp_df = df[["tick", "temperature_c", "pressure_bar"]].set_index("tick")
            st.line_chart(tp_df)
        with c_right:
            st.subheader("Anomaly score (lower = more anomalous)")
            ano_df = df[["tick", "anomaly_score"]].set_index("tick")
            st.line_chart(ano_df)

    # Decision log
    st.subheader("🤖 Autonomous decisions")
    if st.session_state.decisions:
        dec_df = pd.DataFrame(st.session_state.decisions[::-1])
        st.dataframe(dec_df, use_container_width=True, height=240)
    else:
        st.info("No decisions yet — press ▶ Start in the sidebar.")

    # Generative AI report (most recent)
    st.subheader("📝 Latest generative-AI maintenance report")
    if st.session_state.history:
        st.code(st.session_state.history[-1]["report"], language="text")
    else:
        st.write("Waiting for telemetry…")

    # Auto-rerun loop
    if st.session_state.running and st.session_state.tick < 200:
        time.sleep(speed)
        st.rerun()


if __name__ == "__main__":
    main()
