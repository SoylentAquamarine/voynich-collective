#!/usr/bin/env python3
"""Runs the recalibrated section-varying beta_A (0.4172) through the FULL
pipeline (coupling-v2 + boundary-shift-v2 + substitution top-up), per
logs/2026-09-26-claude-coupling-v2-recalibrated-beta-selfreview.md.

beta_A=0.4172 was predicted from a linear-interpolation model combining the
already-measured damping ratio (full-pipeline vs. coupling-only-isolated
beta effect) and an assumed-linear-in-beta_A isolated effect, disclosed and
precommitted before this ran. The correct comparison is the
baseline-corrected gap (design - anchor), not the raw design gap against
the anchor threshold, since the anchor here is known in advance to fail
(boundary-shift artifact, already characterized).

Usage:
    python data/scripts/external_coupling_v2_recalibrated_beta_check.py <units_repo>
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "data" / "scripts"))
import external_coupling_v2_section_aware_preregistered as base
import external_coupling_v2_section_varying_beta_check as prior

OUT_JSON = ROOT / "data" / "derived" / "external-coupling-v2-recalibrated-beta-check-summary.json"

ANCHOR = {"beta_a": 0.5, "beta_b": 0.5}
DESIGN = {"beta_a": 0.4172, "beta_b": 0.5}
PREDICTED_MEAN_GAP = -0.13121  # from the linear-interpolation model, see selfreview log


def main() -> None:
    units_repo = Path(sys.argv[1]).resolve()
    started = time.time()

    def log(m):
        print(f"[{time.time()-started:7.1f}s] {m}", flush=True)

    (source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args,
     token_labels, line_lengths, currier_labels_by_line, real_gap) = base.setup(units_repo, log)

    real_edge_gap_json = ROOT / "data" / "derived" / "external-currier-ab-real-edge-gain-stats-summary.json"
    real_edge = json.loads(real_edge_gap_json.read_text(encoding="utf-8"))
    real_edge_gain_gap = real_edge["currier_a"]["gain_bits_per_boundary"] - real_edge["currier_b"]["gain_bits_per_boundary"]
    log(f"real edge-gain gap (A-B): {real_edge_gain_gap:.5f} bits/boundary")

    manifest = json.loads(base.COUPLING_V2_MANIFEST_PATH.read_text(encoding="utf-8"))
    pilot_cipher_seeds = manifest["seeds"]["cipher"][:3]
    pilot_post_seeds = manifest["seeds"]["postprocessor"][:3]

    atomic_cache = {}
    for i, cs in enumerate(pilot_cipher_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic_cache[i] = [headlines.collapse(t) for t in encrypted["tokens"]]

    def run_config(name, beta_a, beta_b):
        rows = []
        for i in range(3):
            transformed = prior.transform(atomic_cache[i], token_labels, beta_a, beta_b, pilot_post_seeds[i])
            expanded = [base.expand(t) for t in transformed]
            ev = base.evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
            gap, a_edge, b_edge = prior.section_edge_gain_gap(expanded, line_lengths, currier_labels_by_line, scale)
            rows.append({
                "cipher_seed": pilot_cipher_seeds[i], "all_six_pass": ev["all_six_pass"],
                "H1": ev["H1"], "H2": ev["H2"],
                "pooled_edge_gain": ev["edge_gain_bits_per_boundary"],
                "a_edge_gain": a_edge["gain_bits_per_boundary"], "b_edge_gain": b_edge["gain_bits_per_boundary"],
                "edge_gain_gap": gap,
            })
            log(f"{name} seed {pilot_cipher_seeds[i]}: all_six_pass={ev['all_six_pass']} "
                f"pooled_edge={ev['edge_gain_bits_per_boundary']:.4f} "
                f"A_edge={a_edge['gain_bits_per_boundary']:.4f} B_edge={b_edge['gain_bits_per_boundary']:.4f} "
                f"gap={gap:.4f}")
        mean_gap = sum(r["edge_gain_gap"] for r in rows) / len(rows)
        all_pass = all(r["all_six_pass"] for r in rows)
        return {"name": name, "beta_a": beta_a, "beta_b": beta_b, "rows": rows,
                 "mean_edge_gain_gap": mean_gap, "all_three_seeds_pass_six_criteria": all_pass}

    anchor_result = run_config("anchor", ANCHOR["beta_a"], ANCHOR["beta_b"])
    log(f"anchor (beta=0.5/0.5, known boundary-shift baseline): mean_gap={anchor_result['mean_edge_gain_gap']:.5f}")

    design_result = run_config("design", DESIGN["beta_a"], DESIGN["beta_b"])
    log(f"design (beta_a={DESIGN['beta_a']}) raw mean_edge_gain_gap={design_result['mean_edge_gain_gap']:.5f}")

    baseline_corrected_gap = design_result["mean_edge_gain_gap"] - anchor_result["mean_edge_gain_gap"]
    pct_of_real = 100 * baseline_corrected_gap / real_edge_gain_gap
    prediction_error_pct = 100 * (baseline_corrected_gap - PREDICTED_MEAN_GAP) / PREDICTED_MEAN_GAP
    log(f"baseline-corrected design gap (design - anchor) = {baseline_corrected_gap:.5f} "
        f"({pct_of_real:.1f}% of real {real_edge_gain_gap:.5f})")
    log(f"predicted was {PREDICTED_MEAN_GAP:.5f}; actual vs predicted error = {prediction_error_pct:.1f}%")

    summary = {
        "design_log": "logs/2026-09-26-claude-coupling-v2-recalibrated-beta-selfreview.md",
        "real_edge_gain_gap_a_minus_b": real_edge_gain_gap,
        "predicted_baseline_corrected_gap": PREDICTED_MEAN_GAP,
        "anchor": anchor_result,
        "design": design_result,
        "baseline_corrected_design_gap": baseline_corrected_gap,
        "baseline_corrected_pct_of_real": pct_of_real,
        "prediction_error_pct": prediction_error_pct,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
