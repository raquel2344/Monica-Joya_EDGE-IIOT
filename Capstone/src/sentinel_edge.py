"""
SentinelEdge: Autonomous AI Agent for Predictive Maintenance in IIoT
=====================================================================
Capstone Project - ITAI 3377 (IoT & Edge Computing) - Spring 2026
Author: Monica Joya (Raquel)
Houston City College - BAT in AI & Robotics

This module implements the core autonomous agent system. It simulates
an industrial pump / motor with vibration, temperature, and pressure
sensors streaming data through an in-memory message bus, an edge
gateway running anomaly detection plus a forecasting model, a
generative AI layer for synthetic data and natural-language reporting,
a security layer (HMAC + AES-GCM), and a rule-based autonomous decision
agent that issues maintenance actions.

Entry point: this file produces a CSV log and decision history.
The Streamlit dashboard (dashboard.py) reads these to display the
real-time view used in the recorded demo.
"""

from __future__ import annotations

import csv
import hashlib
import hmac
import json
import os
import random
import secrets
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

SHARED_SECRET = b"sentinel-edge-shared-secret-CHANGE-IN-PROD"
DEVICE_ID = "PUMP-A1-Houston-Plant"

# Operating thresholds (typical industrial centrifugal pump)
NOMINAL_VIBRATION_MM_S = 2.5     # ISO 10816 zone A/B boundary
NOMINAL_TEMP_C = 65.0
NOMINAL_PRESSURE_BAR = 4.5

WARNING_VIBRATION = 4.5
CRITICAL_VIBRATION = 7.1


# ---------------------------------------------------------------------
# 1. Sensor Simulation Layer (the "things" in IIoT)
# ---------------------------------------------------------------------

@dataclass
class SensorReading:
    """One tick of telemetry from the simulated pump."""
    timestamp: str
    device_id: str
    vibration_mm_s: float
    temperature_c: float
    pressure_bar: float
    rpm: int
    fault_mode: str = "healthy"  # ground truth, not exposed to AI

    def to_dict(self) -> dict:
        return asdict(self)


class IndustrialPumpSimulator:
    """
    Generates realistic sensor readings for a centrifugal pump,
    with the ability to inject degradation modes (bearing wear,
    cavitation, impeller imbalance) over time.
    """

    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)
        self.tick = 0
        self.fault_mode = "healthy"
        self.degradation = 0.0  # 0.0 = perfect, 1.0 = imminent failure

    def step(self) -> SensorReading:
        """Advance one tick. Degradation grows over time once a fault begins."""
        self.tick += 1

        # Schedule a fault around tick 60 to make the demo interesting
        if self.tick == 60:
            self.fault_mode = self.rng.choice(
                ["bearing_wear", "cavitation", "imbalance"]
            )
        if self.fault_mode != "healthy":
            self.degradation = min(1.0, self.degradation + 0.012)

        # Base operation around nominal values
        vib = NOMINAL_VIBRATION_MM_S + self.rng.normal(0, 0.15)
        temp = NOMINAL_TEMP_C + self.rng.normal(0, 0.4)
        pres = NOMINAL_PRESSURE_BAR + self.rng.normal(0, 0.05)
        rpm = 1750 + int(self.rng.normal(0, 8))

        # Apply fault signature
        if self.fault_mode == "bearing_wear":
            vib += self.degradation * 6.5
            temp += self.degradation * 12.0
        elif self.fault_mode == "cavitation":
            vib += self.degradation * 4.0
            pres -= self.degradation * 1.8
        elif self.fault_mode == "imbalance":
            vib += self.degradation * 5.5
            rpm -= int(self.degradation * 40)

        return SensorReading(
            timestamp=datetime.now(timezone.utc).isoformat(),
            device_id=DEVICE_ID,
            vibration_mm_s=round(vib, 3),
            temperature_c=round(temp, 2),
            pressure_bar=round(pres, 3),
            rpm=rpm,
            fault_mode=self.fault_mode,
        )


# ---------------------------------------------------------------------
# 2. Security Layer (HMAC authentication + tamper detection)
# ---------------------------------------------------------------------

def sign_payload(payload: dict, key: bytes = SHARED_SECRET) -> str:
    """Produce an HMAC-SHA256 signature for the JSON-serialized payload."""
    msg = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def verify_payload(payload: dict, signature: str,
                   key: bytes = SHARED_SECRET) -> bool:
    """Constant-time HMAC verification at the edge gateway."""
    expected = sign_payload(payload, key)
    return hmac.compare_digest(expected, signature)


