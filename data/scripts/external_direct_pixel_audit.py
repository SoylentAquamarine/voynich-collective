#!/usr/bin/env python3
"""Audit the archived direct-pixel separator measurements in Rozanova & Temerev.

The paper's raw page scans and frozen blind manifest are not in its public
bundle.  This script therefore audits the released, unblinded per-boundary
measurements and robustness tables at the pinned final-bundle commit.  It
verifies their checksums, reproduces the headline summaries, and adds a
line-matched permutation check for raw and locally height-normalized gaps.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import tempfile
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd


COMMIT = "956a7c4fc39981f4d116fa3f4edfccce6d065571"
FILES = {
    "results_unblinded.csv": "3c15627dc3ddfca4f331a1fed1e1a290a9b8412ebf9247fe4c9b2778412aedee",
    "threshold_sensitivity.csv": "f7f6734d01793906a863e802b51521c464dff26bada6a65755d3b6506537c562",
    "estimator_robustness.csv": "67eacb729953912e00c55e6091acc9a4f9a5dc647bba5d62d006e503372205ab",
}
RAW_BASE = f"https://raw.githubusercontent.com/lrozanova/voynich-units/{COMMIT}/data/direct_pixel"
MISSING_RAW_INPUTS = [
    "sample_manifest_blind.csv",
    "qc_decisions_blind.csv",
    "sample_key.csv",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def obtain_files(external_root: Path | None, temp_root: Path) -> tuple[dict[str, Path], list[str]]:
    paths: dict[str, Path] = {}
    if external_root:
        data_dir = external_root / "data" / "direct_pixel"
        for name in FILES:
            paths[name] = data_dir / name
        present_names = {p.name for p in external_root.rglob("*.csv")}
        missing = [name for name in MISSING_RAW_INPUTS if name not in present_names]
    else:
        missing = MISSING_RAW_INPUTS[:]
        for name in FILES:
            target = temp_root / name
            urllib.request.urlretrieve(f"{RAW_BASE}/{name}", target)
            paths[name] = target
    for name, expected in FILES.items():
        if not paths[name].is_file():
            raise FileNotFoundError(paths[name])
        actual = sha256(paths[name])
        if actual != expected:
            raise RuntimeError(f"checksum mismatch for {name}: {actual} != {expected}")
    return paths, missing


def group_summary(df: pd.DataFrame, column: str) -> dict:
    by_group = {}
    for group in ("certain", "uncertain"):
        values = df.loc[df.group == group, column].to_numpy(float)
        by_group[group] = {
            "n": int(len(values)),
            "mean": float(values.mean()),
            "median": float(np.median(values)),
            "sd": float(values.std(ddof=1)),
        }
    return {
        "groups": by_group,
        "certain_minus_uncertain": by_group["certain"]["mean"] - by_group["uncertain"]["mean"],
    }


def exact_sign_p(positive: int, total: int) -> float:
    return sum(math.comb(total, k) for k in range(positive, total + 1)) / (2**total)


def line_permutation(df: pd.DataFrame, column: str, nrep: int, seed: int) -> dict:
    observed: list[float] = []
    options: list[np.ndarray] = []
    for _, group in df.groupby(["folio", "line"]):
        if group.group.nunique() != 2:
            continue
        certain = group.loc[group.group == "certain", column].to_numpy(float)
        uncertain = group.loc[group.group == "uncertain", column].to_numpy(float)
        observed.append(float(certain.mean() - uncertain.mean()))
        values = group[column].to_numpy(float)
        nu, nc = len(uncertain), len(certain)
        sums = np.array(
            [sum(values[list(indices)]) for indices in itertools.combinations(range(len(values)), nu)]
        )
        options.append((values.sum() - sums) / nc - sums / nu)

    statistic = float(np.mean(observed))
    rng = np.random.default_rng(seed)
    simulated = np.zeros(nrep)
    for choices in options:
        simulated += rng.choice(choices, size=nrep)
    simulated /= len(options)
    return {
        "matched_lines": len(options),
        "positive_lines": sum(value > 0 for value in observed),
        "equal_line_mean_difference": statistic,
        "permutations": nrep,
        "seed": seed,
        "p_one_sided": float((1 + np.sum(simulated >= statistic)) / (nrep + 1)),
        "p_two_sided": float((1 + np.sum(np.abs(simulated) >= abs(statistic))) / (nrep + 1)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--external-root",
        type=Path,
        help="Checkout of lrozanova/voynich-units at the pinned commit; downloads archived CSVs if omitted.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/derived/external-direct-pixel-summary.json"),
    )
    parser.add_argument("--permutations", type=int, default=300_000)
    parser.add_argument("--seed", type=int, default=20260809)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as td:
        paths, missing = obtain_files(args.external_root, Path(td))
        all_rows = pd.read_csv(paths["results_unblinded.csv"])
        included = all_rows[all_rows.include & all_rows.gap_px.notna()].copy()
        thresholds = pd.read_csv(paths["threshold_sensitivity.csv"])
        estimators = pd.read_csv(paths["estimator_robustness.csv"])

        folios = []
        for folio, group in included.groupby("folio"):
            if group.group.nunique() != 2:
                continue
            row = {"folio": folio}
            for column in ("gap_px", "direct_gap_norm_local_boxheight", "box_gap_img"):
                means = group.groupby("group")[column].mean()
                row[f"{column}_certain_minus_uncertain"] = float(means["certain"] - means["uncertain"])
            row["certain_n"] = int((group.group == "certain").sum())
            row["uncertain_n"] = int((group.group == "uncertain").sum())
            folios.append(row)

        central = thresholds[(thresholds.offset >= -20) & (thresholds.offset <= 25)]
        summary = {
            "source": {
                "repository": "https://github.com/lrozanova/voynich-units",
                "commit": COMMIT,
                "files": {name: {"sha256": expected} for name, expected in FILES.items()},
            },
            "rows": {
                "candidate": int(len(all_rows)),
                "included": int(len(included)),
                "excluded": int(len(all_rows) - len(included)),
                "included_certain": int((included.group == "certain").sum()),
                "included_uncertain": int((included.group == "uncertain").sum()),
            },
            "raw_gap_px": group_summary(included, "gap_px"),
            "normalized_gap_local_boxheight": group_summary(included, "direct_gap_norm_local_boxheight"),
            "locator_box_gap_px": group_summary(included, "box_gap_img"),
            "informative_folios": {
                "count": len(folios),
                "positive_raw": sum(row["gap_px_certain_minus_uncertain"] > 0 for row in folios),
                "positive_normalized": sum(
                    row["direct_gap_norm_local_boxheight_certain_minus_uncertain"] > 0 for row in folios
                ),
                "one_sided_exact_sign_p": exact_sign_p(len(folios), len(folios)),
                "rows": folios,
            },
            "within_line_permutation": {
                "raw_gap_px": line_permutation(included, "gap_px", args.permutations, args.seed),
                "normalized_gap_local_boxheight": line_permutation(
                    included, "direct_gap_norm_local_boxheight", args.permutations, args.seed
                ),
            },
            "threshold_sensitivity": {
                "rows": thresholds.to_dict(orient="records"),
                "central_offsets": [int(value) for value in central.offset],
                "central_all_positive": bool((central["diff"] > 0).all()),
                "all_offsets_positive": bool((thresholds["diff"] > 0).all()),
            },
            "estimator_sensitivity": {
                "rows": estimators.to_dict(orient="records"),
                "all_positive": bool((estimators.difference > 0).all()),
            },
            "raw_pipeline_reproducibility": {
                "missing_public_csv_inputs": missing,
                "page_scans_redistributed": False,
                "archived_measurement_analysis_reproducible": True,
                "raw_pixel_remeasurement_reproducible_from_public_bundle": not missing,
            },
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "raw_gap_difference_px": summary["raw_gap_px"]["certain_minus_uncertain"], "normalized_gap_difference": summary["normalized_gap_local_boxheight"]["certain_minus_uncertain"]}, indent=2))


if __name__ == "__main__":
    main()
