#!/usr/bin/env python3
"""Follow-up to external_anchor_bias_diagnostic.py: does coupling-v2 ALONE
(uniform beta=0.5, no boundary-shift-v2, no substitution top-up) already
produce the nonzero generated edge-gain-gap? Localizes the bias further.

Usage:
    python data/scripts/external_anchor_bias_diagnostic_coupling_only.py <units_repo>
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

OUT_JSON = ROOT / "data" / "derived" / "external-anchor-bias-diagnostic-coupling-only-summary.json"

BETA_FIXED = 0.5


def transform_coupling_only(atomic_tokens, seed):
    rng = random.Random(seed)
    coupled = base.apply_coupling_v2(atomic_tokens, BETA_FIXED, rng)
    return coupled  # no boundary-shift, no substitution top-up


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
        transformed = transform_coupling_only(atomic_cache[i], pilot_post_seeds[i])
        expanded = [base.expand(t) for t in transformed]
        gap, a_edge, b_edge = beta_check.section_edge_gain_gap(expanded, line_lengths, currier_labels_by_line, scale)
        rows.append({"cipher_seed": pilot_cipher_seeds[i], "a_edge_gain": a_edge["gain_bits_per_boundary"],
                     "b_edge_gain": b_edge["gain_bits_per_boundary"], "edge_gain_gap": gap})
        log(f"seed {pilot_cipher_seeds[i]}: A_edge={a_edge['gain_bits_per_boundary']:.4f} "
            f"B_edge={b_edge['gain_bits_per_boundary']:.4f} gap={gap:.4f}")

    mean_gap = sum(r["edge_gain_gap"] for r in rows) / len(rows)
    log(f"mean edge_gain_gap (coupling only, no boundary-shift, no top-up): {mean_gap:.4f}")

    # Also check: raw Naibbe output (before ANY postprocessing) -- is the split present
    # even before coupling touches the stream at all?
    raw_rows = []
    for i in range(3):
        expanded = [base.expand(t) for t in atomic_cache[i]]
        gap, a_edge, b_edge = beta_check.section_edge_gain_gap(expanded, line_lengths, currier_labels_by_line, scale)
        raw_rows.append({"cipher_seed": pilot_cipher_seeds[i], "a_edge_gain": a_edge["gain_bits_per_boundary"],
                          "b_edge_gain": b_edge["gain_bits_per_boundary"], "edge_gain_gap": gap})
        log(f"RAW (no coupling at all) seed {pilot_cipher_seeds[i]}: "
            f"A_edge={a_edge['gain_bits_per_boundary']:.4f} B_edge={b_edge['gain_bits_per_boundary']:.4f} gap={gap:.4f}")
    raw_mean_gap = sum(r["edge_gain_gap"] for r in raw_rows) / len(raw_rows)
    log(f"mean edge_gain_gap (raw Naibbe, no postprocessing at all): {raw_mean_gap:.4f}")

    summary = {
        "design_log": "logs/2026-09-26-claude-anchor-bias-diagnostic-selfreview.md (follow-up, same precommitment)",
        "coupling_only": {"rows": rows, "mean_edge_gain_gap": mean_gap},
        "raw_no_postprocessing": {"rows": raw_rows, "mean_edge_gain_gap": raw_mean_gap},
        "boundary_shift_plus_coupling_mean_gap_for_comparison": -0.0575,
        "full_anchor_mean_gap_for_comparison": -0.05574867702325522,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