# ---------------------------------------------------------------------
# 2b. Channel Encryption Layer (PRODUCTION ROADMAP - NOT ACTIVE)
# ---------------------------------------------------------------------
# Status: Planned for production deployment. Intentionally NOT active in
# this demo so the simulation stays self-contained and inspectable.
#
# The architecture diagram (docs/architecture.svg) shows AES-GCM alongside
# HMAC-SHA256 as the full security boundary. The two primitives serve
# different purposes and are complementary, not redundant:
#
#   - HMAC-SHA256 (active above) provides INTEGRITY + AUTHENTICATION.
#     It detects tampering and confirms the sender held the shared key,
#     but the payload itself is still readable on the wire.
#
#   - AES-GCM (planned, below) would add CONFIDENTIALITY + INTEGRITY.
#     It encrypts the payload so an attacker tapping the OT network
#     cannot read sensor values, decision actions, or device IDs.
#     AES-GCM is an authenticated cipher, so it provides its own
#     integrity check on the ciphertext as well.
#
# Reference implementation (commented out - do not enable without also
# adding key management; the static SHARED_SECRET above is for demo only):
#
# from cryptography.hazmat.primitives.ciphers.aead import AESGCM
#
# def encrypt_payload(payload: dict, key: bytes) -> tuple[bytes, bytes]:
#     """Encrypt with AES-GCM. Returns (nonce, ciphertext_with_tag)."""
#     nonce = secrets.token_bytes(12)  # 96-bit nonce, NIST recommended
#     aesgcm = AESGCM(key)
#     plaintext = json.dumps(payload, sort_keys=True).encode("utf-8")
#     ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)
#     return nonce, ciphertext
#
# def decrypt_payload(nonce: bytes, ciphertext: bytes, key: bytes) -> dict:
#     """Decrypt and verify AES-GCM. Raises InvalidTag if tampered."""
#     aesgcm = AESGCM(key)
#     plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
#     return json.loads(plaintext.decode("utf-8"))
#
# Production deployment would also add:
#   - Key rotation (e.g., rotate every 24h via gateway-issued tokens)
#   - Certificate pinning between device and gateway
#   - Replay protection with per-message nonces and a sliding window
#   - Hardware-backed key storage (TPM on Jetson Orin, Secure Enclave on Mac)
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# 3. Edge Gateway + AI Models
# ---------------------------------------------------------------------

class AnomalyDetector:
    """Isolation Forest trained on healthy operating data."""

    def __init__(self):
        self.model = IsolationForest(
            n_estimators=80,
            contamination=0.05,
            random_state=7,
        )
        self.fitted = False

    def fit(self, healthy_window: list[list[float]]) -> None:
        self.model.fit(healthy_window)
        self.fitted = True

    def score(self, features: list[float]) -> tuple[int, float]:
        """Returns (label, anomaly_score). label: 1 = normal, -1 = anomaly."""
        if not self.fitted:
            return 1, 0.0
        pred = int(self.model.predict([features])[0])
        score = float(self.model.score_samples([features])[0])
        return pred, score


class VibrationForecaster:
    """
    Linear-regression forecaster that predicts vibration N steps ahead
    using a small lag window. Reused from the ITAI 3377 L06 work
    (LinearRegression scored best on MASE in that lab).
    """

    def __init__(self, lag: int = 8, horizon: int = 5):
        self.lag = lag
        self.horizon = horizon
        self.model = LinearRegression()
        self.fitted = False

    def fit(self, series: list[float]) -> None:
        if len(series) < self.lag + self.horizon + 5:
            return
        X, y = [], []
        for i in range(len(series) - self.lag - self.horizon):
            X.append(series[i:i + self.lag])
            y.append(series[i + self.lag + self.horizon - 1])
        self.model.fit(X, y)
        self.fitted = True

    def forecast(self, series: list[float]) -> Optional[float]:
        if not self.fitted or len(series) < self.lag:
            return None
        window = np.asarray(series[-self.lag:]).reshape(1, -1)
        return float(self.model.predict(window)[0])


# ---------------------------------------------------------------------
# 4. Generative AI Layer
# ---------------------------------------------------------------------

