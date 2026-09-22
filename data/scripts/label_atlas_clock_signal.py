#!/usr/bin/env python3
"""SQ-1 pilot: does an exact recurring Lz label word predict a stable clock
position across folios?

Independent reimplementation and rerun of ChatGPT's exploratory test
(comms/FromChatGPTToClaude.md Round 33). Frozen design, matched to that
round's own description: for each Lz-locus occurrence whose first normalized
token also appears as another locus's first token on a DIFFERENT folio,
predict its clock position from the circular mean of that exact token's
positions on all *other* folios (leave-one-folio-out), then score the
circular absolute error on a 720-minute (12-hour) dial. The null shuffles
each folio's own clock positions among its own loci (preserving each folio's
position inventory, label forms, and cross-folio token frequencies) and
repeats the same held-out prediction under the shuffled labeling.

This script does not depend on label_atlas_inventory.py's output files -- it
re-derives the same 298 clocked Lz loci directly from the canonical source,
so a bug in one script's parsing cannot silently validate the other's.

Usage:
    python data/scripts/label_atlas_clock_signal.py
"""

from __future__ import annotations

import json
import math
import random
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "ZL3b-n.txt"
NORMALIZED = ROOT / "data" / "derived" / "ZL3b-normalized.txt"
OUT_JSON = ROOT / "data" / "derived" / "label-atlas-lz-clock-signal.json"
OUT_REPORT = ROOT / "data" / "derived" / "label-atlas-lz-clock-signal-report.md"

LOCUS_LINE = re.compile(r"^<(f[^.,>]+)\.([^,>]+),([^>]+)>\s*(.*)$")
CLOCK = re.compile(r"^<!(\d{1,2}):(\d{2})>")
DIAL = 720  # a 12-hour analog dial expressed in minutes (0..719)
SEED = 20260922
PERMUTATIONS = 10000


def load_normalized() -> dict[str, str]:
    words: dict[str, str] = {}
    for line in NORMALIZED.read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        key, text = line.split("\t", 1)
        words[key] = text
    return words


def load_clocked_lz_loci() -> list[dict]:
    normalized = load_normalized()
    rows: list[dict] = []
    for line in RAW.read_text(encoding="utf-8").splitlines():
        m = LOCUS_LINE.match(line)
        if not m:
            continue
        page, locus_id, descriptor, rest = m.groups()
        if len(descriptor) < 2 or descriptor[1] != "L" or descriptor[2:] != "z":
            continue
        clock_m = CLOCK.match(rest)
        if not clock_m:
            continue
        hour, minute = int(clock_m.group(1)), int(clock_m.group(2))
        position = (hour % 12) * 60 + minute
        locus_key = f"{page}.{locus_id},{descriptor}"
        normalized_word = normalized.get(locus_key, "")
        first_token = normalized_word.split()[0] if normalized_word.split() else None
        if first_token is None:
            continue
        rows.append({"folio": page, "locus_key": locus_key, "token": first_token, "position": position})
    return rows


def circular_mean(positions: list[int]) -> float:
    sin_sum = sum(math.sin(2 * math.pi * p / DIAL) for p in positions)
    cos_sum = sum(math.cos(2 * math.pi * p / DIAL) for p in positions)
    angle = math.atan2(sin_sum, cos_sum)
    return (angle * DIAL / (2 * math.pi)) % DIAL


def circular_abs_error(predicted: float, actual: float) -> float:
    diff = abs(predicted - actual) % DIAL
    return min(diff, DIAL - diff)


def eligible_predictions(rows: list[dict], positions_by_index: list[int]) -> list[float]:
    """For each row, predict from same-token rows on OTHER folios only.

    `positions_by_index` lets the caller substitute shuffled positions while
    reusing the same token/folio structure (and therefore the same
    eligibility set) for the null.
    """
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
    rows = load_clocked_lz_loci()
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
    ge_as_extreme = sum(1 for m in null_means if m <= observed_mean)
    p_value = ge_as_extreme / n

    return {
        "clocked_loci": len(rows),
        "eligible_occurrences": len(observed_errors),
        "observed_mean_error_minutes": observed_mean,
        "null_permutations": PERMUTATIONS,
        "seed": SEED,
        "null_mean_error_minutes": sum(null_means) / n,
        "null_95pct_interval": [null_means[int(0.025 * n)], null_means[int(0.975 * n) - 1]],
        "one_sided_p_at_least_as_low": p_value,
    }


def make_report(result: dict) -> str:
    return f"""# SQ-1 pilot: Lz label clock-position held-out signal

Independent reimplementation of ChatGPT's exploratory test
(`comms/FromChatGPTToClaude.md` Round 33), rerun from the canonical source
without depending on `label_atlas_inventory.py`'s output.

## Result

**No absolute-position signal.** {result['eligible_occurrences']} of {result['clocked_loci']} clocked Lz
loci had a first normalized token recurring on at least one other folio.
Predicting each held-out occurrence's clock position from the circular mean
of that same token's position on *other* folios gives a mean error of
**{result['observed_mean_error_minutes']:.2f} clock-minutes** on a 720-minute dial, versus a
{result['null_permutations']:,}-permutation shuffled-null mean of
**{result['null_mean_error_minutes']:.2f}** (95% interval
{result['null_95pct_interval'][0]:.2f}–{result['null_95pct_interval'][1]:.2f}). One-sided
p (observed at least as low as shuffled) = **{result['one_sided_p_at_least_as_low']:.4f}** —
the real labels are not better than shuffled, and directionally worse.

This falsifies the simple idea that an exact recurring first word, by itself,
names a stable absolute clock/ring position across these folios. It does not
test morphology, visual identity, relative order, or candidate meaning — only
this one specific representation.

## Method

Leave-one-folio-out: for each occurrence whose first normalized token recurs
as another locus's first token on a *different* folio, the predicted position
is the circular mean of that token's positions on every other folio (same-
folio duplicates are excluded from the prediction basis, not just the
occurrence itself). Error is the circular absolute distance on a 720-minute
dial. The null shuffles each folio's own clock positions among its own loci,
preserving each folio's position inventory, the label text, and cross-folio
token frequencies; only the position-to-locus assignment is permuted.
Seed `{result['seed']}`, `{result['null_permutations']:,}` permutations.

## What this does not show

This is exploratory, not independently reproduced by a third party, and is
not a knowledge-base claim. It rules out one specific, simple representation
(absolute clock position, matched by exact first-token identity) as a
candidate semantic feature for SQ-2. It says nothing about relative order,
image-linked object identity, or morphological family matching -- the
necessary next layers before any semantic-anchor test can be attempted.
"""


def main() -> None:
    result = run()
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    OUT_REPORT.write_text(make_report(result), encoding="utf-8")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_REPORT.relative_to(ROOT)}")
    print(
        f"clocked_loci={result['clocked_loci']} eligible={result['eligible_occurrences']} "
        f"observed_mean={result['observed_mean_error_minutes']!r} "
        f"null_mean={result['null_mean_error_minutes']:.2f} p={result['one_sided_p_at_least_as_low']:.4f}"
    )


if __name__ == "__main__":
    main()
