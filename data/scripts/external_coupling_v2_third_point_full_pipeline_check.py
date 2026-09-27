#!/usr/bin/env python3
"""Third full-pipeline data point (beta_A=0.10), per
logs/2026-09-27-claude-damping-ratio-third-point-selfreview.md.

Runs the full pipeline (coupling + boundary-shift-v2 + top-up) at
beta_A=0.10 -- the anchor (beta_A=beta_B=0.5) is already known
(-0.05575) and is not re-run here.

Usage:
    python data/scripts/external_coupling_v2_third_point_full_pipeline_check.py <units_repo>
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

OUT_JSON = ROOT / "data" / "derived" / "external-coupling-v2-third-point-full-pipeline-check-summary.json"

DESIGN = {"beta_a": 0.10, "beta_b": 0.5}
KNOWN_ANCHOR_MEAN_GAP = -0.05574867702325522


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
        transformed = prior.transform(atomic_cache[i], token_labels, DESIGN["beta_a"], DESIGN["beta_b"], pilot_post_seeds[i])
        expanded = [base.expand(t) for t in transformed]
        ev = base.evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
        gap, a_edge, b_edge = prior.section_edge_gain_gap(expanded, line_lengths, currier_labels_by_line, scale)
        rows.append({"cipher_seed": pilot_cipher_seeds[i], "all_six_pass": ev["all_six_pass"], "edge_gain_gap": gap})
        log(f"seed {pilot_cipher_seeds[i]}: all_six_pass={ev['all_six_pass']} gap={gap:.4f}")

    mean_gap = sum(r["edge_gain_gap"] for r in rows) / len(rows)
    baseline_corrected = mean_gap - KNOWN_ANCHOR_MEAN_GAP
    log(f"design (beta_a={DESIGN['beta_a']}) raw mean_edge_gain_gap={mean_gap:.5f}")
    log(f"baseline-corrected (design - known anchor {KNOWN_ANCHOR_MEAN_GAP:.5f}) = {baseline_corrected:.5f}")

    summary = {
        "design_log": "logs/2026-09-27-claude-damping-ratio-third-point-selfreview.md",
        "design": {"beta_a": DESIGN["beta_a"], "beta_b": DESIGN["beta_b"], "rows": rows, "mean_edge_gain_gap": mean_gap},
        "known_anchor_mean_gap": KNOWN_ANCHOR_MEAN_GAP,
        "baseline_corrected_gap": baseline_corrected,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
