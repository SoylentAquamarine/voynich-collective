#!/usr/bin/env python3
"""Descriptive, non-circular Currier A/B corpus statistics: mean line length and
token-repetition rate (type-token ratio), computed directly from the real corpus,
independent of any coupling-mechanism gap statistic.

Purpose: ground data for a FUTURE, properly-designed, non-circularly-chosen
coupling dosage scheme (per knowledge-base/state.md's own "properly-designed new
coupling dosage scheme... derived from real corpus statistics rather than picked
to hit a target" note). This script computes descriptive statistics ONLY -- it
does not design, select, or propose any dosage value. That remains a distinct,
not-yet-started design task, deliberately kept separate so these numbers cannot
be reverse-engineered from a target gap.

Usage:
    python data/scripts/external_currier_ab_length_repetition_stats.py <units_repo>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-currier-ab-length-repetition-stats-summary.json"
REFERENCE_PATH = ROOT / "data" / "external" / "reference" / "boundary-state-null-baseline-edgeonly-reference.json"


def verify_source(repo: Path) -> dict:
    ref = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if commit != ref["source_commit"]:
        raise RuntimeError(f"external repository at {commit}, expected {ref['source_commit']}")
    return {"commit": commit}


def type_token_ratio(words: list[str]) -> float:
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def repetition_rate(words: list[str]) -> float:
    """Fraction of tokens that are repeats of an already-seen type (1 - hapax-adjacent measure,
    but counted as "is this occurrence a repeat", the same notion the substitution top-up mechanic
    itself keys on: candidate_str in emitted."""
    seen: set[str] = set()
    repeats = 0
    for w in words:
        if w in seen:
            repeats += 1
        seen.add(w)
    return repeats / len(words) if words else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("units_repo", type=Path)
    args = parser.parse_args()

    started = time.time()

    def log(m):
        print(f"[{time.time()-started:7.1f}s] {m}", flush=True)

    units_repo = args.units_repo.resolve()
    source = verify_source(units_repo)
    log(f"verified source: commit {source['commit']}")

    sys.path.insert(0, str(units_repo / "analysis"))
    import importlib
    naibbe_module = importlib.import_module("reproduce_naibbe_control")
    from reproduce_space_sensitivity import parse_lines

    bundle = units_repo / "voynich_decipherment_repro_bundle"
    modules = naibbe_module.load_modules(bundle)
    _attack_lib, _attack_voynich, unit_probe, headlines, scale, _space, plant = modules

    parsed, _ = parse_lines(bundle / "voynich_calibration_sources" / "ZL3b.txt", plant.LOCUS_RE, plant.strip_markup)
    currier_labels_by_line = [line["currier"] for line in parsed]
    observed, _, _, _ = scale.load_voynich_lines(bundle, plant.LOCUS_RE, plant.collapse, plant.strip_markup)
    assert len(observed) == len(currier_labels_by_line)

    a_lines = [line for line, label in zip(observed, currier_labels_by_line) if label == "A"]
    b_lines = [line for line, label in zip(observed, currier_labels_by_line) if label == "B"]
    unlabeled_lines = [line for line, label in zip(observed, currier_labels_by_line) if label not in ("A", "B")]

    def line_stats(lines, name):
        lengths = [len(line) for line in lines]
        words = [w for line in lines for w in line]
        mean_len = sum(lengths) / len(lengths) if lengths else 0.0
        ttr = type_token_ratio(words)
        rep_rate = repetition_rate(words)
        log(f"{name}: n_lines={len(lines)} mean_line_length={mean_len:.4f} "
            f"n_tokens={len(words)} type_token_ratio={ttr:.4f} repetition_rate={rep_rate:.4f}")
        return {
            "n_lines": len(lines), "mean_line_length": mean_len, "n_tokens": len(words),
            "type_token_ratio": ttr, "repetition_rate": rep_rate,
        }

    a_stats = line_stats(a_lines, "Currier A")
    b_stats = line_stats(b_lines, "Currier B")
    unlabeled_stats = line_stats(unlabeled_lines, "Unlabeled")

    summary = {
        "source": source,
        "purpose": "descriptive grounding data only -- no dosage value is proposed or designed here",
        "currier_a": a_stats,
        "currier_b": b_stats,
        "unlabeled": unlabeled_stats,
        "repetition_rate_ratio_a_over_b": (
            a_stats["repetition_rate"] / b_stats["repetition_rate"] if b_stats["repetition_rate"] else None
        ),
        "mean_length_ratio_a_over_b": (
            a_stats["mean_line_length"] / b_stats["mean_line_length"] if b_stats["mean_line_length"] else None
        ),
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
