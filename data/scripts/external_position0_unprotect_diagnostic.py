#!/usr/bin/env python3
"""Diagnostic (not a preregistered mechanism test): does letting the substitution
top-up occasionally touch position 0 (currently structurally protected -- see
logs/2026-09-22-claude-coupling-causal-concentration.md, which found coupling's
causal signal lives specifically at position 0) reduce hybrid-shift-v2-substitution's
residual order-share excess, without dropping edge-prediction below its required
threshold (which currently passes with large margin, 0.91-0.94 vs required >=0.15)?

Cheap single-config check before any preregistration: same already-calibrated
nu_sub=0.01, only the substitution top-up's position range is widened to include 0.

Usage:
    python data/scripts/external_position0_unprotect_diagnostic.py <units_repo>
"""

from __future__ import annotations

import importlib
import json
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-position0-unprotect-diagnostic-summary.json"

sys.path.insert(0, str(ROOT / "data" / "scripts"))
from external_hybrid_shift_v2_substitution_novelty_null_audit import (  # noqa: E402
    ATOMIC_ALPHABET, COLD_START_TOKENS, SPARSE_CONTEXT_MIN, SIX_CRITERIA,
    apply_coupling, apply_boundary_shift_v2, expand, evaluate_replicate,
)


def apply_substitution_topup_unprotected(shifted_tokens, nu_sub, rng):
    """Identical to apply_substitution_topup EXCEPT positions range is [0, n-1]
    instead of [1, n-1] -- position 0 is no longer structurally protected."""
    output = []
    emitted = set()
    unigram_freq = Counter()
    bigram_freq = defaultdict(Counter)
    bigram_total = Counter()
    tokens_emitted = 0

    for token in shifted_tokens:
        candidate = list(token)
        candidate_str = "".join(candidate)
        if candidate_str in emitted and len(candidate) >= 2 and rng.random() < nu_sub:
            n = len(candidate)
            start_pos = rng.randrange(0, n)
            positions = [(start_pos + k) % n for k in range(n)]
            use_cold_start = tokens_emitted < COLD_START_TOKENS
            found = False
            for pos in positions:
                original = candidate[pos]
                alternatives = [a for a in ATOMIC_ALPHABET if a != original]
                if use_cold_start:
                    start_step = rng.randrange(1, 26)
                    order = [alternatives[(start_step - 1 + k) % 25] for k in range(25)]
                else:
                    if pos == 0:
                        preceding = None
                    else:
                        preceding = candidate[pos - 1]
                    if preceding is not None and bigram_total.get(preceding, 0) >= SPARSE_CONTEXT_MIN:
                        context = bigram_freq[preceding]
                        keyed = [(-context.get(a, 0), rng.random(), a) for a in alternatives]
                    else:
                        keyed = [(-unigram_freq.get(a, 0), rng.random(), a) for a in alternatives]
                    keyed.sort()
                    order = [a for _, _, a in keyed]
                for alt in order:
                    trial = candidate.copy()
                    trial[pos] = alt
                    trial_str = "".join(trial)
                    if trial_str not in emitted:
                        candidate_str = trial_str
                        found = True
                        break
                if found:
                    break
        output.append(candidate_str)
        emitted.add(candidate_str)
        prev_char = None
        for ch in candidate_str:
            unigram_freq[ch] += 1
            if prev_char is not None:
                bigram_freq[prev_char][ch] += 1
                bigram_total[prev_char] += 1
            prev_char = ch
        tokens_emitted += 1
    return output


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

    tables = json.loads((bundle.parent / "data" / "controls" / "naibbe" / "naibbe_tables.json").read_text(encoding="utf-8"))
    cipher = naibbe_module.NaibbeCipher(tables, deck="deck_52", ambiguity_rule="v1")
    words = naibbe_module.caesar_words(_attack_lib)
    letters = "".join(words)

    args = SimpleNamespace(skip_attack=True, skip_crossing=True, shuffles=100, extra_k=[])

    cipher_seeds = [42, 179, 316, 453, 590]
    post_seeds = [7100042, 7100179, 7100316, 7100453, 7100590]

    results = []
    for cs, ps in zip(cipher_seeds, post_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic = [headlines.collapse(t) for t in encrypted["tokens"]]
        rng = random.Random(ps)
        coupled = apply_coupling(atomic, 0.5, rng)
        shifted = apply_boundary_shift_v2(coupled, 1.0, rng)
        topped = apply_substitution_topup_unprotected(shifted, 0.01, rng)
        expanded = [expand(t) for t in topped]
        ev = evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
        results.append({"cipher_seed": cs, **{k: ev[k] for k in
                        ("H1", "H2", "token_order_share", "hapax_share_of_types",
                         "edge_gain_bits_per_boundary", "edge_positive_blocks", "all_six_pass", "criteria_pass")}})
        log(f"seed {cs}: order_share={ev['token_order_share']:.4f} (ceiling 0.02) "
            f"edge={ev['edge_gain_bits_per_boundary']:.4f} (floor 0.15) "
            f"H1={ev['H1']:.4f} H2={ev['H2']:.4f} hapax={ev['hapax_share_of_types']:.4f} "
            f"all_six_pass={ev['all_six_pass']}")

    mean_order = sum(r["token_order_share"] for r in results) / len(results)
    mean_edge = sum(r["edge_gain_bits_per_boundary"] for r in results) / len(results)
    summary = {"replicates": results, "mean_order_share": mean_order, "mean_edge_gain": mean_edge}
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")
    log(f"mean order_share={mean_order:.4f} (vs primary's 0.0234, ceiling 0.02) mean edge={mean_edge:.4f} (floor 0.15)")


if __name__ == "__main__":
    main()
