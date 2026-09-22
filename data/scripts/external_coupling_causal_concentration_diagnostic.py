#!/usr/bin/env python3
"""Diagnostic (not a preregistered mechanism test): direct follow-up to
external_coupling_order_concentration_diagnostic.py (PR #42), whose leading hypothesis
(order-share excess concentrates in pairs where the NEXT token's first character is one
of the 4 coupling-target initials) was not confirmed. That diagnostic's own caveats named
an untried, more direct alternative: condition on whether coupling ACTUALLY FIRED for the
next token (the true causal event), not just on which letter it happened to produce --
those are different things, since a token can start with 'o'/'q'/'C'/'S' by chance from
the underlying Naibbe output even when coupling never touched it.

This modifies apply_coupling to also return, per token, whether coupling fired for it,
then splits the same collapsed-MI statistic by that direct boolean rather than by initial
-letter membership.

Usage:
    python data/scripts/external_coupling_causal_concentration_diagnostic.py <units_repo>
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
OUT_JSON = ROOT / "data" / "derived" / "external-coupling-causal-concentration-diagnostic-summary.json"

sys.path.insert(0, str(ROOT / "data" / "scripts"))
from external_hybrid_shift_v2_substitution_novelty_null_audit import (  # noqa: E402
    ATOMIC_ALPHABET, TARGET_INITIALS,
    apply_boundary_shift_v2, apply_substitution_topup, expand,
)

TOP_CAP = 2000


def apply_coupling_tracked(atomic_tokens, beta, rng):
    """Identical to apply_coupling, except also returns a parallel boolean list:
    fired[i] = True iff coupling's rng.random() < beta check succeeded for token i
    (the actual causal event), not just whether the result happens to start with a
    TARGET_INITIALS letter."""
    output = []
    fired = []
    prev_last = None
    for i, token in enumerate(atomic_tokens):
        candidate = list(token)
        this_fired = False
        if i > 0 and rng.random() < beta:
            target = TARGET_INITIALS[ATOMIC_ALPHABET.index(prev_last) % 4]
            candidate[0] = target
            this_fired = True
        candidate_str = "".join(candidate)
        output.append(candidate_str)
        fired.append(this_fired)
        prev_last = candidate_str[-1]
    return output, fired


def collapsed_mutual_information(pairs):
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

    results = []
    for cs, ps in zip(cipher_seeds, post_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic = [headlines.collapse(t) for t in encrypted["tokens"]]

        rng = random.Random(ps)
        coupled, fired = apply_coupling_tracked(atomic, 0.5, rng)
        shifted = apply_boundary_shift_v2(coupled, 1.0, rng)
        # boundary shift consumes tokens in pairs sometimes, merging/splitting -- track
        # provenance is lost across a shift, so this diagnostic works at the COUPLING
        # output stage directly (pre-shift), which is where "fired" is well-defined,
        # and separately checks the POST-shift+substitution stage using the ORIGINAL
        # per-source-token fired flags is not meaningful (shifted tokens are new pieces).
        # So: measure MI at the coupling-output stage itself (pre-shift/pre-substitution),
        # split by whether the NEXT token in that stream had coupling fire.
        expanded_pre = [expand(t) for t in coupled]
        pairs_pre = list(zip(expanded_pre, expanded_pre[1:]))
        fired_pairs = [(l, r) for (l, r), f in zip(pairs_pre, fired[1:]) if f]
        not_fired_pairs = [(l, r) for (l, r), f in zip(pairs_pre, fired[1:]) if not f]

        mi_all, n_all = collapsed_mutual_information(pairs_pre)
        mi_fired, n_fired = collapsed_mutual_information(fired_pairs)
        mi_not_fired, n_not_fired = collapsed_mutual_information(not_fired_pairs)

        # Also measure the full pipeline (post shift+substitution) MI for reference,
        # matching primary's own aggregate order-share magnitude.
        topped = apply_substitution_topup(shifted, 0.01, random.Random(ps + 1))
        expanded_full = [expand(t) for t in topped]
        pairs_full = list(zip(expanded_full, expanded_full[1:]))
        mi_full, n_full = collapsed_mutual_information(pairs_full)

        row = {
            "cipher_seed": cs,
            "mi_coupling_stage_all": mi_all, "n_all": n_all,
            "mi_coupling_fired_pairs": mi_fired, "n_fired": n_fired,
            "mi_coupling_not_fired_pairs": mi_not_fired, "n_not_fired": n_not_fired,
            "fired_fraction": n_fired / n_all,
            "mi_full_pipeline": mi_full, "n_full": n_full,
        }
        results.append(row)
        log(f"seed {cs}: coupling-stage MI_all={mi_all:.5f} | MI_fired={mi_fired:.5f} (n={n_fired}, {100*n_fired/n_all:.1f}%) "
            f"| MI_not_fired={mi_not_fired:.5f} (n={n_not_fired}) | full-pipeline MI={mi_full:.5f}")

    summary = {
        "hypothesis": "order predictability concentrates in pairs where coupling ACTUALLY FIRED for the next token (the causal event), not merely pairs where it happens to start with a coupling-target letter",
        "note": "measured at the coupling-output stage (pre-shift/pre-substitution) where per-token fired provenance is well-defined; a post-shift measurement cannot attribute provenance since shifts merge/resplit tokens",
        "replicates": results,
        "mean_mi_fired": sum(r["mi_coupling_fired_pairs"] for r in results) / len(results),
        "mean_mi_not_fired": sum(r["mi_coupling_not_fired_pairs"] for r in results) / len(results),
        "mean_fired_fraction": sum(r["fired_fraction"] for r in results) / len(results),
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")
    log(f"mean MI_fired={summary['mean_mi_fired']:.5f} vs mean MI_not_fired={summary['mean_mi_not_fired']:.5f}")


if __name__ == "__main__":
    main()