class SyntheticDataGenerator:
    """
    Produces synthetic 'what-if' degraded readings. This is the
    generative-AI-for-edge angle: at training time we use the generator
    to balance the dataset (rare faults are scarce in real plants);
    at inference time we use it to stress-test the autonomous policy.
    """

    def __init__(self, seed: int = 11):
        self.rng = np.random.default_rng(seed)

    def generate_fault_window(self, fault: str, n: int = 30) -> list[dict]:
        out = []
        for k in range(n):
            severity = k / max(n - 1, 1)
            row = {
                "vibration_mm_s": NOMINAL_VIBRATION_MM_S
                                  + self.rng.normal(0, 0.15)
                                  + severity * (6.0 if fault == "bearing_wear" else 4.5),
                "temperature_c": NOMINAL_TEMP_C
                                 + self.rng.normal(0, 0.4)
                                 + severity * (12.0 if fault == "bearing_wear" else 3.0),
                "pressure_bar": NOMINAL_PRESSURE_BAR
                                + self.rng.normal(0, 0.05)
                                - severity * (1.6 if fault == "cavitation" else 0.0),
            }
            out.append(row)
        return out


def generate_maintenance_report(reading: SensorReading,
                                forecast_value: Optional[float],
                                anomaly_score: float,
                                action: str) -> str:
    """
    Generative AI report writer. In production this would call
    Groq llama-3.3-70b-versatile (already wired up for InvestorInsight AI).
    For an offline demo we use a templated generator so the system
    runs without a network or API key. The structure is identical to
    what the LLM produces in the cloud version.
    """
    severity = "CRITICAL" if reading.vibration_mm_s > CRITICAL_VIBRATION \
        else "WARNING" if reading.vibration_mm_s > WARNING_VIBRATION \
        else "NORMAL"

    forecast_txt = (f"{forecast_value:.2f} mm/s in 5 ticks"
                    if forecast_value is not None else "no forecast yet")

    return (
        f"[{severity}] Pump {reading.device_id} reports vibration "
        f"{reading.vibration_mm_s:.2f} mm/s, temperature "
        f"{reading.temperature_c:.1f} C, pressure "
        f"{reading.pressure_bar:.2f} bar. Anomaly score: "
        f"{anomaly_score:.3f}. Forecast: {forecast_txt}. "
        f"Recommended action: {action}."
    )


# ---------------------------------------------------------------------
# 5. Autonomous Decision Agent
# ---------------------------------------------------------------------

@dataclass
class Decision:
    timestamp: str
    action: str
    severity: str
    rationale: str
    reading: dict = field(default_factory=dict)


class AutonomousAgent:
    """
    Hybrid policy:
      - Hard rules for safety-critical thresholds (ISO 10816 zones)
      - Soft signal from anomaly score + forecast for proactive action
    The agent is autonomous: it decides without a human in the loop,
    but every decision is logged and explainable.
    """

    def decide(self, reading: SensorReading,
               anomaly_pred: int,
               anomaly_score: float,
               forecast: Optional[float]) -> Decision:

        # Hard safety rule
        if reading.vibration_mm_s > CRITICAL_VIBRATION:
            return Decision(
                timestamp=reading.timestamp,
                action="EMERGENCY_SHUTDOWN",
                severity="CRITICAL",
                rationale=(f"Vibration {reading.vibration_mm_s:.2f} mm/s "
                           f"exceeds ISO 10816 zone D ({CRITICAL_VIBRATION})"),
                reading=reading.to_dict(),
            )

        # Predictive rule: forecast is climbing toward warning band
        # while current reading is still in the nominal zone.
        # Fires earlier than threshold-based rules - this is the "smart" win.
        predictive_threshold = WARNING_VIBRATION * 0.78  # ~3.5 mm/s
        if forecast is not None and forecast > predictive_threshold \
                and reading.vibration_mm_s <= predictive_threshold:
            return Decision(
                timestamp=reading.timestamp,
                action="SCHEDULE_MAINTENANCE",
                severity="WARNING",
                rationale=(f"Forecast vibration {forecast:.2f} mm/s "
                           f"trending toward warning band; schedule "
                           f"maintenance proactively"),
                reading=reading.to_dict(),
            )

        # Warning band reached
        if reading.vibration_mm_s > WARNING_VIBRATION:
            return Decision(
                timestamp=reading.timestamp,
                action="REDUCE_LOAD",
                severity="WARNING",
                rationale=(f"Vibration {reading.vibration_mm_s:.2f} mm/s "
                           f"in warning band; reduce load to extend life"),
                reading=reading.to_dict(),
            )

        # Anomaly without threshold breach
        if anomaly_pred == -1:
            return Decision(
                timestamp=reading.timestamp,
                action="FLAG_FOR_REVIEW",
                severity="INFO",
                rationale=(f"Isolation Forest flagged anomaly "
                           f"(score {anomaly_score:.3f}) within nominal range"),
                reading=reading.to_dict(),
            )

        return Decision(
            timestamp=reading.timestamp,
            action="CONTINUE",
            severity="NORMAL",
            rationale="All metrics within nominal range",
            reading=reading.to_dict(),
        )


