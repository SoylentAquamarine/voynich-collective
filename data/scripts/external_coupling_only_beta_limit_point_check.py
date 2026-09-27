#!/usr/bin/env python3
"""Isolated coupling-only check at beta_A=0.48 (much closer to beta_B=0.5
than any prior point), per
logs/2026-09-28-claude-damping-ratio-limit-point-selfreview.md.

Usage:
    python data/scripts/external_coupling_only_beta_limit_point_check.py <units_repo>
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

OUT_JSON = ROOT / "data" / "derived" / "external-coupling-only-beta-limit-point-check-summary.json"

BETA_A = 0.48
BETA_B = 0.5
UNIFORM_COUPLING_ONLY_BASELINE = 0.0064


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
    pilot_cipher_seeds = manifest["seeds"]["cipher"][:3]
    pilot_post_seeds = manifest["seeds"]["postprocessor"][:3]

    atomic_cache = {}
    for i, cs in enumerate(pilot_cipher_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic_cache[i] = [headlines.collapse(t) for t in encrypted["tokens"]]

    rows = []
    for i in range(3):
        transformed = transform_coupling_only_section_varying(atomic_cache[i], token_labels, pilot_post_seeds[i])
        expanded = [base.expand(t) for t in transformed]
        gap, a_edge, b_edge = beta_check.section_edge_gain_gap(expanded, line_lengths, currier_labels_by_line, scale)
        rows.append({"cipher_seed": pilot_cipher_seeds[i], "a_edge_gain": a_edge["gain_bits_per_boundary"],
                     "b_edge_gain": b_edge["gain_bits_per_boundary"], "edge_gain_gap": gap})
        log(f"seed {pilot_cipher_seeds[i]}: gap={gap:.4f}")

    mean_gap = sum(r["edge_gain_gap"] for r in rows) / len(rows)
    net_effect = mean_gap - UNIFORM_COUPLING_ONLY_BASELINE
    log(f"mean edge_gain_gap (coupling only, beta_A={BETA_A}): {mean_gap:.4f}, net effect: {net_effect:.4f}")

    summary = {
        "design_log": "logs/2026-09-28-claude-damping-ratio-limit-point-selfreview.md",
        "beta_a": BETA_A, "beta_b": BETA_B,
        "rows": rows,
        "mean_edge_gain_gap": mean_gap,
        "uniform_beta_coupling_only_baseline": UNIFORM_COUPLING_ONLY_BASELINE,
        "net_effect": net_effect,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
