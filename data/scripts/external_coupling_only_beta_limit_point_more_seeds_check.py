#!/usr/bin/env python3
"""7 additional seeds (positions 4-10 of the manifest) at beta_A=0.48,
isolated coupling-only configuration, per
logs/2026-09-28-claude-limit-point-more-seeds-selfreview.md.

Departs explicitly from the standard 3-seed pilot convention to test
whether a larger sample recovers a more stable damping-ratio numerator
estimate near the beta_A=beta_B boundary.

Usage:
    python data/scripts/external_coupling_only_beta_limit_point_more_seeds_check.py <units_repo>
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "data" / "scripts"))
import external_coupling_v2_section_aware_preregistered as base
import external_coupling_v2_section_varying_beta_check as beta_check

OUT_JSON = ROOT / "data" / "derived" / "external-coupling-only-beta-limit-point-more-seeds-check-summary.json"

BETA_A = 0.48
BETA_B = 0.5
UNIFORM_COUPLING_ONLY_BASELINE = 0.0064
SEED_COUNT = 10  # total, including the original 3 (42, 179, 316) already run


def transform_coupling_only_section_varying(atomic_tokens, token_labels, seed):
    rng = random.Random(seed)
    beta_by_label = {"A": BETA_A, "B": BETA_B, "?": BETA_B}
    coupled = beta_check.apply_section_varying_coupling(atomic_tokens, token_labels, beta_by_label, rng)
    return coupled


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

    # Already-known results for seeds 0-2 (42, 179, 316), from the prior 3-seed run
    prior_rows = [
        {"cipher_seed": 42, "edge_gain_gap": -0.0175},
        {"cipher_seed": 179, "edge_gain_gap": -0.0219},
        {"cipher_seed": 316, "edge_gain_gap": -0.0812},
    ]

    new_rows = []
    for i in range(3, SEED_COUNT):
        cs, ps = cipher_seeds[i], post_seeds[i]
        encrypted = cipher.encrypt(letters, cs)
        atomic = [headlines.collapse(t) for t in encrypted["tokens"]]
        transformed = transform_coupling_only_section_varying(atomic, token_labels, ps)
        expanded = [base.expand(t) for t in transformed]
        gap, a_edge, b_edge = beta_check.section_edge_gain_gap(expanded, line_lengths, currier_labels_by_line, scale)
        new_rows.append({"cipher_seed": cs, "edge_gain_gap": gap})
        log(f"seed {cs}: gap={gap:.4f}")

    all_rows = prior_rows + new_rows
    mean_gap_3 = sum(r["edge_gain_gap"] for r in prior_rows) / 3
    mean_gap_10 = sum(r["edge_gain_gap"] for r in all_rows) / len(all_rows)
    import statistics
    stdev_3 = statistics.stdev(r["edge_gain_gap"] for r in prior_rows)
    stdev_10 = statistics.stdev(r["edge_gain_gap"] for r in all_rows)

    log(f"3-seed mean: {mean_gap_3:.4f} (stdev {stdev_3:.4f})")
    log(f"10-seed mean: {mean_gap_10:.4f} (stdev {stdev_10:.4f})")
    log(f"10-seed net effect: {mean_gap_10 - UNIFORM_COUPLING_ONLY_BASELINE:.4f}")

    summary = {
        "design_log": "logs/2026-09-28-claude-limit-point-more-seeds-selfreview.md",
        "beta_a": BETA_A, "beta_b": BETA_B,
        "prior_rows": prior_rows,
        "new_rows": new_rows,
        "all_rows": all_rows,
        "mean_gap_3seed": mean_gap_3,
        "stdev_3seed": stdev_3,
        "mean_gap_10seed": mean_gap_10,
        "stdev_10seed": stdev_10,
        "uniform_beta_coupling_only_baseline": UNIFORM_COUPLING_ONLY_BASELINE,
        "net_effect_10seed": mean_gap_10 - UNIFORM_COUPLING_ONLY_BASELINE,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
