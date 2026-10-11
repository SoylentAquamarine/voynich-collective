#!/usr/bin/env python3
"""7 additional seeds (positions 4-10 of the manifest) at beta_A=0.48,
full-pipeline (coupling + boundary-shift-v2 + top-up) configuration, per
the open question named in
logs/2026-09-28-claude-limit-point-more-seeds-selfreview.md: "the
full-pipeline denominator side was not re-run with a larger seed count...
a fully stabilized damping-ratio estimate at this point would still need
that."

Mirrors external_coupling_only_beta_limit_point_more_seeds_check.py's own
pattern exactly, but for the full-pipeline side instead of the isolated
coupling-only side.

The anchor (beta_A=beta_B=0.5, -0.05574867702325522) is already known at
3 seeds and is not re-run here, same as the original 3-seed full-pipeline
check.

Usage:
    python data/scripts/external_coupling_v2_limit_point_full_pipeline_more_seeds_check.py <units_repo>
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "data" / "scripts"))
import external_coupling_v2_section_aware_preregistered as base
import external_coupling_v2_section_varying_beta_check as prior

OUT_JSON = ROOT / "data" / "derived" / "external-coupling-v2-limit-point-full-pipeline-more-seeds-check-summary.json"

DESIGN = {"beta_a": 0.48, "beta_b": 0.5}
KNOWN_ANCHOR_MEAN_GAP = -0.05574867702325522
SEED_COUNT = 10  # total, including the original 3 (42, 179, 316) already run

# Already-known results for seeds 0-2 (42, 179, 316), from the original
# 3-seed full-pipeline run (external-coupling-v2-limit-point-full-pipeline-check-summary.json)
PRIOR_ROWS = [
    {"cipher_seed": 42, "all_six_pass": True, "edge_gain_gap": -0.026347724765073965},
    {"cipher_seed": 179, "all_six_pass": True, "edge_gain_gap": -0.06561963332524123},
    {"cipher_seed": 316, "all_six_pass": True, "edge_gain_gap": -0.10056926574799929},
]


def main() -> None:
    units_repo = Path(sys.argv[1]).resolve()
    started = time.time()

    def log(m):
        print(f"[{time.time()-started:7.1f}s] {m}", flush=True)

    (source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args,
     token_labels, line_lengths, currier_labels_by_line, real_gap) = base.setup(units_repo, log)

    manifest = json.loads(base.COUPLING_V2_MANIFEST_PATH.read_text(encoding="utf-8"))
    cipher_seeds = manifest["seeds"]["cipher"][:SEED_COUNT]
    post_seeds = manifest["seeds"]["postprocessor"][:SEED_COUNT]

    new_rows = []
    for i in range(3, SEED_COUNT):
        cs, ps = cipher_seeds[i], post_seeds[i]
        encrypted = cipher.encrypt(letters, cs)
        atomic = [headlines.collapse(t) for t in encrypted["tokens"]]
        transformed = prior.transform(atomic, token_labels, DESIGN["beta_a"], DESIGN["beta_b"], ps)
        expanded = [base.expand(t) for t in transformed]
        ev = base.evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
        gap, a_edge, b_edge = prior.section_edge_gain_gap(expanded, line_lengths, currier_labels_by_line, scale)
        new_rows.append({"cipher_seed": cs, "all_six_pass": ev["all_six_pass"], "edge_gain_gap": gap})
        log(f"seed {cs}: all_six_pass={ev['all_six_pass']} gap={gap:.4f}")

    all_rows = PRIOR_ROWS + new_rows
    mean_gap_3 = sum(r["edge_gain_gap"] for r in PRIOR_ROWS) / 3
    mean_gap_10 = sum(r["edge_gain_gap"] for r in all_rows) / len(all_rows)
    stdev_3 = statistics.stdev(r["edge_gain_gap"] for r in PRIOR_ROWS)
    stdev_10 = statistics.stdev(r["edge_gain_gap"] for r in all_rows)

    baseline_corrected_3 = mean_gap_3 - KNOWN_ANCHOR_MEAN_GAP
    baseline_corrected_10 = mean_gap_10 - KNOWN_ANCHOR_MEAN_GAP

    # Isolated (numerator) side, already measured at 10 seeds in the prior cycle
    isolated_mean_10seed = -0.0467  # from external-coupling-only-beta-limit-point-more-seeds-check-summary.json

    damping_ratio_3 = baseline_corrected_3 / isolated_mean_10seed if isolated_mean_10seed else float("nan")
    damping_ratio_10 = baseline_corrected_10 / isolated_mean_10seed if isolated_mean_10seed else float("nan")

    log(f"3-seed mean: {mean_gap_3:.5f} (stdev {stdev_3:.5f}), baseline-corrected {baseline_corrected_3:.5f}")
    log(f"10-seed mean: {mean_gap_10:.5f} (stdev {stdev_10:.5f}), baseline-corrected {baseline_corrected_10:.5f}")
    log(f"damping ratio (3-seed full-pipeline / 10-seed isolated): {damping_ratio_3:.4f}")
    log(f"damping ratio (10-seed full-pipeline / 10-seed isolated): {damping_ratio_10:.4f}")

    summary = {
        "design_log": "logs/2026-10-11-claude-limit-point-full-pipeline-more-seeds-selfreview.md",
        "beta_a": DESIGN["beta_a"], "beta_b": DESIGN["beta_b"],
        "prior_rows": PRIOR_ROWS,
        "new_rows": new_rows,
        "all_rows": all_rows,
        "mean_gap_3seed": mean_gap_3,
        "stdev_3seed": stdev_3,
        "mean_gap_10seed": mean_gap_10,
        "stdev_10seed": stdev_10,
        "known_anchor_mean_gap": KNOWN_ANCHOR_MEAN_GAP,
        "baseline_corrected_gap_3seed": baseline_corrected_3,
        "baseline_corrected_gap_10seed": baseline_corrected_10,
        "isolated_mean_10seed": isolated_mean_10seed,
        "damping_ratio_3seed_fullpipeline_over_10seed_isolated": damping_ratio_3,
        "damping_ratio_10seed_fullpipeline_over_10seed_isolated": damping_ratio_10,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
