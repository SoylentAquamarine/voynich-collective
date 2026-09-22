#!/usr/bin/env python3
"""Criterion-(b) check (see logs/2026-09-22-claude-criterion-b-precommitment.md, written
before this script was run): does either already-frozen, already-merged mechanism
(boundary-shift-v2 or hybrid-shift-v2-substitution -- both built purely to satisfy the six
criteria, neither ever calibrated against these statistics) happen to reproduce two
already-existing measurements taken for unrelated original purposes: the overall Zipf
log-log slope (Statistician pass 1, -0.9266) and the adjacent-token Levenshtein<=2 excess
over within-line shuffles (self-citation report, +1.833pp)?

Reuses zipf_slope() from data/scripts/statistician_pass1.py and adjacent_similarity() from
the external voynich-units bundle's reproduce_selfcitation_control.py directly -- no new
statistic code.

Usage:
    python data/scripts/external_frozen_mechanisms_zipf_levenshtein_check.py <units_repo>
"""

from __future__ import annotations

import importlib
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-frozen-mechanisms-zipf-levenshtein-check-summary.json"

sys.path.insert(0, str(ROOT / "data" / "scripts"))
from statistician_pass1 import zipf_slope  # noqa: E402
from external_boundary_shift_v2_novelty_null_audit import (  # noqa: E402
    apply_coupling as bsv2_coupling, apply_boundary_shift_v2, expand as bsv2_expand,
)
from external_hybrid_shift_v2_substitution_novelty_null_audit import (  # noqa: E402
    apply_coupling as hyb_coupling, apply_boundary_shift_v2 as hyb_shift_v2,
    apply_substitution_topup, expand as hyb_expand,
)

REAL_ZIPF_SLOPE = -0.9266
REAL_LEV_LE2_EXCESS = 0.018330034378581106


def main() -> None:
    units_repo = Path(sys.argv[1]).resolve()
    started = time.time()

    def log(m):
        print(f"[{time.time()-started:7.1f}s] {m}", flush=True)

    sys.path.insert(0, str(units_repo / "analysis"))
    naibbe_module = importlib.import_module("reproduce_naibbe_control")
    selfcitation_module = importlib.import_module("reproduce_selfcitation_control")
    bundle = units_repo / "voynich_decipherment_repro_bundle"
    modules = naibbe_module.load_modules(bundle)
    _attack_lib, _attack_voynich, unit_probe, headlines, scale, _space, plant = modules

    observed, _, _, _ = scale.load_voynich_lines(bundle, plant.LOCUS_RE, plant.collapse, plant.strip_markup)
    line_lengths = [len(line) for line in observed]

    tables = json.loads((bundle.parent / "data" / "controls" / "naibbe" / "naibbe_tables.json").read_text(encoding="utf-8"))
    cipher = naibbe_module.NaibbeCipher(tables, deck="deck_52", ambiguity_rule="v1")
    words = naibbe_module.caesar_words(_attack_lib)
    letters = "".join(words)

    cipher_seeds = [42, 179, 316, 453, 590]

    def measure(lines):
        words_flat = [w for line in lines for w in line]
        zs = zipf_slope(Counter(words_flat))
        sim = selfcitation_module.adjacent_similarity(lines, shuffles=200, seed=20260922)
        return {
            "zipf_slope": zs,
            "lev_le2_observed": sim["lev_le2"],
            "lev_le2_shuffled": sim["lev_le2_shuffled"],
            "lev_le2_excess": sim["lev_le2"] - sim["lev_le2_shuffled"],
        }

    results = {"boundary_shift_v2_primary": [], "hybrid_shift_v2_substitution_primary": []}

    for cs in cipher_seeds:
        encrypted = cipher.encrypt(letters, cs)
        atomic = [headlines.collapse(t) for t in encrypted["tokens"]]

        # boundary-shift-v2 primary: beta=0.5, nu=0.2, postprocessor seed convention from its own manifest
        rng = random.Random(8000000 + cs)
        coupled = bsv2_coupling(atomic, 0.5, rng)
        shifted = apply_boundary_shift_v2(coupled, 0.2, rng)
        expanded = [bsv2_expand(t) for t in shifted]
        lines = scale.wrap_to_lengths(expanded, line_lengths)
        m = measure(lines)
        results["boundary_shift_v2_primary"].append({"cipher_seed": cs, **m})
        log(f"boundary-shift-v2 seed {cs}: zipf={m['zipf_slope']:.4f} (real {REAL_ZIPF_SLOPE}) "
            f"lev_le2_excess={100*m['lev_le2_excess']:+.2f}pp (real {100*REAL_LEV_LE2_EXCESS:+.2f}pp)")

        # hybrid-shift-v2-substitution primary: beta=0.5, nu_shift=1.0, nu_sub=0.01
        rng = random.Random(7100000 + cs)
        coupled = hyb_coupling(atomic, 0.5, rng)
        shifted = hyb_shift_v2(coupled, 1.0, rng)
        topped = apply_substitution_topup(shifted, 0.01, rng)
        expanded = [hyb_expand(t) for t in topped]
        lines = scale.wrap_to_lengths(expanded, line_lengths)
        m = measure(lines)
        results["hybrid_shift_v2_substitution_primary"].append({"cipher_seed": cs, **m})
        log(f"hybrid-shift-v2-substitution seed {cs}: zipf={m['zipf_slope']:.4f} (real {REAL_ZIPF_SLOPE}) "
            f"lev_le2_excess={100*m['lev_le2_excess']:+.2f}pp (real {100*REAL_LEV_LE2_EXCESS:+.2f}pp)")

    def summarize(rows):
        return {
            "mean_zipf_slope": sum(r["zipf_slope"] for r in rows) / len(rows),
            "mean_lev_le2_excess": sum(r["lev_le2_excess"] for r in rows) / len(rows),
        }

    summary = {
        "real_voynich_reference": {"zipf_slope": REAL_ZIPF_SLOPE, "lev_le2_excess": REAL_LEV_LE2_EXCESS,
                                    "provenance": "Zipf: statistician-pass1-summary.json (2026-09-19, unrelated purpose). Lev: external-selfcitation-state-summary.json (2026-09-20, unrelated mechanism)"},
        "replicates": results,
        "boundary_shift_v2_primary_summary": summarize(results["boundary_shift_v2_primary"]),
        "hybrid_shift_v2_substitution_primary_summary": summarize(results["hybrid_shift_v2_substitution_primary"]),
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")
    log(f"boundary-shift-v2 mean: {summary['boundary_shift_v2_primary_summary']}")
    log(f"hybrid-shift-v2-substitution mean: {summary['hybrid_shift_v2_substitution_primary_summary']}")


if __name__ == "__main__":
    main()
