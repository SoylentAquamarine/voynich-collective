#!/usr/bin/env python3
"""Criterion-(b) check: BPE dependence-gap curve SHAPE (see
logs/2026-09-22-claude-bpe-curve-shape-precommitment.md, written before this script was
run). The six frozen criteria only constrain the curve's minimum checkpoint location and
the k64 gap magnitude -- never the curve's full shape (its values at 0 and 16 merges too).
Real Voynich's own held-out-quire curve (0/16/32/64 merges: 1.686/1.423/1.379/1.490 bits)
was published in data/derived/external-units-paper-audit.md (2026-09-19, reproducing an
external paper, a year before either frozen mechanism existed) and has never been compared
against either mechanism's own curve shape.

Sanity-checks the methodology first: reproduces real Voynich's own curve directly through
the same battery() call every mechanism-test script uses, before trusting any comparison
to the externally-published reference (same discipline as the word-length check, which
found a real representation mismatch worth disclosing).

Usage:
    python data/scripts/external_frozen_mechanisms_bpe_curve_shape_check.py <units_repo>
"""

from __future__ import annotations

import importlib
import json
import random
import sys
import time
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-frozen-mechanisms-bpe-curve-shape-check-summary.json"

sys.path.insert(0, str(ROOT / "data" / "scripts"))
from external_boundary_shift_v2_novelty_null_audit import (  # noqa: E402
    apply_coupling as bsv2_coupling, apply_boundary_shift_v2, expand as bsv2_expand,
)
from external_hybrid_shift_v2_substitution_novelty_null_audit import (  # noqa: E402
    apply_coupling as hyb_coupling, apply_boundary_shift_v2 as hyb_shift_v2,
    apply_substitution_topup, expand as hyb_expand,
)

EXTERNAL_PAPER_REFERENCE_CURVE = {"0": 1.686, "16": 1.423, "32": 1.379, "64": 1.490}


def main() -> None:
    units_repo = Path(sys.argv[1]).resolve()
    started = time.time()

    def log(m):
        print(f"[{time.time()-started:7.1f}s] {m}", flush=True)

    sys.path.insert(0, str(units_repo / "analysis"))
    naibbe_module = importlib.import_module("reproduce_naibbe_control")
    bundle = units_repo / "voynich_decipherment_repro_bundle"
    modules = naibbe_module.load_modules(bundle)
    _attack_lib, _attack_voynich, unit_probe, headlines, scale, _space, plant = modules

    voy_tokens = naibbe_module.voynich_entropy_tokens(bundle, headlines)
    observed, _, _, _ = scale.load_voynich_lines(bundle, plant.LOCUS_RE, plant.collapse, plant.strip_markup)
    line_lengths = [len(line) for line in observed]
    pooled = unit_probe.voynich_lines()
    targets = {
        "entropy_tokens": len(voy_tokens),
        "line_lengths": line_lengths,
        "bpe_glyphs": sum(len(w) for ln in pooled for w in ln),
    }
    args = SimpleNamespace(skip_attack=True, skip_crossing=True, shuffles=100, extra_k=[])

    def curve_for(tokens):
        result = naibbe_module.battery("replicate", tokens, None, set(), targets, args, modules, lambda m: None, [])
        c = result["bpe"]["curve"]
        return {k: c[k]["gap"] for k in c}

    # Sanity check: real Voynich's own tokens through the same battery() pipeline.
    real_words = [w for line in observed for w in line]
    real_curve = curve_for(real_words)
    log(f"real Voynich curve (this pipeline): {real_curve}")
    log(f"external paper's own reference curve: {EXTERNAL_PAPER_REFERENCE_CURVE}")

    tables = json.loads((bundle.parent / "data" / "controls" / "naibbe" / "naibbe_tables.json").read_text(encoding="utf-8"))
    cipher = naibbe_module.NaibbeCipher(tables, deck="deck_52", ambiguity_rule="v1")
    words = naibbe_module.caesar_words(_attack_lib)
    letters = "".join(words)

    cipher_seeds = [42, 179, 316, 453, 590]
    results = {"boundary_shift_v2_primary": [], "hybrid_shift_v2_substitution_primary": []}

    for cs in cipher_seeds:
        encrypted = cipher.encrypt(letters, cs)
        atomic = [headlines.collapse(t) for t in encrypted["tokens"]]

        rng = random.Random(8000000 + cs)
        coupled = bsv2_coupling(atomic, 0.5, rng)
        shifted = apply_boundary_shift_v2(coupled, 0.2, rng)
        expanded = [bsv2_expand(t) for t in shifted]
        curve = curve_for(expanded)
        results["boundary_shift_v2_primary"].append({"cipher_seed": cs, "curve": curve})
        log(f"boundary-shift-v2 seed {cs}: {curve}")

        rng = random.Random(7100000 + cs)
        coupled = hyb_coupling(atomic, 0.5, rng)
        shifted = hyb_shift_v2(coupled, 1.0, rng)
        topped = apply_substitution_topup(shifted, 0.01, rng)
        expanded = [hyb_expand(t) for t in topped]
        curve = curve_for(expanded)
        results["hybrid_shift_v2_substitution_primary"].append({"cipher_seed": cs, "curve": curve})
        log(f"hybrid-shift-v2-substitution seed {cs}: {curve}")

    def summarize(rows):
        keys = rows[0]["curve"].keys()
        return {k: sum(r["curve"][k] for r in rows) / len(rows) for k in keys}

    summary = {
        "external_paper_reference_curve": EXTERNAL_PAPER_REFERENCE_CURVE,
        "real_voynich_curve_this_pipeline": real_curve,
        "replicates": results,
        "boundary_shift_v2_primary_mean_curve": summarize(results["boundary_shift_v2_primary"]),
        "hybrid_shift_v2_substitution_primary_mean_curve": summarize(results["hybrid_shift_v2_substitution_primary"]),
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")
    log(f"boundary-shift-v2 mean curve: {summary['boundary_shift_v2_primary_mean_curve']}")
    log(f"hybrid-shift-v2-substitution mean curve: {summary['hybrid_shift_v2_substitution_primary_mean_curve']}")


if __name__ == "__main__":
    main()
