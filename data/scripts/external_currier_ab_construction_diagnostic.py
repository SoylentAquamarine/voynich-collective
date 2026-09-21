#!/usr/bin/env python3
"""Diagnostic (not a preregistered mechanism test): can a generator built to
DELIBERATELY vary its dosage between Currier-A-labeled and Currier-B-labeled
output sections construct a pooled character-entropy gap approaching
Voynich's real +0.278 bits (see external_currier_ab_diagnostic.py)?

Non-circularity discipline: the two dosage values (nu_A, nu_B) are NOT
chosen now to hit the target gap. They are reused, unchanged, from
bigram-novelty-null's own ALREADY-FROZEN sensitivity configurations
(weaker_novelty nu=0.1, stronger_novelty nu=0.3), established in an earlier,
unrelated design before this diagnostic existed. Whatever gap results is
reported honestly, whichever direction it falls.

Base mechanism choice: boundary-shift-v2 was considered and rejected for
this specific test, because its own nu parameter is PROVEN exactly
entropy-invariant (see PR #36) -- varying it between sections could never
move H2 at all, by construction. bigram-novelty-null's nu parameter DOES
move H2 (established in PR #30), so it is the correct base for testing
whether dosage variation alone can construct an entropy asymmetry.

Usage:
    python data/scripts/external_currier_ab_construction_diagnostic.py <units_repo>
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
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-currier-ab-construction-diagnostic-summary.json"

ATOMIC_ALPHABET = "CEIKNPSTadefgiklmnopqrstxy"
EXPAND_MAP = {"C": "ch", "E": "ee", "I": "in", "K": "ckh", "N": "iin", "P": "cph", "S": "sh", "T": "cth"}
TARGET_INITIALS = ["o", "q", "C", "S"]
COLD_START_TOKENS = 5
SPARSE_CONTEXT_MIN = 20

# Frozen, reused unchanged from bigram-novelty-null's own sensitivity configurations (PR #30).
NU_A = 0.3   # bigram-novelty-null's "stronger_novelty"
NU_B = 0.1   # bigram-novelty-null's "weaker_novelty"
NU_DEFAULT = 0.2  # bigram-novelty-null's own primary, used for unlabeled ("?") lines


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


def apply_section_varying_substitution(coupled_tokens, token_labels, nu_by_label, rng):
    """Identical bigram-conditional substitution mechanics to bigram-novelty-null,
    except nu is looked up per-token from its Currier-label section instead of
    being one global value."""
    output = []
    emitted = set()
    unigram_freq: Counter = Counter()
    bigram_freq: dict = defaultdict(Counter)
    bigram_total: Counter = Counter()
    tokens_emitted = 0

    for idx, token in enumerate(coupled_tokens):
        candidate = list(token)
        candidate_str = "".join(candidate)
        label = token_labels[idx] if idx < len(token_labels) else "?"
        nu = nu_by_label[label]
        if candidate_str in emitted and len(candidate) >= 2 and rng.random() < nu:
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
    parser.add_argument("--nu-a", type=float, default=NU_A)
    parser.add_argument("--nu-b", type=float, default=NU_B)
    parser.add_argument("--nu-default", type=float, default=NU_DEFAULT)
    parser.add_argument("--out-suffix", default="")
    parser.add_argument("--provenance", default="reused unchanged from bigram-novelty-null's own prior sensitivity configs, not chosen to match this target")
    args = parser.parse_args()
    nu_a, nu_b, nu_default = args.nu_a, args.nu_b, args.nu_default
    out_json = ROOT / "data" / "derived" / f"external-currier-ab-construction-diagnostic{args.out_suffix}-summary.json"

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

    # per-TOKEN label array, in flat-stream order, built from per-line labels
    token_labels = [label for length, label in zip(line_lengths, currier_labels_by_line) for _ in range(length)]

    real_a_words = [tok for line, label in zip(observed, currier_labels_by_line) if label == "A" for tok in line]
    real_b_words = [tok for line, label in zip(observed, currier_labels_by_line) if label == "B" for tok in line]
    real_gap = char_bigram_conditional_entropy(real_a_words) - char_bigram_conditional_entropy(real_b_words)
    log(f"real Voynich gap (sanity check): {real_gap:.4f} bits")

    tables = json.loads((bundle.parent / "data" / "controls" / "naibbe" / "naibbe_tables.json").read_text(encoding="utf-8"))
    cipher = naibbe_module.NaibbeCipher(tables, deck="deck_52", ambiguity_rule="v1")
    words = naibbe_module.caesar_words(_attack_lib)
    letters = "".join(words)

    nu_by_label = {"A": nu_a, "B": nu_b, "?": nu_default}
    log(f"frozen dosages ({args.provenance}): "
        f"nu_A={nu_a} nu_B={nu_b} nu_default={nu_default}")

    cipher_seeds = [42, 179, 316, 453, 590]
    post_seeds = [9000042, 9000179, 9000316, 9000453, 9000590]
    results = []
    for cs, ps in zip(cipher_seeds, post_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic = [headlines.collapse(t) for t in encrypted["tokens"]]
        assert len(atomic) >= len(token_labels), "generated stream shorter than the real line template"
        rng = random.Random(ps)
        coupled = apply_coupling(atomic, 0.5, rng)
        transformed = apply_section_varying_substitution(coupled, token_labels, nu_by_label, rng)
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
        "real_voynich_gap": real_gap,
        "frozen_dosages": {"nu_A": nu_a, "nu_B": nu_b, "nu_default": nu_default,
                            "provenance": args.provenance},
        "replicates": results,
        "mean_gap": mean_gap,
        "mean_gap_as_fraction_of_real": mean_gap / real_gap,
    }
    out_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {out_json}")
    log(f"mean generated gap: {mean_gap:.4f} bits ({100*mean_gap/real_gap:.1f}% of real {real_gap:.4f})")


if __name__ == "__main__":
    main()
