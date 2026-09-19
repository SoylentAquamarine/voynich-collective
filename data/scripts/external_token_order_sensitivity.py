#!/usr/bin/env python3
"""Stress-test the external paper's weak adjacent-token-order result.

The paper collapses every token outside the 2,000 most frequent types to one
``<other>`` symbol, then subtracts the mutual information found after
within-line shuffling.  This script tests whether the reported Voynich/control
separation is driven by that fixed cap or by Voynich's long rare-token tail.

It adds three views:

1. a wider fixed-cap curve;
2. equal retained-token coverage across corpora; and
3. ten-fold held-out prediction, where vocabularies and probabilities are
   learned from training folds only.

Usage:
    python data/scripts/external_token_order_sensitivity.py \
        ../paper-audit/voynich-units \
        --output data/derived/external-token-order-sensitivity-summary.json
"""

from __future__ import annotations

import argparse
import importlib
import json
import math
import random
import subprocess
import sys
from collections import Counter
from pathlib import Path


EXPECTED_COMMIT = "956a7c4fc39981f4d116fa3f4edfccce6d065571"
CAPS = (50, 100, 250, 500, 1000, 2000, 4000, 8000)
COVERAGES = (0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.975)
ALPHAS = (1.0, 5.0, 20.0, 100.0, 500.0, 2000.0)
SEED = 20260919


def load_external(repo: Path):
    actual_commit = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual_commit != EXPECTED_COMMIT:
        raise RuntimeError(
            f"external repository is at {actual_commit}, expected {EXPECTED_COMMIT}"
        )
    sys.path.insert(0, str(repo / "analysis"))
    edge = importlib.import_module("reproduce_edge_order")
    scale = importlib.import_module("reproduce_scale_transition")
    bundle = repo / "voynich_decipherment_repro_bundle"
    corpora, _, meta = edge.build_corpora(bundle, repo / "data" / "voynich-units")
    selected = {
        name: lines
        for name, lines in corpora.items()
        if "[raw EVA]" not in name
    }
    return scale, selected, meta


def frequency_order(lines: list[list[str]]) -> list[tuple[str, int]]:
    return Counter(token for line in lines for token in line).most_common()


def coverage_for_cap(lines: list[list[str]], cap: int) -> float:
    ordered = frequency_order(lines)
    total = sum(count for _, count in ordered)
    return sum(count for _, count in ordered[:cap]) / total


def retained_for_coverage(lines: list[list[str]], target: float) -> tuple[set[str], float]:
    ordered = frequency_order(lines)
    total = sum(count for _, count in ordered)
    retained = set()
    covered = 0
    for token, count in ordered:
        retained.add(token)
        covered += count
        if covered / total >= target:
            break
    return retained, covered / total


def recode(lines: list[list[str]], retained: set[str]) -> list[list[str]]:
    return [
        [token if token in retained else "<other>" for token in line]
        for line in lines
        if len(line) >= 2
    ]


def order_for_retained(
    lines: list[list[str]], retained: set[str], scale, shuffles: int, seed: int
) -> dict:
    recoded = recode(lines, retained)
    observed, entropy = scale.mutual_information(recoded)
    rng = random.Random(seed)
    null = []
    for _ in range(shuffles):
        permuted = [list(line) for line in recoded]
        for line in permuted:
            rng.shuffle(line)
        null.append(scale.mutual_information(permuted)[0])
    null_mean = sum(null) / len(null)
    excess = observed - null_mean
    return {
        "retained_types": len(retained),
        "retained_coverage": sum(
            token in retained for line in lines for token in line
        ) / sum(len(line) for line in lines),
        "entropy_bits": entropy,
        "observed_mi_bits": observed,
        "shuffle_mean_mi_bits": null_mean,
        "shuffle_sd_mi_bits": (
            sum((value - null_mean) ** 2 for value in null) / (len(null) - 1)
        ) ** 0.5 if len(null) > 1 else 0.0,
        "shuffle_min_mi_bits": min(null),
        "shuffle_max_mi_bits": max(null),
        "excess_bits": excess,
        "share_of_entropy": excess / entropy if entropy else 0.0,
        "observed_exceeds_all_shuffles": observed > max(null),
    }


def contiguous_folds(lines: list[list[str]], count: int) -> list[list[list[str]]]:
    boundaries = [round(index * len(lines) / count) for index in range(count + 1)]
    return [lines[boundaries[i] : boundaries[i + 1]] for i in range(count)]