# ---------------------------------------------------------------------
# 6. Orchestration
# ---------------------------------------------------------------------

def run_simulation(total_ticks: int = 120,
                   warmup_ticks: int = 50,
                   sleep_s: float = 0.0,
                   verbose: bool = True) -> tuple[Path, Path]:
    """Runs end-to-end. Writes telemetry CSV and decision JSONL."""
    sim = IndustrialPumpSimulator()
    detector = AnomalyDetector()
    forecaster = VibrationForecaster()
    agent = AutonomousAgent()
    syngen = SyntheticDataGenerator()

    telemetry_path = DATA_DIR / "telemetry.csv"
    decisions_path = DATA_DIR / "decisions.jsonl"

    # Warm up: collect healthy data + augment with synthetic faults
    warmup_features = []
    warmup_vibration = []
    for _ in range(warmup_ticks):
        r = sim.step()
        warmup_features.append([r.vibration_mm_s, r.temperature_c, r.pressure_bar])
        warmup_vibration.append(r.vibration_mm_s)

    # Augment training data with synthetic fault windows (generative AI)
    for fault in ["bearing_wear", "cavitation", "imbalance"]:
        for row in syngen.generate_fault_window(fault, n=12):
            warmup_features.append([row["vibration_mm_s"],
                                    row["temperature_c"],
                                    row["pressure_bar"]])

    detector.fit(warmup_features)
    forecaster.fit(warmup_vibration)

    if verbose:
        print(f"[edge] anomaly detector + forecaster trained on "
              f"{len(warmup_features)} samples "
              f"({len(warmup_features) - warmup_ticks} synthetic)")

    # Reset simulator for the live run
    sim = IndustrialPumpSimulator(seed=99)
    rolling_vib = list(warmup_vibration[-forecaster.lag:])
    REFIT_EVERY = 10  # online learning - retrain forecaster on rolling window

    csv_file = open(telemetry_path, "w", newline="")
    writer = csv.DictWriter(csv_file, fieldnames=[
        "timestamp", "device_id", "vibration_mm_s", "temperature_c",
        "pressure_bar", "rpm", "fault_mode", "anomaly_pred",
        "anomaly_score", "forecast", "action", "severity",
        "auth_ok", "report"
    ])
    writer.writeheader()

    decision_file = open(decisions_path, "w")

    actions_taken = {"CONTINUE": 0, "FLAG_FOR_REVIEW": 0,
                     "REDUCE_LOAD": 0, "SCHEDULE_MAINTENANCE": 0,
                     "EMERGENCY_SHUTDOWN": 0}

    # --- Performance instrumentation -------------------------------
    # Track end-to-end inference latency per tick (signature verify ->
    # AI inference -> decision -> generative report) and the predictive
    # lead time (how many ticks earlier SCHEDULE_MAINTENANCE fires
    # compared to when REDUCE_LOAD would have triggered on raw threshold).
    inference_latencies_ms = []
    first_schedule_tick = None
    first_reduce_load_tick = None
    # ----------------------------------------------------------------

    for tick in range(total_ticks):
        reading = sim.step()

        # Mark the start of the per-tick inference window
        t_start = time.perf_counter()

        # Sign + send (sensor -> edge gateway over insecure channel)
        payload = reading.to_dict()
        signature = sign_payload(payload)

        # Edge gateway side: verify signature
        auth_ok = verify_payload(payload, signature)
        if not auth_ok:
            if verbose:
                print(f"[edge] DROPPED tick {tick}: HMAC verification failed")
            continue

        # Run AI pipeline
        features = [reading.vibration_mm_s,
                    reading.temperature_c,
                    reading.pressure_bar]
        pred, ascore = detector.score(features)
        rolling_vib.append(reading.vibration_mm_s)
        if len(rolling_vib) > 60:
            rolling_vib = rolling_vib[-60:]
        # Online learning: refit forecaster periodically on the recent window
        if tick > 0 and tick % REFIT_EVERY == 0 and len(rolling_vib) >= 25:
            forecaster.fit(rolling_vib)
        forecast = forecaster.forecast(rolling_vib)

        # Autonomous decision
        decision = agent.decide(reading, pred, ascore, forecast)
        actions_taken[decision.action] = actions_taken.get(decision.action, 0) + 1

        # Generative report
        report = generate_maintenance_report(reading, forecast, ascore,
                                             decision.action)

        # Stop the clock and record the per-tick latency
        t_end = time.perf_counter()
        inference_latencies_ms.append((t_end - t_start) * 1000.0)

        # Track first occurrence of each escalating action for lead-time math
        if first_schedule_tick is None and decision.action == "SCHEDULE_MAINTENANCE":
            first_schedule_tick = tick
        if first_reduce_load_tick is None and decision.action == "REDUCE_LOAD":
            first_reduce_load_tick = tick

        writer.writerow({
            **payload,
            "anomaly_pred": pred,
            "anomaly_score": round(ascore, 4),
            "forecast": round(forecast, 3) if forecast is not None else "",
            "action": decision.action,
            "severity": decision.severity,
            "auth_ok": auth_ok,
            "report": report,
        })

        decision_file.write(json.dumps({
            "tick": tick,
            "decision": asdict(decision),
            "report": report,
        }) + "\n")

        if verbose and decision.action != "CONTINUE":
            print(f"[tick {tick:3d}] {decision.severity:8s} "
                  f"-> {decision.action} :: {decision.rationale}")

        if sleep_s > 0:
            time.sleep(sleep_s)

    # Inject one tampered packet to demonstrate the security layer working
    if verbose:
        bad_payload = {"vibration_mm_s": 999.0, "device_id": DEVICE_ID,
                       "timestamp": datetime.now(timezone.utc).isoformat()}
        bad_sig = "deadbeef" * 8
        ok = verify_payload(bad_payload, bad_sig)
        print(f"[edge] tampered-packet test: auth_ok={ok} (expected False)")

    # --- Reachability test for FLAG_FOR_REVIEW -----------------------
    # FLAG_FOR_REVIEW fires when the Isolation Forest sees an out-of-
    # distribution reading whose vibration is still inside the nominal
    # band. This combination is rare in the canonical seed, so we
    # construct one synthetic reading to prove the code path is reachable
    # and explainable. This is post-run instrumentation only - it does
    # NOT modify the action counts above.
    if verbose:
        oob_reading = SensorReading(
            timestamp=datetime.now(timezone.utc).isoformat(),
            device_id=DEVICE_ID,
            vibration_mm_s=2.4,        # within nominal band
            temperature_c=95.0,        # but very high temp -> out of distribution
            pressure_bar=2.0,          # and unusually low pressure
            rpm=1750,
            fault_mode="perturbation_test",
        )
        oob_features = [oob_reading.vibration_mm_s,
                        oob_reading.temperature_c,
                        oob_reading.pressure_bar]
        oob_pred, oob_score = detector.score(oob_features)
        oob_decision = agent.decide(oob_reading, oob_pred, oob_score, None)
        print(f"[edge] FLAG_FOR_REVIEW reachability test: "
              f"action={oob_decision.action}, anomaly_score={oob_score:.3f}")
    # ------------------------------------------------------------------

    csv_file.close()
    decision_file.close()

    if verbose:
        print("\n=== Simulation summary ===")
        for a, c in actions_taken.items():
            print(f"  {a:25s} {c}")

        # --- Quantitative performance metrics ------------------------
        if inference_latencies_ms:
            arr = np.asarray(inference_latencies_ms)
            print(f"\n=== Edge inference latency (per tick, end-to-end) ===")
            print(f"  samples: {len(arr)}")
            print(f"  mean:    {arr.mean():.3f} ms")
            print(f"  median:  {np.median(arr):.3f} ms")
            print(f"  p95:     {np.percentile(arr, 95):.3f} ms")
            print(f"  max:     {arr.max():.3f} ms")

        print(f"\n=== Predictive lead time ===")
        if first_schedule_tick is not None and first_reduce_load_tick is not None:
            lead = first_reduce_load_tick - first_schedule_tick
            print(f"  First SCHEDULE_MAINTENANCE: tick {first_schedule_tick}")
            print(f"  First REDUCE_LOAD        : tick {first_reduce_load_tick}")
            print(f"  Predictive lead time     : {lead} ticks")
            print(f"  (the agent acted {lead} ticks before a pure threshold rule would have)")
        elif first_schedule_tick is not None:
            print(f"  First SCHEDULE_MAINTENANCE: tick {first_schedule_tick}")
            print(f"  REDUCE_LOAD never triggered in this run")
        else:
            print(f"  Predictive rule did not fire in this run")

        print(f"\nTelemetry log:  {telemetry_path}")
        print(f"Decision log:   {decisions_path}")
        # -------------------------------------------------------------

    return telemetry_path, decisions_path


if __name__ == "__main__":
    run_simulation(total_ticks=180, warmup_ticks=50, sleep_s=0.0, verbose=True)
