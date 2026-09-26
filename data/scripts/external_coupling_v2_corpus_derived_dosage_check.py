#!/usr/bin/env python3
"""Checks the two corpus-statistic-derived nu_sub pairs named in
logs/2026-09-26-claude-coupling-v2-corpus-derived-dosage-selfreview.md,
using coupling-v2's own 3 pilot seeds. Reuses the exact mechanism functions
from external_coupling_v2_section_aware_preregistered.py unchanged.

Design 1 (repetition-rate-derived): nu_sub_A=0.01155, nu_sub_B=0.01
Design 2 (mean-length-derived): nu_sub_A=0.01364, nu_sub_B=0.01

Usage:
    python data/scripts/external_coupling_v2_corpus_derived_dosage_check.py <units_repo>
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "data" / "scripts"))
import external_coupling_v2_section_aware_preregistered as base

OUT_JSON = ROOT / "data" / "derived" / "external-coupling-v2-corpus-derived-dosage-check-summary.json"

DESIGNS = [
    {"name": "repetition_rate_derived", "nu_sub_a": 0.01155, "nu_sub_b": 0.01},
    {"name": "mean_length_derived", "nu_sub_a": 0.01364, "nu_sub_b": 0.01},
]


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
    log(f"pilot seeds: cipher={pilot_cipher_seeds} postprocessor={pilot_post_seeds}")

    atomic_cache = {}
    for i, cs in enumerate(pilot_cipher_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic_cache[i] = [headlines.collapse(t) for t in encrypted["tokens"]]

    results = []
    for design in DESIGNS:
        seed_rows = []
        for i in range(3):
            transformed = base.transform_replicate(
                atomic_cache[i], token_labels, design["nu_sub_a"], design["nu_sub_b"], pilot_post_seeds[i]
            )
            expanded = [base.expand(t) for t in transformed]
            ev = base.evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
            gap = base.section_gap(expanded, line_lengths, currier_labels_by_line, scale)
            seed_rows.append({"cipher_seed": pilot_cipher_seeds[i], "all_six_pass": ev["all_six_pass"],
                               "H2": ev["H2"], "gap": gap})
            log(f"{design['name']} seed {pilot_cipher_seeds[i]}: all_six_pass={ev['all_six_pass']} "
                f"H2={ev['H2']:.4f} gap={gap:.4f}")
        mean_gap = sum(r["gap"] for r in seed_rows) / len(seed_rows)
        all_pass = all(r["all_six_pass"] for r in seed_rows)
        results.append({
            "design": design["name"], "nu_sub_a": design["nu_sub_a"], "nu_sub_b": design["nu_sub_b"],
            "seed_rows": seed_rows, "all_three_seeds_pass_six_criteria": all_pass,
            "mean_gap": mean_gap, "mean_gap_as_fraction_of_real": mean_gap / real_gap,
        })
        log(f"{design['name']}: mean_gap={mean_gap:.4f} ({100*mean_gap/real_gap:.2f}% of real) "
            f"all_pass={all_pass}")

    summary = {
        "design_log": "logs/2026-09-26-claude-coupling-v2-corpus-derived-dosage-selfreview.md",
        "real_gap": real_gap,
        "predicted_outcome": "small, negative, wrong-signed gap close to -6% of the real gap",
        "results": results,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
