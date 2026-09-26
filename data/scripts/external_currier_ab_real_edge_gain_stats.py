#!/usr/bin/env python3
"""Descriptive, non-circular measurement: the REAL Voynich corpus's own
held-out cross-token edge-prediction gain (the same statistic the project's
six-criterion 'edge' test uses), computed SEPARATELY for real Currier A
lines and real Currier B lines, rather than pooled across the whole corpus.

Purpose: grounding data for a possible future section-varying-beta coupling
design (beta controls the strength of the coupling mechanism's own
cross-token dependency, which the edge-gain statistic measures most
directly) -- per this project's own non-circularity discipline, this
script computes the measurement ONLY. It does not design, select, or
propose any beta value. That remains a distinct, not-yet-started task.

Usage:
    python data/scripts/external_currier_ab_real_edge_gain_stats.py <units_repo>
"""

from __future__ import annotations

import importlib
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "data" / "scripts"))
import external_coupling_v2_section_aware_preregistered as base

OUT_JSON = ROOT / "data" / "derived" / "external-currier-ab-real-edge-gain-stats-summary.json"


def main() -> None:
    units_repo = Path(sys.argv[1]).resolve()
    started = time.time()

    def log(m):
        print(f"[{time.time()-started:7.1f}s] {m}", flush=True)

    source = base.verify_source(units_repo)
    log(f"verified source: commit {source['commit']}")

    sys.path.insert(0, str(units_repo / "analysis"))
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
    pooled_lines = observed

    def edge_stats(lines, name):
        edge = base.edge_crossfit(lines, alpha=1.0, blocks=16)
        log(f"{name}: n_lines={len(lines)} edge_gain={edge['gain_bits_per_boundary']:.4f} "
            f"positive_blocks={edge['positive_blocks']}/{edge['blocks']}")
        return edge

    pooled_edge = edge_stats(pooled_lines, "Pooled (whole corpus)")
    a_edge = edge_stats(a_lines, "Currier A")
    b_edge = edge_stats(b_lines, "Currier B")

    summary = {
        "source": source,
        "purpose": "descriptive grounding data only -- no beta value is proposed or designed here",
        "pooled": pooled_edge,
        "currier_a": a_edge,
        "currier_b": b_edge,
        "edge_gain_ratio_a_over_b": a_edge["gain_bits_per_boundary"] / b_edge["gain_bits_per_boundary"],
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
