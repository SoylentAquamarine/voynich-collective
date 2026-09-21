#!/usr/bin/env python3
"""Diagnostic (not a preregistered mechanism test): does a generator that passes
the six frozen criteria also reproduce Voynich's real Currier A/B pooled
character-entropy asymmetry (H2 ~2.20 bits for A vs ~1.98 for B, Statistician
pass 1) when its output is split using the REAL per-line Currier labels?

The generation mechanisms tested in this project (Naibbe, boundary coupling,
every novelty-rule variant, boundary-shift-v2) are homogeneous stochastic
processes with no notion of "page" or "Currier label" -- nothing in them
should make one arbitrary sub-segment of the output differ from another
except ordinary seed noise. The null expectation is therefore that splitting
GENERATED output by the real A/B line assignment (used here only as an
external splitting key, not fed into generation) should show a near-zero
gap, unlike real Voynich's own real, disclosed asymmetry.

This is a post-hoc analysis of already-generated, already-frozen replicate
data (boundary-shift-v2's frozen seeds) using an already-established metric
(char_bigram_conditional_entropy, from statistician_pass1.py) against an
already-published reference value (Statistician pass 1). It does not
preregister a new mechanism, freeze new criteria, or make any pass/fail
claim -- it reports a comparison.

Usage:
    python data/scripts/external_currier_ab_diagnostic.py <units_repo>
"""

from __future__ import annotations

import importlib
import json
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-currier-ab-diagnostic-summary.json"
OUT_REPORT = ROOT / "data" / "derived" / "external-currier-ab-diagnostic-report.md"

ATOMIC_ALPHABET = "CEIKNPSTadefgiklmnopqrstxy"
EXPAND_MAP = {"C": "ch", "E": "ee", "I": "in", "K": "ckh", "N": "iin", "P": "cph", "S": "sh", "T": "cth"}
TARGET_INITIALS = ["o", "q", "C", "S"]


def expand(atomic_token: str) -> str:
    return "".join(EXPAND_MAP.get(a, a) for a in atomic_token)


def char_bigram_conditional_entropy(words: list[str]) -> float:
    import math
    pair_counts: Counter = Counter()
    prefix_counts: Counter = Counter()
    for w in words:
        for i in range(1, len(w)):
            prefix, nxt = w[i - 1], w[i]
            pair_counts[(prefix, nxt)] += 1
            prefix_counts[prefix] += 1
    total = sum(pair_counts.values())
    if total == 0:
        return 0.0
    h = 0.0
    for (prefix, nxt), c in pair_counts.items():
        p_joint = c / total
        p_cond = c / prefix_counts[prefix]
        h -= p_joint * math.log2(p_cond)
    return h


def apply_coupling(atomic_tokens, beta, rng):
    output = []
    prev_last = None
    for i, token in enumerate(atomic_tokens):
        candidate = list(token)
        if i > 0 and rng.random() < beta:
            target = TARGET_INITIALS[ATOMIC_ALPHABET.index(prev_last) % 4]
            candidate[0] = target
        candidate_str = "".join(candidate)
        output.append(candidate_str)
        prev_last = candidate_str[-1]
    return output


def apply_boundary_shift_v2(coupled_tokens, nu, rng):
    result = []
    emitted = set()
    i = 0
    n = len(coupled_tokens)
    while i < n:
        tok_i = coupled_tokens[i]
        eligible = tok_i in emitted and i + 1 < n
        if eligible and rng.random() < nu:
            tok_j = coupled_tokens[i + 1]
            combined = tok_i + tok_j
            L = len(combined)
            original_split = len(tok_i)
            start_pos = rng.randrange(1, L)
            positions = [(start_pos - 1 + k) % (L - 1) + 1 for k in range(L - 1)]
            positions = [p for p in positions if p != original_split]
            found = False
            for p in positions:
                left, right = combined[:p], combined[p:]
                left_new = left not in emitted
                right_new = right not in emitted
                if left_new != right_new:
                    result.append(left); result.append(right)
                    emitted.add(left); emitted.add(right)
                    found = True
                    break
            if not found:
                for p in positions:
                    left, right = combined[:p], combined[p:]
                    if left not in emitted or right not in emitted:
                        result.append(left); result.append(right)
                        emitted.add(left); emitted.add(right)
                        found = True
                        break
            if not found:
                result.append(tok_i); result.append(tok_j)
                emitted.add(tok_i); emitted.add(tok_j)
            i += 2
        else:
            result.append(tok_i)
            emitted.add(tok_i)
            i += 1
    return result


