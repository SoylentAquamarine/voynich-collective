#!/usr/bin/env python3
"""SQ-1 follow-up: does a recurring Lz label word predict a stable RELATIVE
labelling-order position, even though it doesn't predict absolute clock time?

Precommitment: logs/2026-09-22-claude-lz-relative-order-precommitment.md,
written before this script ran. Reuses the exact leave-one-folio-out /
circular-null design already independently verified in
label_atlas_clock_signal.py, but on a different feature: each locus's rank
among its own folio's Lz loci (sorted by numeric locus ID), scaled to [0, 1)
and treated as circular. This tests a production/behavioral axis (labelling
order) as distinct from the already-falsified astronomical axis (clock time).

Usage:
    python data/scripts/label_atlas_lz_relative_order.py
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY_CSV = ROOT / "data" / "derived" / "label-atlas-lz-pilot.csv"
OUT_JSON = ROOT / "data" / "derived" / "label-atlas-lz-relative-order-signal.json"
OUT_REPORT = ROOT / "data" / "derived" / "label-atlas-lz-relative-order-signal-report.md"

DIAL = 1.0  # relative rank is circular on [0, 1)
SEED = 20260922
PERMUTATIONS = 10000


def load_rows() -> list[dict]:
    with INVENTORY_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit(f"{INVENTORY_CSV} is empty -- run label_atlas_inventory.py first")
    return rows


def assign_relative_ranks(rows: list[dict]) -> list[dict]:
    by_folio: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_folio[row["folio"]].append(row)

    out: list[dict] = []
    for folio, folio_rows in by_folio.items():
        ordered = sorted(folio_rows, key=lambda r: int(r["locus_id"]))
        n = len(ordered)
        for rank, row in enumerate(ordered):
            first_token = row["normalized_word"].split()[0] if row["normalized_word"].split() else None
            if first_token is None:
                continue
            out.append({"folio": folio, "token": first_token, "position": rank / n})
    return out


def circular_mean(positions: list[float]) -> float:
    sin_sum = sum(math.sin(2 * math.pi * p / DIAL) for p in positions)
    cos_sum = sum(math.cos(2 * math.pi * p / DIAL) for p in positions)
    angle = math.atan2(sin_sum, cos_sum)
    return (angle * DIAL / (2 * math.pi)) % DIAL


def circular_abs_error(predicted: float, actual: float) -> float:
    diff = abs(predicted - actual) % DIAL
    return min(diff, DIAL - diff)


def eligible_predictions(rows: list[dict], positions_by_index: list[float]) -> list[float]:
    by_token_folio: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    for i, row in enumerate(rows):
        by_token_folio[row["token"]][row["folio"]].append(i)

    errors: list[float] = []
    for i, row in enumerate(rows):
        folio_map = by_token_folio[row["token"]]
        other_folio_indices = [j for f, idxs in folio_map.items() if f != row["folio"] for j in idxs]
        if not other_folio_indices:
            continue
        predicted = circular_mean([positions_by_index[j] for j in other_folio_indices])
        errors.append(circular_abs_error(predicted, positions_by_index[i]))
    return errors


def run() -> dict:
    inventory_rows = load_rows()
    rows = assign_relative_ranks(inventory_rows)
    observed_positions = [row["position"] for row in rows]
    observed_errors = eligible_predictions(rows, observed_positions)
    observed_mean = sum(observed_errors) / len(observed_errors)

    by_folio_indices: dict[str, list[int]] = defaultdict(list)
    for i, row in enumerate(rows):
        by_folio_indices[row["folio"]].append(i)

    rng = random.Random(SEED)
    null_means: list[float] = []
    for _ in range(PERMUTATIONS):
        shuffled = list(observed_positions)
        for indices in by_folio_indices.values():
            values = [shuffled[i] for i in indices]
            rng.shuffle(values)
            for i, v in zip(indices, values):
                shuffled[i] = v
        errors = eligible_predictions(rows, shuffled)
        null_means.append(sum(errors) / len(errors))

    null_means.sort()
    n = len(null_means)
    p_value = sum(1 for m in null_means if m <= observed_mean) / n

    return {
        "total_lz_loci": len(rows),
        "eligible_occurrences": len(observed_errors),
        "observed_mean_error_fraction": observed_mean,
        "null_permutations": PERMUTATIONS,
        "seed": SEED,
        "null_mean_error_fraction": sum(null_means) / n,
        "null_95pct_interval": [null_means[int(0.025 * n)], null_means[int(0.975 * n) - 1]],
        "one_sided_p_at_least_as_low": p_value,
    }


def make_report(result: dict) -> str:
    signal = result["one_sided_p_at_least_as_low"] < 0.05
    verdict = (
        "a candidate signal worth a proper held-out follow-up"
        if signal
        else "no relative-order signal either"
    )
    return f"""# SQ-1 follow-up: Lz label relative reading-order signal

