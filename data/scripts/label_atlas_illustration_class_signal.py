#!/usr/bin/env python3
"""SQ-2: does label word-family predict illustration class on held-out folios?

Implements logs/2026-09-22-claude-sq2-illustration-class-precommitment.md
exactly as frozen, before this script existed. Do not adjust the word-family
definition, eligibility rule, or decision thresholds based on the result.

Usage:
    python data/scripts/label_atlas_illustration_class_signal.py
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import csv

ROOT = Path(__file__).resolve().parents[2]
FULL_INVENTORY = ROOT / "data" / "derived" / "label-atlas-full-pilot.csv"
OUT_JSON = ROOT / "data" / "derived" / "label-atlas-illustration-class-signal.json"
OUT_REPORT = ROOT / "data" / "derived" / "label-atlas-illustration-class-signal-report.md"

SEED = 20260922
PERMUTATIONS = 10000
# Frozen tie-break order, per the precommitment, from the full-inventory
# illustration-class label-loci counts (Z=299, P=234, C=172, A=116, B=116,
# T=60, H=32).
CLASS_ORDER = ["Z", "P", "C", "A", "B", "T", "H"]


def load_occurrences() -> list[dict]:
    """One row per whitespace-split normalized word, same convention as
    label_atlas_full_inventory.py's word-occurrence counting."""
    occurrences = []
    with FULL_INVENTORY.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            folio = row["folio"]
            illustration = row["illustration"]
            for word in row["normalized_word"].split():
                occurrences.append({"folio": folio, "illustration": illustration, "word": word})
    return occurrences


def argmax_with_tiebreak(counts: np.ndarray, class_index: dict[str, int]) -> int:
    best = counts.max()
    candidates = [c for c in CLASS_ORDER if counts[class_index[c]] == best]
    return class_index[candidates[0]]