def predictive_gain(
    lines: list[list[str]], cap: int, alpha: float, folds: int = 10
) -> dict:
    blocks = contiguous_folds(lines, folds)
    fold_rows = []
    total_gain = 0.0
    total_pairs = 0
    for held_out_index, testing in enumerate(blocks):
        training = [
            line
            for index, block in enumerate(blocks)
            if index != held_out_index
            for line in block
        ]
        ordered = frequency_order(training)
        retained = {token for token, _ in ordered[:cap]}
        train_recoded = recode(training, retained)
        test_recoded = recode(testing, retained)

        following = Counter()
        previous = Counter()
        bigrams = Counter()
        for line in train_recoded:
            for left, right in zip(line, line[1:]):
                previous[left] += 1
                following[right] += 1
                bigrams[(left, right)] += 1
        vocabulary = retained | {"<other>"}
        beta = 0.5
        n_following = sum(following.values())
        base_probability = {
            token: (following[token] + beta) / (n_following + beta * len(vocabulary))
            for token in vocabulary
        }

        gain = 0.0
        pairs = 0
        for line in test_recoded:
            for left, right in zip(line, line[1:]):
                baseline = base_probability[right]
                conditional = (
                    bigrams[(left, right)] + alpha * baseline
                ) / (previous[left] + alpha)
                gain += math.log2(conditional / baseline)
                pairs += 1
        fold_rows.append(
            {
                "fold": held_out_index,
                "pairs": pairs,
                "gain_bits_per_pair": gain / pairs,
            }
        )
        total_gain += gain
        total_pairs += pairs
    return {
        "cap": cap,
        "alpha": alpha,
        "pairs": total_pairs,
        "gain_bits_per_pair": total_gain / total_pairs,
        "positive_folds": sum(row["gain_bits_per_pair"] > 0 for row in fold_rows),
        "folds": fold_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("external_repo", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--shuffles", type=int, default=30)
    parser.add_argument("--focused-shuffles", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    repo = args.external_repo.resolve()
    scale, corpora, meta = load_external(repo)
    voynich = corpora["Voynich observed separators"]
    voynich_cap2000_coverage = coverage_for_cap(voynich, 2000)

    result = {
        "external_commit": EXPECTED_COMMIT,
        "seed": args.seed,
        "shuffles": args.shuffles,
        "meta": meta,
        "voynich_cap2000_coverage": voynich_cap2000_coverage,
        "corpora": {},
    }
    for name, lines in corpora.items():
        ordered = frequency_order(lines)
        cap_rows = {}
        for cap in CAPS:
            retained = {token for token, _ in ordered[:cap]}
            cap_rows[str(cap)] = order_for_retained(
                lines, retained, scale, args.shuffles, args.seed
            )

        coverage_rows = {}
        for target in COVERAGES:
            retained, actual = retained_for_coverage(lines, target)
            row = order_for_retained(lines, retained, scale, args.shuffles, args.seed)
            row["actual_coverage"] = actual
            coverage_rows[str(target)] = row

        matched_retained, matched_actual = retained_for_coverage(
            lines, voynich_cap2000_coverage
        )
        matched_row = order_for_retained(
            lines, matched_retained, scale, args.shuffles, args.seed
        )
        matched_row["target_coverage"] = voynich_cap2000_coverage
        matched_row["actual_coverage"] = matched_actual

        crossfit = [
            predictive_gain(lines, cap, alpha)
            for cap in (500, 2000, 4000)
            for alpha in ALPHAS
        ]
        result["corpora"][name] = {
            "tokens": sum(len(line) for line in lines),
            "types": len(ordered),
            "cap_sensitivity": cap_rows,
            "coverage_sensitivity": coverage_rows,
            "voynich_cap2000_coverage_matched": matched_row,
            "crossfit": crossfit,
        }

    # The broad grid locates the closest natural/record control. Re-run that
    # single comparison at much higher permutation precision so a noisy
    # 30-shuffle null estimate is not mistaken for a meaningful gap.
    voy_rows = result["corpora"]["Voynich observed separators"]["coverage_sensitivity"]
    closest = None
    for target in COVERAGES:
        key = str(target)
        voy_share = voy_rows[key]["share_of_entropy"]
        for name, row in result["corpora"].items():
            if name.startswith("Voynich"):
                continue
            control_share = row["coverage_sensitivity"][key]["share_of_entropy"]
            candidate = (abs(control_share - voy_share), target, name)
            if closest is None or candidate < closest:
                closest = candidate
    _, closest_target, closest_name = closest
    focused = {}
    for name in ("Voynich observed separators", closest_name):
        retained, actual = retained_for_coverage(corpora[name], closest_target)
        row = order_for_retained(
            corpora[name], retained, scale, args.focused_shuffles, args.seed
        )
        row["actual_coverage"] = actual
        focused[name] = row
    result["closest_coverage_comparison"] = {
        "target_coverage": closest_target,
        "control": closest_name,
        "shuffles": args.focused_shuffles,
        "rows": focused,
        "share_gap_control_minus_voynich": (
            focused[closest_name]["share_of_entropy"]
            - focused["Voynich observed separators"]["share_of_entropy"]
        ),
    }

    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        print(rendered)


if __name__ == "__main__":
    main()
