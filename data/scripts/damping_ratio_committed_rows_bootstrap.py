#!/usr/bin/env python3
"""Fallback analysis on committed rows only (no external code, no simulation).

Design: logs/2026-11-04-damping-ratio-ten-seed-anchors-selfreview.md, Amendment section.
Damping ratio = (full - full_anchor) / (iso - iso_baseline), baseline-subtracted on both sides,
the definition used for the 0.10 / 0.2245 / 0.4172 points.
Independent per-configuration seed bootstrap (configurations have different seed counts).
The coupling-only uniform baseline (+0.0064) has no committed per-seed rows; it is held fixed.

Usage: python3 data/scripts/damping_ratio_committed_rows_bootstrap.py
"""
import json
import random
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "data" / "derived"
OUT = D / "damping-ratio-committed-rows-bootstrap-summary.json"
ISO_BASELINE = 0.0064
N, SEED = 10_000, 20261104


def load(name):
    return json.loads((D / name).read_text())


rec = load("external-coupling-v2-recalibrated-beta-check-summary.json")
rows = {
    "full_anchor": [r["edge_gain_gap"] for r in rec["anchor"]["rows"]],
    "full_4172": [r["edge_gain_gap"] for r in rec["design"]["rows"]],
    "iso_4172": [r["edge_gain_gap"] for r in load("external-coupling-only-beta-curvature-check-summary.json")["rows"]],
    "full_48": [r["edge_gain_gap"] for r in load("external-coupling-v2-limit-point-full-pipeline-more-seeds-check-summary.json")["all_rows"]],
    "iso_48": [r["edge_gain_gap"] for r in load("external-coupling-only-beta-limit-point-more-seeds-check-summary.json")["all_rows"]],
}
m = {k: statistics.fmean(v) for k, v in rows.items()}


def ratio(mm, b):
    return (mm[f"full_{b}"] - mm["full_anchor"]) / (mm[f"iso_{b}"] - ISO_BASELINE)


point = {b: ratio(m, b) for b in ("4172", "48")}
on_file_0330 = (m["full_48"] - m["full_anchor"]) / m["iso_48"]  # the inconsistent 2026-10-11 form
rng = random.Random(SEED)
boots = {"4172": [], "48": [], "D": []}
for _ in range(N):
    mm = {k: statistics.fmean(rng.choice(v) for _ in v) for k, v in rows.items()}
    a, b = ratio(mm, "4172"), ratio(mm, "48")
    boots["4172"].append(a); boots["48"].append(b); boots["D"].append(a - b)


def ci(xs):
    s = sorted(xs)
    return [s[int(0.025 * N)], s[int(0.975 * N) - 1]]


summary = {
    "design_log": "logs/2026-11-04-damping-ratio-ten-seed-anchors-selfreview.md (Amendment)",
    "rows": rows, "means": m, "seed_counts": {k: len(v) for k, v in rows.items()},
    "iso_baseline_fixed": ISO_BASELINE,
    "ratio_point": point,
    "ratio_048_as_reported_2026_10_11_raw_denominator": on_file_0330,
    "bootstrap": {"n": N, "seed": SEED, "ci95": {k: ci(v) for k, v in boots.items()},
                  "share_D_le_0": sum(x <= 0 for x in boots["D"]) / N},
    "D_point": point["4172"] - point["48"],
}
summary["dip_resolved_as_real"] = summary["bootstrap"]["ci95"]["D"][0] > 0
OUT.write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({k: summary[k] for k in ("means", "ratio_point", "ratio_048_as_reported_2026_10_11_raw_denominator", "bootstrap", "D_point", "dip_resolved_as_real")}, indent=1))