def main() -> None:
    import argparse
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument("units_repo", type=Path)
    parser.add_argument("--replicates", type=int, default=5)
    args = parser.parse_args()
    units_repo = args.units_repo.resolve()

    started = time.time()

    def log(msg):
        print(f"[{time.time()-started:7.1f}s] {msg}", flush=True)

    sys.path.insert(0, str(units_repo / "analysis"))
    naibbe_module = importlib.import_module("reproduce_naibbe_control")
    from reproduce_space_sensitivity import parse_lines

    bundle = units_repo / "voynich_decipherment_repro_bundle"
    modules = naibbe_module.load_modules(bundle)
    _attack_lib, _attack_voynich, unit_probe, headlines, scale, _space, plant = modules

    # Real per-line Currier labels, in the EXACT same order as observed/line_lengths
    parsed, _skipped = parse_lines(
        bundle / "voynich_calibration_sources" / "ZL3b.txt", plant.LOCUS_RE, plant.strip_markup
    )
    currier_labels = [line["currier"] for line in parsed]
    log(f"parsed {len(parsed)} real lines with Currier labels "
        f"(A={currier_labels.count('A')}, B={currier_labels.count('B')}, ?={currier_labels.count('?')})")

    observed, _certain_only, _grouped, _skipped2 = scale.load_voynich_lines(
        bundle, plant.LOCUS_RE, plant.collapse, plant.strip_markup
    )
    assert len(observed) == len(currier_labels), (
        f"line count mismatch: observed={len(observed)} vs currier_labels={len(currier_labels)}"
    )
    line_lengths = [len(line) for line in observed]

    # Sanity check: reproduce the known real Voynich A vs B pooled H2 gap (Statistician pass 1: ~2.20 vs ~1.98)
    real_a_words = [tok for line, label in zip(observed, currier_labels) if label == "A" for tok in line]
    real_b_words = [tok for line, label in zip(observed, currier_labels) if label == "B" for tok in line]
    real_a_h2 = char_bigram_conditional_entropy(real_a_words)
    real_b_h2 = char_bigram_conditional_entropy(real_b_words)
    log(f"SANITY CHECK -- real Voynich pooled H2: A={real_a_h2:.4f} ({len(real_a_words)} words) "
        f"B={real_b_h2:.4f} ({len(real_b_words)} words) gap={real_a_h2 - real_b_h2:.4f}")

    tables = json.loads((bundle.parent / "data" / "controls" / "naibbe" / "naibbe_tables.json").read_text(encoding="utf-8"))
    cipher = naibbe_module.NaibbeCipher(tables, deck="deck_52", ambiguity_rule="v1")
    words = naibbe_module.caesar_words(_attack_lib)
    letters = "".join(words)

    import random
    sys.path.insert(0, str(ROOT / "data" / "scripts"))
    from external_bigram_novelty_null_audit import transform_replicate as bigram_transform

    cipher_seeds = [42, 179, 316, 453, 590][: args.replicates]
    shift_post_seeds = [8000042, 8000179, 8000316, 8000453, 8000590][: args.replicates]
    bigram_post_seeds = [5000042, 5000179, 5000316, 5000453, 5000590][: args.replicates]

    def gap_for(expanded_tokens):
        gen_lines = scale.wrap_to_lengths(expanded_tokens, line_lengths)
        a_words = [tok for line, label in zip(gen_lines, currier_labels) if label == "A" for tok in line]
        b_words = [tok for line, label in zip(gen_lines, currier_labels) if label == "B" for tok in line]
        a_h2 = char_bigram_conditional_entropy(a_words)
        b_h2 = char_bigram_conditional_entropy(b_words)
        return a_h2, b_h2, a_h2 - b_h2, len(a_words), len(b_words)

    mechanisms: dict[str, list] = {"baseline_naibbe": [], "bigram_novelty_null": [], "boundary_shift_v2": []}
    for cs, sps, bps in zip(cipher_seeds, shift_post_seeds, bigram_post_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic = [headlines.collapse(t) for t in encrypted["tokens"]]

        a_h2, b_h2, gap, na, nb = gap_for([expand(t) for t in atomic])
        mechanisms["baseline_naibbe"].append({"cipher_seed": cs, "A_H2": a_h2, "B_H2": b_h2, "gap": gap,
                                               "A_words": na, "B_words": nb})
        log(f"baseline_naibbe seed {cs}: A={a_h2:.4f} B={b_h2:.4f} gap={gap:.4f}")

        transformed = bigram_transform(atomic, beta=0.5, nu=0.2, seed=bps)
        a_h2, b_h2, gap, na, nb = gap_for([expand(t) for t in transformed])
        mechanisms["bigram_novelty_null"].append({"cipher_seed": cs, "postprocessor_seed": bps,
                                                    "A_H2": a_h2, "B_H2": b_h2, "gap": gap, "A_words": na, "B_words": nb})
        log(f"bigram_novelty_null seed {cs}: A={a_h2:.4f} B={b_h2:.4f} gap={gap:.4f}")

        rng = random.Random(sps)
        coupled = apply_coupling(atomic, 0.5, rng)
        shifted = apply_boundary_shift_v2(coupled, 0.2, rng)
        a_h2, b_h2, gap, na, nb = gap_for([expand(t) for t in shifted])
        mechanisms["boundary_shift_v2"].append({"cipher_seed": cs, "postprocessor_seed": sps,
                                                  "A_H2": a_h2, "B_H2": b_h2, "gap": gap, "A_words": na, "B_words": nb})
        log(f"boundary_shift_v2 seed {cs}: A={a_h2:.4f} B={b_h2:.4f} gap={gap:.4f}")

    summary = {
        "real_voynich": {"A_H2": real_a_h2, "B_H2": real_b_h2, "gap": real_a_h2 - real_b_h2,
                          "A_words": len(real_a_words), "B_words": len(real_b_words)},
    }
    for name, results in mechanisms.items():
        mean_gap = sum(r["gap"] for r in results) / len(results)
        summary[name] = {"replicates": results, "mean_gap": mean_gap}
        log(f"{name}: mean gap={mean_gap:.4f} (range {min(r['gap'] for r in results):.4f} to {max(r['gap'] for r in results):.4f})")

    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")
    log(f"REAL gap: {real_a_h2 - real_b_h2:.4f} bits")


if __name__ == "__main__":
    main()