Precommitment: [`logs/2026-09-22-claude-lz-relative-order-precommitment.md`](../../logs/2026-09-22-claude-lz-relative-order-precommitment.md), written before this script ran.

## Result

**{verdict.capitalize()}.** {result['eligible_occurrences']} of {result['total_lz_loci']} Lz
loci had a first normalized token recurring on at least one other folio (the
same eligibility set as the clock-position test, since eligibility depends
only on token identity, not position). Predicting each held-out occurrence's
*relative labelling-order rank* (its position among its own folio's Lz loci,
scaled to `[0, 1)`) from the circular mean of that same token's relative rank
on *other* folios gives a mean error of **{result['observed_mean_error_fraction']:.4f}**
(as a fraction of a full ring), versus a {result['null_permutations']:,}-permutation
shuffled-null mean of **{result['null_mean_error_fraction']:.4f}** (95% interval
{result['null_95pct_interval'][0]:.4f}–{result['null_95pct_interval'][1]:.4f}).
One-sided p (observed at least as low as shuffled) = **{result['one_sided_p_at_least_as_low']:.4f}**.

This tests a different axis than the already-falsified clock-position result:
not the astronomical/semantic clock value, but the order in which the scribe
labelled figures within a folio. {"The result suggests this axis is worth a properly independent held-out follow-up before treating it as a candidate SQ-2 feature." if signal else "It comes back null as well -- recurring exact-word identity does not predict a stable position on this axis any more than it did on the clock-time axis."}

## Method

Leave-one-folio-out, identical in structure to the independently-verified
clock-position test (`label-atlas-lz-clock-signal-report.md`): for each
occurrence whose first normalized token recurs as another locus's first token
on a different folio, predict from the circular mean of that token's relative
rank on every other folio. Null shuffles each folio's own rank assignment
among its own loci. Seed `{result['seed']}`, `{result['null_permutations']:,}` permutations
-- identical seed and count to the clock test, for direct comparability.

## What this does not show

This is exploratory, not independently reproduced by a third party, and not
a knowledge-base claim. A null result here does not rule out *other*
relative-structure representations (e.g. inner/outer ring membership, which
is recorded only as inconsistent free-text commentary in the source and was
not attempted here because it cannot be parsed deterministically without a
real risk of misclassification). A positive result would still need an
independent held-out replication, exactly like the clock test's own design,
before being treated as more than a lead.
"""


def main() -> None:
    result = run()
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    OUT_REPORT.write_text(make_report(result), encoding="utf-8")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_REPORT.relative_to(ROOT)}")
    print(
        f"eligible={result['eligible_occurrences']} observed_mean={result['observed_mean_error_fraction']:.4f} "
        f"null_mean={result['null_mean_error_fraction']:.4f} p={result['one_sided_p_at_least_as_low']:.4f}"
    )


if __name__ == "__main__":
    main()
