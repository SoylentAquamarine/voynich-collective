#!/usr/bin/env python3
"""Diagnostic (not a preregistered mechanism test): the REVERSED-assignment
follow-up to external_coupling_v3_1_section_aware_diagnostic.py. Under
coupling-v3.1's own mechanism (Naibbe + coupling-v2's identity-mapping rule at
beta=0.15, fixed + boundary-shift-v2, nu_shift=1.0, fixed), does swapping
which Currier section gets the stronger substitution top-up dosage (nu_sub)
change the sign or size of the generated pooled Currier A/B character-bigram-
entropy gap relative to the real +0.278-bit gap?

Design reasoning, result-blinding disclosure, and the honesty precommitment
are in logs/2026-09-25-claude-section-aware-coupling-v3-1-reversed-selfreview.md,
written before this script ran. Dosage values are the same two already-frozen
values as the first attempt (0.02 = coupling-v2's own "stronger_topup", 0.01 =
primary) -- only the section assignment is swapped: nu_sub_A=0.01 (was 0.02),
nu_sub_B=0.02 (was 0.01).

Usage:
    python data/scripts/external_coupling_v3_1_section_aware_reversed_diagnostic.py <units_repo>
"""

from __future__ import annotations

import importlib
import json
import math
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-coupling-v3-1-section-aware-reversed-diagnostic-summary.json"

ATOMIC_ALPHABET = "CEIKNPSTadefgiklmnopqrstxy"
EXPAND_MAP = {"C": "ch", "E": "ee", "I": "in", "K": "ckh", "N": "iin", "P": "cph", "S": "sh", "T": "cth"}
COLD_START_TOKENS = 5
SPARSE_CONTEXT_MIN = 20

# Reused unchanged from coupling-v3.1's own frozen manifest (beta) and from
# coupling-v2's own already-executed sensitivity grid (the two nu_sub values).
# ASSIGNMENT REVERSED relative to the first section-aware attempt.
BETA_FIXED = 0.15
NU_SHIFT_FIXED = 1.0
NU_SUB_A = 0.01   # coupling-v3.1's own (and coupling-v2's own) primary value -- was 0.02 in the first attempt
NU_SUB_B = 0.02   # coupling-v2's own "stronger_topup" sensitivity value -- was 0.01 in the first attempt
NU_SUB_DEFAULT = 0.01


def expand(atomic_token: str) -> str:
    return "".join(EXPAND_MAP.get(a, a) for a in atomic_token)


def char_bigram_conditional_entropy(words: list[str]) -> float:
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


def apply_coupling_v3(atomic_tokens: list[str], beta: float, rng: random.Random) -> list[str]:
    """Identical to coupling-v3/v3.1: target = prev_last, 26 distinct possible targets."""
    output: list[str] = []
    prev_last = None
    for i, token in enumerate(atomic_tokens):
        candidate = list(token)
        if i > 0 and rng.random() < beta:
            candidate[0] = prev_last
        candidate_str = "".join(candidate)
        output.append(candidate_str)
        prev_last = candidate_str[-1]
    return output


def apply_boundary_shift_v2(coupled_tokens: list[str], nu_shift: float, rng: random.Random) -> list[str]:
    """Unchanged from external_coupling_v3_1_corrected_selection_audit.py."""
    result: list[str] = []
    emitted: set[str] = set()
    i = 0
    n = len(coupled_tokens)
    while i < n:
        tok_i = coupled_tokens[i]
        eligible = tok_i in emitted and i + 1 < n
        if eligible and rng.random() < nu_shift:
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
                result.append(tok_i)
                result.append(tok_j)
                emitted.add(tok_i)
                emitted.add(tok_j)
            i += 2
        else:
            result.append(tok_i)
            emitted.add(tok_i)
            i += 1
    return result


