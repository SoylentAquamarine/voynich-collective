#!/usr/bin/env python3
"""Adversarial checks for the external paper's cross-token edge dependence.

This script deliberately imports the public reproduction bundle rather than
copying its parser.  It asks two narrower questions than the paper driver:

1. Does last-glyph -> next-first-glyph dependence predict a genuinely omitted
   quire under several fixed Dirichlet smoothing strengths?
2. Does excess mutual information survive nulls that preserve quire and token
   position within the manuscript line?

Usage:
    python data/scripts/external_edge_crossfit.py \
        ../paper-audit/voynich-units \
        --output data/derived/external-edge-crossfit-summary.json
"""

from __future__ import annotations

import argparse
import importlib
import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


ALPHAS = (0.1, 0.5, 1.0, 5.0, 20.0)
SEED = 20260919
EXPECTED_COMMIT = "956a7c4fc39981f4d116fa3f4edfccce6d065571"


def load_external(repo: Path):
    actual_commit = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual_commit != EXPECTED_COMMIT:
        raise RuntimeError(
            f"external repository is at {actual_commit}, expected {EXPECTED_COMMIT}"
        )
    analysis = repo / "analysis"
    sys.path.insert(0, str(analysis))
    edge = importlib.import_module("reproduce_edge_order")
    space = importlib.import_module("reproduce_space_sensitivity")
    bundle = repo / "voynich_decipherment_repro_bundle"
    _, _, locus_re, collapse, strip_markup = edge.rst.load_modules(bundle)
    parsed, skipped = space.parse_lines(
        bundle / "voynich_calibration_sources" / "ZL3b.txt",
        locus_re,
        strip_markup,
    )
    return edge, parsed, collapse, skipped


def records(parsed: list[dict], collapse, representation: str) -> list[dict]:
    output = []
    for line_number, line in enumerate(parsed):
        if line["quire"] == "?":
            continue
        if representation == "collapsed":
            tokens = [collapse(token) for token in line["tokens"]]
        else:
            tokens = [token.lower() for token in line["tokens"]]
        n = len(tokens)
        for left_index in range(n - 1):
            right_index = left_index + 1
            output.append(
                {
                    "quire": line["quire"],
                    "line": line_number,
                    "left_index": left_index,
                    "right_index": right_index,
                    "line_length": n,
                    "left": tokens[left_index][-1],
                    "right": tokens[right_index][0],
                }
            )
    return output


def subset(rows: list[dict], interior_only: bool) -> list[dict]:
    if not interior_only:
        return rows
    return [
        row
        for row in rows
        if row["left_index"] > 0
        and row["right_index"] < row["line_length"] - 1
    ]


def crossfit(rows: list[dict], alpha: float) -> dict:
    quires = sorted({row["quire"] for row in rows})
    folds = []
    total_gain = 0.0
    total_pairs = 0
    for held_out in quires:
        training = [row for row in rows if row["quire"] != held_out]
        testing = [row for row in rows if row["quire"] == held_out]
        marginal = Counter(row["right"] for row in training)
        context = Counter((row["left"], row["right"]) for row in training)
        left_count = Counter(row["left"] for row in training)
        training_alphabet = set(marginal)
        # The extra bucket handles a glyph absent from the training quires;
        # vocabulary size and all frequencies therefore come from training only.
        k = len(training_alphabet) + 1
        n_train = len(training)
        gain = 0.0
        for row in testing:
            observed_y = row["right"]
            y = observed_y if observed_y in training_alphabet else "<unknown>"
            x = row["left"]
            p_conditional = (context[(x, y)] + alpha) / (left_count[x] + alpha * k)
            p_marginal = (marginal[y] + alpha) / (n_train + alpha * k)
            gain += math.log2(p_conditional / p_marginal)
        folds.append(
            {
                "quire": held_out,
                "pairs": len(testing),
                "gain_bits_per_pair": gain / len(testing),
            }
        )
        total_gain += gain
        total_pairs += len(testing)
    return {
        "alpha": alpha,
        "pairs": total_pairs,
        "quires": len(quires),
        "gain_bits_per_pair": total_gain / total_pairs,
        "positive_folds": sum(row["gain_bits_per_pair"] > 0 for row in folds),
        "folds": folds,
    }


def encode_pairs(rows: list[dict]):
    left_values = sorted({row["left"] for row in rows})
    right_values = sorted({row["right"] for row in rows})
    left_index = {value: index for index, value in enumerate(left_values)}
    right_index = {value: index for index, value in enumerate(right_values)}
    left = np.array([left_index[row["left"]] for row in rows], dtype=np.int64)
    right = np.array([right_index[row["right"]] for row in rows], dtype=np.int64)
    return left, right, len(right_values)


def position_strata(rows: list[dict], scheme: str) -> list[np.ndarray]:
    groups = defaultdict(list)
    for index, row in enumerate(rows):
        if scheme == "quire":
            key = (row["quire"],)
        elif scheme == "quire_relative_quintile":
            relative = row["right_index"] / (row["line_length"] - 1)
            key = (row["quire"], min(4, int(relative * 5)))
        elif scheme == "quire_edge_distance":
            key = (
                row["quire"],
                min(row["right_index"], 3),
                min(row["line_length"] - 1 - row["right_index"], 3),
            )
        else:
            raise ValueError(scheme)
        groups[key].append(index)
    return [np.array(indices, dtype=np.int64) for indices in groups.values()]


def stratified_null(rows: list[dict], edge, scheme: str, shuffles: int, seed: int) -> dict:
    left, right, right_types = encode_pairs(rows)
    observed = edge.pair_mi(left, right, right_types)
    strata = position_strata(rows, scheme)
    rng = np.random.default_rng(seed)
    null = np.empty(shuffles)
    for repetition in range(shuffles):
        permuted = right.copy()
        for indices in strata:
            permuted[indices] = rng.permutation(permuted[indices])
        null[repetition] = edge.pair_mi(left, permuted, right_types)
    return {
        "scheme": scheme,
        "pairs": len(rows),
        "strata": len(strata),
        "singleton_strata": sum(len(indices) == 1 for indices in strata),
        "observed_mi_bits": observed,
        "null_mean_mi_bits": float(null.mean()),
        "null_sd_mi_bits": float(null.std(ddof=1)),
        "null_max_mi_bits": float(null.max()),
        "excess_bits": observed - float(null.mean()),
        "observed_exceeds_all_shuffles": bool(observed > null.max()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("external_repo", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--shuffles", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    repo = args.external_repo.resolve()
    edge, parsed, collapse, skipped = load_external(repo)
    result = {
        "external_commit": EXPECTED_COMMIT,
        "skipped_lines": skipped,
        "shuffles": args.shuffles,
        "seed": args.seed,
        "representations": {},
    }
    for representation in ("collapsed", "raw"):
        all_rows = records(parsed, collapse, representation)
        rep_result = {}
        for label, interior_only in (("all_pairs", False), ("interior_pairs", True)):
            selected = subset(all_rows, interior_only)
            rep_result[label] = {
                "pairs": len(selected),
                "crossfit": [crossfit(selected, alpha) for alpha in ALPHAS],
                "position_nulls": [
                    stratified_null(selected, edge, scheme, args.shuffles, args.seed)
                    for scheme in (
                        "quire",
                        "quire_relative_quintile",
                        "quire_edge_distance",
                    )
                ],
            }
        result["representations"][representation] = rep_result

    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        print(rendered)


if __name__ == "__main__":
    main()