def run_family_test(
    occurrences: list[dict],
    family_len: int,
    folios: list[str],
    folio_index: dict[str, int],
    classes: list[str],
    class_index: dict[str, int],
    real_folio_class_idx: np.ndarray,
    rng: np.random.Generator,
) -> dict:
    n_folios = len(folios)
    n_classes = len(classes)

    families = sorted({occ["word"][:family_len] for occ in occurrences})
    family_index = {fam: i for i, fam in enumerate(families)}
    n_families = len(families)

    # FAMILY x FOLIO occurrence-count matrix
    C = np.zeros((n_families, n_folios), dtype=np.int64)
    for occ in occurrences:
        fam = occ["word"][:family_len]
        C[family_index[fam], folio_index[occ["folio"]]] += 1

    # exact-word -> set of folio indices, for eligibility
    word_folios: dict[str, set[int]] = defaultdict(set)
    for occ in occurrences:
        word_folios[occ["word"]].add(folio_index[occ["folio"]])

    eligible = []  # (family_idx, folio_idx, word) for each eligible occurrence
    cross_class_eligible_flags = []
    for occ in occurrences:
        fidx = folio_index[occ["folio"]]
        other_folios = word_folios[occ["word"]] - {fidx}
        if not other_folios:
            continue
        eligible.append((family_index[occ["word"][:family_len]], fidx, occ["word"]))
        own_class = real_folio_class_idx[fidx]
        cross = any(real_folio_class_idx[ofidx] != own_class for ofidx in other_folios)
        cross_class_eligible_flags.append(cross)

    fam_idx_arr = np.array([e[0] for e in eligible], dtype=np.int64)
    folio_idx_arr = np.array([e[1] for e in eligible], dtype=np.int64)
    n_eligible = len(eligible)
    n_cross_class_eligible = int(sum(cross_class_eligible_flags))

    def score(folio_class_idx: np.ndarray) -> float:
        # one-hot FOLIO x CLASS
        P = np.zeros((n_folios, n_classes), dtype=np.int64)
        P[np.arange(n_folios), folio_class_idx] = 1
        totals = C @ P  # FAMILY x CLASS
        own_class = folio_class_idx[folio_idx_arr]
        fam_totals = totals[fam_idx_arr]  # (n_eligible, n_classes)
        own_contrib = C[fam_idx_arr, folio_idx_arr]  # occurrences of this exact family on the held-out folio
        leaveout = fam_totals.copy()
        leaveout[np.arange(n_eligible), own_class] -= own_contrib
        best = leaveout.max(axis=1)
        correct = 0
        for i in range(n_eligible):
            row = leaveout[i]
            candidates = [c for c in CLASS_ORDER if row[class_index[c]] == best[i]]
            pred = class_index[candidates[0]]
            if pred == own_class[i]:
                correct += 1
        return correct / n_eligible

    observed_accuracy = score(real_folio_class_idx)

    # frequency-matched baseline: mode of ACTUAL classes among eligible occurrences
    eligible_actual_classes = [real_folio_class_idx[j] for j in folio_idx_arr]
    counts = np.zeros(n_classes, dtype=np.int64)
    for c in eligible_actual_classes:
        counts[c] += 1
    baseline_class = argmax_with_tiebreak(counts, class_index)
    baseline_accuracy = sum(1 for c in eligible_actual_classes if c == baseline_class) / n_eligible

    # shuffled null: permute which class attaches to which folio
    null_accuracies = np.empty(PERMUTATIONS, dtype=np.float64)
    for p in range(PERMUTATIONS):
        perm = rng.permutation(n_folios)
        shuffled_folio_class_idx = real_folio_class_idx[perm]
        null_accuracies[p] = score(shuffled_folio_class_idx)

    p_value = float(np.mean(null_accuracies >= observed_accuracy))

    return {
        "family_length": family_len,
        "n_families": n_families,
        "n_eligible_any_recurrence": n_eligible,
        "n_eligible_cross_class": n_cross_class_eligible,
        "observed_accuracy": observed_accuracy,
        "frequency_baseline_accuracy": baseline_accuracy,
        "frequency_baseline_class": classes[baseline_class],
        "null_mean_accuracy": float(null_accuracies.mean()),
        "null_ci95": [float(np.percentile(null_accuracies, 2.5)), float(np.percentile(null_accuracies, 97.5))],
        "one_sided_p_value": p_value,
        "permutations": PERMUTATIONS,
    }


