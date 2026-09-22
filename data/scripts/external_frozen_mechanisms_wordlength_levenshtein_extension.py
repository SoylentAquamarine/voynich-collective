#!/usr/bin/env python3
"""Criterion-(b) check extension (see
logs/2026-09-22-claude-criterion-b-extension-precommitment.md, written before this script
was run): direct follow-up to PR #43's frozen-mechanisms check, adding two more
already-existing, unrelated-purpose statistics that were simply not read out yet --

1. Word-length mean/stdev (Statistician pass 1, 2026-09-19, basic corpus description,
   no mechanism-design purpose). Real Voynich overall: mean 5.03, stdev 1.89.
2. Adjacent-token Levenshtein<=1 excess and exact-identical excess -- both already computed
   by the SAME adjacent_similarity() call used for the Levenshtein<=2 check in PR #43; only
   the lev_le2 field was read out there.

Same two already-frozen mechanisms (boundary-shift-v2, hybrid-shift-v2-substitution),
same seeds, same non-circularity discipline: neither statistic played any role in
calibrating either design.

Usage:
    python data/scripts/external_frozen_mechanisms_wordlength_levenshtein_extension.py <units_repo>
"""

from __future__ import annotations

import importlib
import json
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-frozen-mechanisms-wordlength-levenshtein-extension-summary.json"

sys.path.insert(0, str(ROOT / "data" / "scripts"))
from external_boundary_shift_v2_novelty_null_audit import (  # noqa: E402
    apply_coupling as bsv2_coupling, apply_boundary_shift_v2, expand as bsv2_expand,
)
from external_hybrid_shift_v2_substitution_novelty_null_audit import (  # noqa: E402
    apply_coupling as hyb_coupling, apply_boundary_shift_v2 as hyb_shift_v2,
    apply_substitution_topup, expand as hyb_expand,
)

REAL_WORD_LENGTH_MEAN = 5.03
REAL_WORD_LENGTH_STDEV = 1.89
REAL_LEV_LE1_EXCESS = None  # filled in from the real-Voynich sanity check at runtime
REAL_IDENTICAL_EXCESS = None


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

    # Sanity check: reproduce real Voynich's own word-length and lev_le1/identical stats
    # directly from the same template every mechanism is compared against.
    real_words = [w for line in observed for w in line]
    real_lengths = [len(w) for w in real_words]
    real_mean = sum(real_lengths) / len(real_lengths)
    real_stdev = statistics.pstdev(real_lengths)
    real_sim = selfcitation_module.adjacent_similarity(observed, shuffles=200, seed=20260922)
    real_lev_le1_excess = real_sim["lev_le1"] - real_sim["lev_le1_shuffled"]
    real_identical_excess = real_sim["identical"] - real_sim["identical_shuffled"]
    log(f"real Voynich sanity check: word_length mean={real_mean:.4f} stdev={real_stdev:.4f} "
        f"(reference {REAL_WORD_LENGTH_MEAN}/{REAL_WORD_LENGTH_STDEV}) "
        f"lev_le1_excess={100*real_lev_le1_excess:+.2f}pp identical_excess={100*real_identical_excess:+.2f}pp")

    tables = json.loads((bundle.parent / "data" / "controls" / "naibbe" / "naibbe_tables.json").read_text(encoding="utf-8"))
    cipher = naibbe_module.NaibbeCipher(tables, deck="deck_52", ambiguity_rule="v1")
    words = naibbe_module.caesar_words(_attack_lib)
    letters = "".join(words)

    cipher_seeds = [42, 179, 316, 453, 590]

    def measure(lines):
        words_flat = [w for line in lines for w in line]
        lengths = [len(w) for w in words_flat]
        mean = sum(lengths) / len(lengths)
        stdev = statistics.pstdev(lengths)
        sim = selfcitation_module.adjacent_similarity(lines, shuffles=200, seed=20260922)
        return {
            "word_length_mean": mean, "word_length_stdev": stdev,
            "lev_le1_excess": sim["lev_le1"] - sim["lev_le1_shuffled"],
            "identical_excess": sim["identical"] - sim["identical_shuffled"],
        }

    results = {"boundary_shift_v2_primary": [], "hybrid_shift_v2_substitution_primary": []}

    for cs in cipher_seeds:
        encrypted = cipher.encrypt(letters, cs)
        atomic = [headlines.collapse(t) for t in encrypted["tokens"]]

        rng = random.Random(8000000 + cs)
        coupled = bsv2_coupling(atomic, 0.5, rng)
        shifted = apply_boundary_shift_v2(coupled, 0.2, rng)
        expanded = [bsv2_expand(t) for t in shifted]
        lines = scale.wrap_to_lengths(expanded, line_lengths)
        m = measure(lines)
        results["boundary_shift_v2_primary"].append({"cipher_seed": cs, **m})
        log(f"boundary-shift-v2 seed {cs}: word_length mean={m['word_length_mean']:.4f} stdev={m['word_length_stdev']:.4f} "
            f"lev_le1_excess={100*m['lev_le1_excess']:+.2f}pp identical_excess={100*m['identical_excess']:+.2f}pp")

        rng = random.Random(7100000 + cs)
        coupled = hyb_coupling(atomic, 0.5, rng)
        shifted = hyb_shift_v2(coupled, 1.0, rng)
        topped = apply_substitution_topup(shifted, 0.01, rng)
        expanded = [hyb_expand(t) for t in topped]
        lines = scale.wrap_to_lengths(expanded, line_lengths)
        m = measure(lines)
        results["hybrid_shift_v2_substitution_primary"].append({"cipher_seed": cs, **m})
        log(f"hybrid-shift-v2-substitution seed {cs}: word_length mean={m['word_length_mean']:.4f} stdev={m['word_length_stdev']:.4f} "
            f"lev_le1_excess={100*m['lev_le1_excess']:+.2f}pp identical_excess={100*m['identical_excess']:+.2f}pp")

    def summarize(rows):
        return {k: sum(r[k] for r in rows) / len(rows) for k in
                ("word_length_mean", "word_length_stdev", "lev_le1_excess", "identical_excess")}

    summary = {
        "real_voynich_reference": {
            "word_length_mean": real_mean, "word_length_stdev": real_stdev,
            "lev_le1_excess": real_lev_le1_excess, "identical_excess": real_identical_excess,
            "provenance": "word-length: Statistician pass 1 (2026-09-19, unrelated purpose). lev_le1/identical: same adjacent_similarity() call as PR #43's lev_le2 check, fields simply not read out there.",
        },
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
