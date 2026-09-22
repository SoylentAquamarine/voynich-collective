#!/usr/bin/env python3
"""Diagnostic (not a preregistered mechanism test): does the hybrid-shift-v2-substitution
design's excess token-order-share predictability concentrate specifically in transitions
where the NEXT token's first character is one of the 4 coupling-target initials
(TARGET_INITIALS = ["o","q","C","S"]), versus transitions where it isn't?

Motivated by logs/2026-09-22-claude-coupling-order-interaction-reasoning.md: coupling
(beta=0.5) forces roughly half of all tokens' first character into one of only 4 values
(not the full 26-symbol alphabet), via a fixed modulus on the previous token's last
character. The hypothesis is that this 4-way collapse, not some incidental interaction,
is what the novelty mechanism (shift-v2 + substitution) reveals to the whole-token
order-share metric once it opens enough vocabulary for that metric to have resolution.

Reuses the hybrid-shift-v2-substitution script's transform functions unchanged (imported
directly, not copy-pasted) and computes a top-2000-capped, <other>-collapsed adjacent-pair
mutual information -- the same convention the project's order-share metric uses -- split
into two subsets by whether the SECOND token of each pair starts with a coupling-target
initial.

Usage:
    python data/scripts/external_coupling_order_concentration_diagnostic.py <units_repo>
"""

from __future__ import annotations

import importlib
import json
import math
import random
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-coupling-order-concentration-diagnostic-summary.json"

sys.path.insert(0, str(ROOT / "data" / "scripts"))
from external_hybrid_shift_v2_substitution_novelty_null_audit import (  # noqa: E402
    ATOMIC_ALPHABET, EXPAND_MAP, TARGET_INITIALS,
    apply_coupling, apply_boundary_shift_v2, apply_substitution_topup, expand,
)

TOP_CAP = 2000


def collapsed_mutual_information(pairs):
    """pairs: list of (left_token, right_token). Cap to top-2000 by frequency (computed
    over the right-token marginal, matching the project's order-share convention closely
    enough for a diagnostic), collapse the rest to <other>, compute I(left;right) in bits."""
    if not pairs:
        return None, 0
    right_freq = Counter(r for _, r in pairs)
    top_types = {t for t, _ in right_freq.most_common(TOP_CAP)}

    def cap(t):
        return t if t in top_types else "<other>"

    capped = [(cap(l), cap(r)) for l, r in pairs]
    joint = Counter(capped)
    left_marg = Counter(l for l, _ in capped)
    right_marg = Counter(r for _, r in capped)
    n = len(capped)
    mi = 0.0
    for (l, r), c in joint.items():
        p_lr = c / n
        p_l = left_marg[l] / n
        p_r = right_marg[r] / n
        mi += p_lr * math.log2(p_lr / (p_l * p_r))
    return mi, n


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

    tables = json.loads((bundle.parent / "data" / "controls" / "naibbe" / "naibbe_tables.json").read_text(encoding="utf-8"))
    cipher = naibbe_module.NaibbeCipher(tables, deck="deck_52", ambiguity_rule="v1")
    words = naibbe_module.caesar_words(_attack_lib)
    letters = "".join(words)

    cipher_seeds = [42, 179, 316, 453, 590]
    post_seeds = [7100042, 7100179, 7100316, 7100453, 7100590]

    results = {"primary": [], "hybrid_novelty_only": []}
    for cs, ps in zip(cipher_seeds, post_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic = [headlines.collapse(t) for t in encrypted["tokens"]]

        for name, beta in (("primary", 0.5), ("hybrid_novelty_only", 0.0)):
            rng = random.Random(ps)
            coupled = apply_coupling(atomic, beta, rng)
            shifted = apply_boundary_shift_v2(coupled, 1.0, rng)
            topped = apply_substitution_topup(shifted, 0.01, rng)
            expanded = [expand(t) for t in topped]

            pairs = list(zip(expanded, expanded[1:]))
            coupled_pairs = [(l, r) for l, r in pairs if r[0] in TARGET_INITIALS]
            other_pairs = [(l, r) for l, r in pairs if r[0] not in TARGET_INITIALS]

            mi_all, n_all = collapsed_mutual_information(pairs)
            mi_coupled, n_coupled = collapsed_mutual_information(coupled_pairs)
            mi_other, n_other = collapsed_mutual_information(other_pairs)

            row = {
                "cipher_seed": cs, "beta": beta,
                "mi_all_bits": mi_all, "n_all": n_all,
                "mi_coupling_initial_bits": mi_coupled, "n_coupling_initial": n_coupled,
                "mi_other_initial_bits": mi_other, "n_other_initial": n_other,
                "coupling_initial_fraction_of_pairs": n_coupled / n_all,
            }
            results[name].append(row)
            log(f"{name} seed {cs}: MI_all={mi_all:.5f} MI_coupling-initial={mi_coupled:.5f} "
                f"(n={n_coupled}, {100*n_coupled/n_all:.1f}% of pairs) MI_other-initial={mi_other:.5f} (n={n_other})")

    def summarize(rows):
        return {
            "mean_mi_all": sum(r["mi_all_bits"] for r in rows) / len(rows),
            "mean_mi_coupling_initial": sum(r["mi_coupling_initial_bits"] for r in rows) / len(rows),
            "mean_mi_other_initial": sum(r["mi_other_initial_bits"] for r in rows) / len(rows),
            "mean_coupling_initial_fraction": sum(r["coupling_initial_fraction_of_pairs"] for r in rows) / len(rows),
        }

    summary = {
        "hypothesis": "excess order-share predictability in 'primary' (coupling on) concentrates in pairs where the next token's first char is a coupling-target initial",
        "target_initials": TARGET_INITIALS,
        "replicates": results,
        "primary_summary": summarize(results["primary"]),
        "hybrid_novelty_only_summary": summarize(results["hybrid_novelty_only"]),
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")
    log(f"primary: {summary['primary_summary']}")
    log(f"hybrid_novelty_only: {summary['hybrid_novelty_only_summary']}")


if __name__ == "__main__":
    main()