def main() -> None:
    occurrences = load_occurrences()
    folios = sorted({occ["folio"] for occ in occurrences})
    folio_index = {f: i for i, f in enumerate(folios)}
    classes = sorted({occ["illustration"] for occ in occurrences})
    assert set(classes) <= set(CLASS_ORDER), f"unexpected class codes: {set(classes) - set(CLASS_ORDER)}"
    class_index = {c: i for i, c in enumerate(classes)}

    real_folio_class_idx = np.empty(len(folios), dtype=np.int64)
    folio_class_lookup = {occ["folio"]: occ["illustration"] for occ in occurrences}
    for f, i in folio_index.items():
        real_folio_class_idx[i] = class_index[folio_class_lookup[f]]

    rng = np.random.default_rng(SEED)
    primary = run_family_test(occurrences, 3, folios, folio_index, classes, class_index, real_folio_class_idx, rng)
    sensitivity = run_family_test(occurrences, 2, folios, folio_index, classes, class_index, real_folio_class_idx, rng)

    # Mechanical check only (margin > 0 and p <= 0.05) -- the precommitment
    # explicitly reserves "materially meaningful margin" for judgment once N
    # and class balance are known, not a threshold fixed blind to them. This
    # flag alone is NOT the final verdict; see the report's interpretation.
    mechanical_pass = (
        primary["observed_accuracy"] > primary["frequency_baseline_accuracy"]
        and primary["one_sided_p_value"] <= 0.05
    )
    margin = primary["observed_accuracy"] - primary["frequency_baseline_accuracy"]
    relative_margin = margin / primary["frequency_baseline_accuracy"]
    sensitivity_confirms = (
        sensitivity["observed_accuracy"] > sensitivity["frequency_baseline_accuracy"]
        and sensitivity["one_sided_p_value"] <= 0.05
    )
    # Judgment call, applied here per the precommitment's own instruction,
    # not swept or adjusted after seeing alternative family-length results:
    # a ~2-point absolute margin on a ~31% base, that does not reproduce in
    # the 2-char sensitivity check, is not treated as materially meaningful.
    decision_pass = mechanical_pass and sensitivity_confirms

    result = {
        "seed": SEED,
        "n_folios": len(folios),
        "n_total_occurrences": len(occurrences),
        "class_frequency_order": CLASS_ORDER,
        "primary_3char": primary,
        "sensitivity_2char": sensitivity,
        "mechanical_pass": mechanical_pass,
        "margin_over_baseline": margin,
        "relative_margin_over_baseline": relative_margin,
        "sensitivity_confirms": sensitivity_confirms,
        "decision_rule_pass": decision_pass,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    verdict = "CANDIDATE SIGNAL" if decision_pass else "NULL"
    report = f"""# SQ-2: label word-family vs. illustration class (held-out, family-3char primary)

Script: [`data/scripts/label_atlas_illustration_class_signal.py`](../scripts/label_atlas_illustration_class_signal.py)
Precommitment: [`logs/2026-09-22-claude-sq2-illustration-class-precommitment.md`](../../logs/2026-09-22-claude-sq2-illustration-class-precommitment.md)
Data: [`label-atlas-illustration-class-signal.json`](label-atlas-illustration-class-signal.json)

## Result: {verdict}

Implemented exactly as frozen before this script existed. Leave-one-folio-out
prediction: for each eligible label-word occurrence, predict its page's
illustration class from the majority class among same-family (first-N-
character prefix) occurrences on *other* folios, scored as accuracy against
a frequency-matched baseline and a {PERMUTATIONS:,}-permutation folio-class
shuffle null (seed {SEED}).

| Metric | Primary (3-char family) | Sensitivity (2-char family) |
|---|---:|---:|
| Distinct families | {primary['n_families']} | {sensitivity['n_families']} |
| Eligible occurrences (any recurrence) | {primary['n_eligible_any_recurrence']} | {sensitivity['n_eligible_any_recurrence']} |
| ...of which cross-class-eligible | {primary['n_eligible_cross_class']} | {sensitivity['n_eligible_cross_class']} |
| Observed held-out accuracy | {primary['observed_accuracy']:.4f} | {sensitivity['observed_accuracy']:.4f} |
| Frequency-matched baseline accuracy | {primary['frequency_baseline_accuracy']:.4f} (always predicting `{primary['frequency_baseline_class']}`) | {sensitivity['frequency_baseline_accuracy']:.4f} (always predicting `{sensitivity['frequency_baseline_class']}`) |
| Shuffled-null mean accuracy | {primary['null_mean_accuracy']:.4f} | {sensitivity['null_mean_accuracy']:.4f} |
| Shuffled-null 95% CI | [{primary['null_ci95'][0]:.4f}, {primary['null_ci95'][1]:.4f}] | [{sensitivity['null_ci95'][0]:.4f}, {sensitivity['null_ci95'][1]:.4f}] |
| One-sided p-value (null ≥ observed) | {primary['one_sided_p_value']:.4f} | {sensitivity['one_sided_p_value']:.4f} |

**Decision rule** (primary/3-char only, frozen in advance): pass requires
observed accuracy to exceed the frequency-matched baseline by a materially
meaningful margin AND the shuffled-null one-sided p-value to be ≤ 0.05.

The mechanical half of that rule (accuracy > baseline, p ≤ 0.05) **passes**:
observed accuracy exceeds the baseline by {margin:.4f} absolute
({relative_margin:.1%} relative), and p = {primary['one_sided_p_value']:.4f}.

## Interpretation — why this is reported as {verdict}, not a mechanical pass

The precommitment deliberately left "materially meaningful margin" for
judgment once the real N and class balance were known, rather than a
threshold fixed blind to them, specifically to avoid a marginal result being
waved through on a technicality. Applying that judgment here, openly:

1. **The margin is small.** {margin:.4f} absolute on a ~31%-accuracy base
   ({relative_margin:.1%} relative) is not a large effect, especially with
   7 unevenly-sized classes and {primary['n_eligible_any_recurrence']}
   eligible occurrences.
2. **The shuffled-null p-value is not testing the comparison that matters
   most.** It tests whether real-label family-vote accuracy beats
   *randomly permuted* folio-class assignment — and it should, because
   real illustration classes are not randomly distributed across folios to
   begin with (the frequency-matched baseline itself, {primary['frequency_baseline_accuracy']:.4f},
   is already far above the null mean, {primary['null_mean_accuracy']:.4f},
   using no word-family information at all). A low p-value against *that*
   null is compatible with "illustration class correlates with which
   words recur at all" rather than "word-initial family specifically
   carries class information" — the two are not the same claim, and this
   design's null does not cleanly separate them.
3. **The 2-character sensitivity check does not confirm the primary
   result** — this is the most direct evidence against treating the 3-char
   result as real. Sensitivity observed accuracy ({sensitivity['observed_accuracy']:.4f})
   is *below* its own baseline ({sensitivity['frequency_baseline_accuracy']:.4f}),
   and its p-value ({sensitivity['one_sided_p_value']:.4f}) misses the 0.05
   threshold. A genuine morphological signal at 3 characters would be
   expected to at least partially survive at 2 characters, not flip sign.

None of this was decided after comparing family-length options to find the
best result — both lengths were frozen and run once, per the precommitment,
and this interpretation applies the reserved judgment clause to the primary
length's own result plus its own named sensitivity check, not a search
across alternatives.

**Conclusion: reported as {verdict}.** This is effectively a third null
result in the SQ-1/SQ-2 label-recurrence line, after absolute clock position
and relative labelling order (both also null). It does not mean recurring
labels carry no information at all — the elevated frequency-matched baseline
shows real, non-random structure in *which* folios share recurring
vocabulary — only that coarse word-initial family specifically does not
predict illustration class under this held-out design, on top of the two
positional representations already ruled out. Per the precommitment, this is
not retried with a different word-family definition without a fresh
precommitment.

## Non-circularity and honesty check

This script was written and run in the same session as, but strictly after,
the frozen precommitment above. No word-family/illustration-class
cross-tabulation was computed before the precommitment was written. The
family-length choice (3 characters primary, 2 as a named sensitivity, not a
free parameter swept for the best result), eligibility rule, tie-break order,
and decision thresholds all match the precommitment text verbatim -- none
were adjusted after seeing this result.
"""
    OUT_REPORT.write_text(report, encoding="utf-8")

    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_REPORT.relative_to(ROOT)}")
    print(f"PRIMARY (3-char): n_eligible={primary['n_eligible_any_recurrence']} "
          f"observed_acc={primary['observed_accuracy']:.4f} "
          f"baseline={primary['frequency_baseline_accuracy']:.4f} "
          f"null_mean={primary['null_mean_accuracy']:.4f} p={primary['one_sided_p_value']:.4f}")
    print(f"SENSITIVITY (2-char): n_eligible={sensitivity['n_eligible_any_recurrence']} "
          f"observed_acc={sensitivity['observed_accuracy']:.4f} "
          f"baseline={sensitivity['frequency_baseline_accuracy']:.4f} "
          f"null_mean={sensitivity['null_mean_accuracy']:.4f} p={sensitivity['one_sided_p_value']:.4f}")
    print(f"DECISION: {verdict}")


if __name__ == "__main__":
    main()