def apply_section_varying_substitution_topup(shifted_tokens, token_labels, nu_by_label, rng):
    """Same mechanics as apply_substitution_topup, except nu_sub is looked up
    per-token from that token's Currier-label section instead of being one
    global value -- unchanged from the first section-aware diagnostic."""
    output: list[str] = []
    emitted: set[str] = set()
    unigram_freq: Counter = Counter()
    bigram_freq: dict[str, Counter] = defaultdict(Counter)
    bigram_total: Counter = Counter()
    tokens_emitted = 0

    for idx, token in enumerate(shifted_tokens):
        candidate = list(token)
        candidate_str = "".join(candidate)
        label = token_labels[idx] if idx < len(token_labels) else "?"
        nu_sub = nu_by_label[label]
        if candidate_str in emitted and len(candidate) >= 2 and rng.random() < nu_sub:
            n = len(candidate)
            start_pos = rng.randrange(1, n)
            positions = [(start_pos - 1 + k) % (n - 1) + 1 for k in range(n - 1)]
            use_cold_start = tokens_emitted < COLD_START_TOKENS
            found = False
            for pos in positions:
                original = candidate[pos]
                alternatives = [a for a in ATOMIC_ALPHABET if a != original]
                if use_cold_start:
                    start_step = rng.randrange(1, 26)
                    order = [alternatives[(start_step - 1 + k) % 25] for k in range(25)]
                else:
                    preceding = candidate[pos - 1]
                    if bigram_total.get(preceding, 0) >= SPARSE_CONTEXT_MIN:
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
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("units_repo", type=Path)
    args = parser.parse_args()

    started = time.time()

    def log(m):
        print(f"[{time.time()-started:7.1f}s] {m}", flush=True)

    units_repo = args.units_repo.resolve()
    sys.path.insert(0, str(units_repo / "analysis"))
    naibbe_module = importlib.import_module("reproduce_naibbe_control")
    from reproduce_space_sensitivity import parse_lines

    bundle = units_repo / "voynich_decipherment_repro_bundle"
    modules = naibbe_module.load_modules(bundle)
    _attack_lib, _attack_voynich, unit_probe, headlines, scale, _space, plant = modules

    parsed, _ = parse_lines(bundle / "voynich_calibration_sources" / "ZL3b.txt", plant.LOCUS_RE, plant.strip_markup)
    currier_labels_by_line = [line["currier"] for line in parsed]
    observed, _, _, _ = scale.load_voynich_lines(bundle, plant.LOCUS_RE, plant.collapse, plant.strip_markup)
    line_lengths = [len(line) for line in observed]
    assert len(line_lengths) == len(currier_labels_by_line)

    token_labels = [label for length, label in zip(line_lengths, currier_labels_by_line) for _ in range(length)]

    real_a_words = [tok for line, label in zip(observed, currier_labels_by_line) if label == "A" for tok in line]
    real_b_words = [tok for line, label in zip(observed, currier_labels_by_line) if label == "B" for tok in line]
    real_gap = char_bigram_conditional_entropy(real_a_words) - char_bigram_conditional_entropy(real_b_words)
    log(f"real Voynich gap (sanity check): {real_gap:.4f} bits")

    tables = json.loads((bundle.parent / "data" / "controls" / "naibbe" / "naibbe_tables.json").read_text(encoding="utf-8"))
    cipher = naibbe_module.NaibbeCipher(tables, deck="deck_52", ambiguity_rule="v1")
    words = naibbe_module.caesar_words(_attack_lib)
    letters = "".join(words)

    nu_by_label = {"A": NU_SUB_A, "B": NU_SUB_B, "?": NU_SUB_DEFAULT}
    log(f"frozen dosages (reused unchanged, assignment REVERSED from the first attempt): "
        f"nu_sub_A={NU_SUB_A} nu_sub_B={NU_SUB_B} nu_sub_default={NU_SUB_DEFAULT} "
        f"beta={BETA_FIXED} (fixed, not varied by section) nu_shift={NU_SHIFT_FIXED}")

    # coupling-v3.1's own frozen seed pairs (cipher, postprocessor), reused unchanged.
    cipher_seeds = [42, 179, 316, 453, 590]
    post_seeds = [7100042, 7100179, 7100316, 7100453, 7100590]
    results = []
    for cs, ps in zip(cipher_seeds, post_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic = [headlines.collapse(t) for t in encrypted["tokens"]]
        assert len(atomic) >= len(token_labels), "generated stream shorter than the real line template"
        rng = random.Random(ps)
        coupled = apply_coupling_v3(atomic, BETA_FIXED, rng)
        shifted = apply_boundary_shift_v2(coupled, NU_SHIFT_FIXED, rng)
        transformed = apply_section_varying_substitution_topup(shifted, token_labels, nu_by_label, rng)
        expanded = [expand(t) for t in transformed]

        gen_lines = scale.wrap_to_lengths(expanded, line_lengths)
        gen_a_words = [tok for line, label in zip(gen_lines, currier_labels_by_line) if label == "A" for tok in line]
        gen_b_words = [tok for line, label in zip(gen_lines, currier_labels_by_line) if label == "B" for tok in line]
        gen_a_h2 = char_bigram_conditional_entropy(gen_a_words)
        gen_b_h2 = char_bigram_conditional_entropy(gen_b_words)
        gap = gen_a_h2 - gen_b_h2
        results.append({"cipher_seed": cs, "postprocessor_seed": ps,
                         "A_H2": gen_a_h2, "B_H2": gen_b_h2, "gap": gap})
        log(f"seed {cs}: A={gen_a_h2:.4f} B={gen_b_h2:.4f} gap={gap:.4f} "
            f"(real gap {real_gap:.4f}, achieved {100*gap/real_gap:.1f}% of real magnitude)")

    mean_gap = sum(r["gap"] for r in results) / len(results)
    summary = {
        "base_mechanism": "coupling-v3.1 (beta=0.15 fixed) + boundary-shift-v2 (nu_shift=1.0 fixed) + section-varying substitution top-up (REVERSED assignment)",
        "real_voynich_gap": real_gap,
        "frozen_dosages": {
            "nu_sub_A": NU_SUB_A, "nu_sub_B": NU_SUB_B, "nu_sub_default": NU_SUB_DEFAULT,
            "beta_fixed": BETA_FIXED, "nu_shift_fixed": NU_SHIFT_FIXED,
            "provenance": "same two values as the first section-aware attempt (coupling-v2's own already-executed sensitivity grid: 0.02=stronger_topup, 0.01=primary), assignment swapped (A=0.01, B=0.02, was A=0.02, B=0.01) -- the reversal named as the untested next step in the first attempt's own report",
        },
        "replicates": results,
        "mean_gap": mean_gap,
        "mean_gap_as_fraction_of_real": mean_gap / real_gap,
        "first_attempt_mean_gap_for_comparison": None,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")
    log(f"mean generated gap: {mean_gap:.4f} bits ({100*mean_gap/real_gap:.1f}% of real {real_gap:.4f})")


if __name__ == "__main__":
    main()
