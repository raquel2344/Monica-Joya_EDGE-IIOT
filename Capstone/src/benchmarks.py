"""
SentinelEdge — Performance Benchmarks
======================================
Runs the same end-to-end pipeline used in production, but with timing
instrumentation around each stage. Reports p50 / p95 / p99 latencies
in milliseconds for the security check, the AI inference, the agent
decision, and the full per-tick pipeline.

Usage (from the Capstone/ folder):
    python src/benchmarks.py

Writes a results file to data/benchmarks.json and prints a table.
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sentinel_edge import (
    AnomalyDetector,
    AutonomousAgent,
    IndustrialPumpSimulator,
    SyntheticDataGenerator,
    VibrationForecaster,
    generate_maintenance_report,
    sign_payload,
    verify_payload,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def percentile(values: list[float], p: float) -> float:
    """Return the p-th percentile of values (p in 0..100)."""
    if not values:
        return 0.0
    s = sorted(values)
    k = (len(s) - 1) * (p / 100.0)
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    frac = k - lo
    return s[lo] * (1 - frac) + s[hi] * frac


def fmt_ms(seconds: float) -> str:
    return f"{seconds * 1000:.3f} ms"


def main():
    print("\n=== SentinelEdge Performance Benchmark ===\n")

    # -----------------------------------------------------------------
    # 1. Training time (warm up: edge AI fit on healthy + synthetic)
    # -----------------------------------------------------------------
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

    t0 = time.perf_counter()
    detector.fit(feats)
    detector_train_s = time.perf_counter() - t0

    t0 = time.perf_counter()
    forecaster.fit(vibs)
    forecaster_train_s = time.perf_counter() - t0

    print(f"Training (one-time, runs at startup):")
    print(f"  Isolation Forest fit ({len(feats)} samples):     {fmt_ms(detector_train_s)}")
    print(f"  Linear Regression forecaster fit ({len(vibs)} samples):  "
          f"{fmt_ms(forecaster_train_s)}")
    print()

    # -----------------------------------------------------------------
    # 2. Per-stage and per-tick latency over a full simulation run
    # -----------------------------------------------------------------
    sim = IndustrialPumpSimulator(seed=99)
    agent = AutonomousAgent()
    rolling_vib = list(vibs[-forecaster.lag:])

    n_ticks = 200
    sec_times, ai_times, decision_times, report_times, total_times = [], [], [], [], []

    for tick in range(n_ticks):
        tick_t0 = time.perf_counter()

        reading = sim.step()
        payload = reading.to_dict()

        # Security stage: sign + verify (production gateway path)
        s0 = time.perf_counter()
        signature = sign_payload(payload)
        ok = verify_payload(payload, signature)
        sec_times.append(time.perf_counter() - s0)

        # AI inference stage: anomaly + forecast
        a0 = time.perf_counter()
        feat = [reading.vibration_mm_s, reading.temperature_c, reading.pressure_bar]
        pred, ascore = detector.score(feat)
        rolling_vib.append(reading.vibration_mm_s)
        if len(rolling_vib) > 60:
            rolling_vib = rolling_vib[-60:]
        if tick > 0 and tick % 10 == 0 and len(rolling_vib) >= 25:
            forecaster.fit(rolling_vib)
        forecast = forecaster.forecast(rolling_vib)
        ai_times.append(time.perf_counter() - a0)

        # Decision stage
        d0 = time.perf_counter()
        decision = agent.decide(reading, pred, ascore, forecast)
        decision_times.append(time.perf_counter() - d0)

        # Generative report stage
        r0 = time.perf_counter()
        _ = generate_maintenance_report(reading, forecast, ascore, decision.action)
        report_times.append(time.perf_counter() - r0)

        total_times.append(time.perf_counter() - tick_t0)

    # -----------------------------------------------------------------
    # 3. Build report
    # -----------------------------------------------------------------
    stages = {
        "Security (sign + verify)": sec_times,
        "AI inference (anomaly + forecast)": ai_times,
        "Decision (agent policy)": decision_times,
        "Generative report (template)": report_times,
        "Full per-tick pipeline": total_times,
    }

    print(f"Per-stage latency (over {n_ticks} ticks):")
    print(f"  {'Stage':<38} {'p50':>12} {'p95':>12} {'p99':>12} {'mean':>12}")
    print(f"  {'-'*38} {'-'*12} {'-'*12} {'-'*12} {'-'*12}")
    out_table = []
    for name, vals in stages.items():
        p50 = percentile(vals, 50)
        p95 = percentile(vals, 95)
        p99 = percentile(vals, 99)
        mean = statistics.mean(vals)
        print(f"  {name:<38} {fmt_ms(p50):>12} {fmt_ms(p95):>12} "
              f"{fmt_ms(p99):>12} {fmt_ms(mean):>12}")
        out_table.append({
            "stage": name,
            "p50_ms": round(p50 * 1000, 3),
            "p95_ms": round(p95 * 1000, 3),
            "p99_ms": round(p99 * 1000, 3),
            "mean_ms": round(mean * 1000, 3),
        })

    print()
    headroom = 250.0  # Streamlit default tick = 250 ms
    full_p95_ms = percentile(total_times, 95) * 1000
    print(f"Dashboard tick interval (configurable):  250 ms")
    print(f"Per-tick pipeline p95:                   {full_p95_ms:.3f} ms")
    print(f"Headroom (250 - p95):                    {headroom - full_p95_ms:.3f} ms "
          f"(~{(1 - full_p95_ms/headroom)*100:.1f}% of budget free)")

    # -----------------------------------------------------------------
    # 4. Save JSON for the journal
    # -----------------------------------------------------------------
    results = {
        "host": "user-machine",
        "n_ticks": n_ticks,
        "training_time_ms": {
            "isolation_forest_fit": round(detector_train_s * 1000, 3),
            "linear_regression_fit": round(forecaster_train_s * 1000, 3),
        },
        "stage_latency_ms": out_table,
        "dashboard_tick_interval_ms": 250,
        "headroom_ms": round(headroom - full_p95_ms, 3),
        "headroom_pct": round((1 - full_p95_ms/headroom)*100, 1),
    }
    out_path = DATA_DIR / "benchmarks.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to: {out_path}")
    print("\n👉 Send the table above to Claude so the numbers can go into the journal.\n")


if __name__ == "__main__":
    main()
