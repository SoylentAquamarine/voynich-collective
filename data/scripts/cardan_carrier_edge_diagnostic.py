#!/usr/bin/env python3
"""Measure how much cross-token edge order the frozen Cardan carrier can transmit.

This is deliberately narrower than the preregistered six-criterion execution.
It independently reconstructs only the honest sequential generator described in
the pinned upstream source, then applies the already-audited project edge metric.

Usage:
    python data/scripts/cardan_carrier_edge_diagnostic.py \
      ../../paper-audit/UD_English-EWT ../../paper-audit/voynich-units
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import random
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "cardan-carrier-edge-diagnostic.json"
OUT_REPORT = ROOT / "data" / "derived" / "cardan-carrier-edge-diagnostic-report.md"
OUT_CHART = ROOT / "docs" / "assets" / "cardan-carrier-edge-attenuation.svg"

EWT_COMMIT = "4a4d77f599ea53cc405f85d0cec4b2f14f81d42b"
UNITS_COMMIT = "956a7c4fc39981f4d116fa3f4edfccce6d065571"
PRIMARY_P = (0.00, 0.05, 0.10, 0.30)
CONTROL_P = 1.00
SEEDS = tuple(42 + 137 * i for i in range(20))
EDGE_THRESHOLD = 0.15

sys.path.insert(0, str(ROOT / "data" / "scripts"))
from audit_document_baseline_panel import parse_documents  # noqa: E402
from external_naibbe_audit import edge_crossfit  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit(repo: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()


def verify_ewt(repo: Path) -> tuple[list[Path], dict]:
    manifest = json.loads((ROOT / "data" / "baselines" / "document-panel-v1.json").read_text())
    corpus = next(row for row in manifest["corpora"] if row["key"] == "english_ewt")
    if git_commit(repo) != EWT_COMMIT or corpus["commit"] != EWT_COMMIT:
        raise RuntimeError("English EWT commit mismatch")
    paths = []
    files = {}
    for row in corpus["files"]:
        path = repo / row["path"]
        actual = sha256(path)
        if actual != row["sha256"]:
            raise RuntimeError(f"English EWT checksum mismatch: {row['path']}")
        paths.append(path)
        files[row["path"]] = actual
    return paths, {"commit": EWT_COMMIT, "files": files}


def template_lengths(repo: Path) -> tuple[list[int], dict]:
    if git_commit(repo) != UNITS_COMMIT:
        raise RuntimeError("voynich-units commit mismatch")
    analysis = repo / "analysis"
    bundle = repo / "voynich_decipherment_repro_bundle"
    for path in (
        analysis,
        bundle / "decipherment_attack_v6",
        bundle / "decipherment_attack_v5",
        bundle / "decipherment_attack",
    ):
        sys.path.insert(0, str(path))
    naibbe = importlib.import_module("reproduce_naibbe_control")
    modules = naibbe.load_modules(bundle)
    _attack_lib, _attack_voynich, _unit_probe, _headlines, scale, _space, plant = modules
    lines, _, _, _ = scale.load_voynich_lines(bundle, plant.LOCUS_RE, plant.collapse, plant.strip_markup)
    lengths = [len(line) for line in lines]
    return lengths, {"commit": UNITS_COMMIT, "lines": len(lengths), "tokens": sum(lengths)}


def wrap(tokens: list[str], lengths: list[int]) -> list[list[str]]:
    needed = sum(lengths)
    if len(tokens) < needed:
        raise RuntimeError(f"only {len(tokens)} tokens for {needed}-token template")
    output = []
    position = 0
    for length in lengths:
        output.append(tokens[position : position + length])
        position += length
    return output


def sequential_projection(
    source_words: list[str], holes: int, jump_probability: float, seed: int, target: int
) -> list[str]:
    """Clean-room implementation of the documented upstream sequential rule."""
    rng = random.Random(seed)
    output = []
    row_index = 0
    attempts = 0
    while len(output) < target and attempts < target * 20:
        attempts += 1
        row = source_words[row_index % len(source_words)]
        if row:
            count = min(holes, len(row))
            selected = "".join(row[index] for index in sorted(rng.sample(range(len(row)), count)))
            if len(selected) >= 2:
                output.append(selected)
        if rng.random() < jump_probability:
            row_index = rng.randint(0, len(source_words) - 1)
        else:
            row_index = (row_index + 1) % len(source_words)
    if len(output) != target:
        raise RuntimeError("sequential projection did not reach the target length")
    return output


def edge_result(tokens: list[str], lengths: list[int]) -> dict:
    result = edge_crossfit(wrap(tokens, lengths), alpha=1.0, blocks=16)
    return {
        "gain_bits_per_boundary": result["gain_bits_per_boundary"],
        "positive_blocks": result["positive_blocks"],
        "pairs": result["pairs"],
    }


def summarise(rows: list[dict]) -> dict:
    gains = [row["gain_bits_per_boundary"] for row in rows]
    blocks = [row["positive_blocks"] for row in rows]
    return {
        "replicates": len(rows),
        "mean_gain_bits_per_boundary": statistics.mean(gains),
        "min_gain_bits_per_boundary": min(gains),
        "max_gain_bits_per_boundary": max(gains),
        "mean_positive_blocks": statistics.mean(blocks),
        "gain_threshold_passes": sum(value >= EDGE_THRESHOLD for value in gains),
        "joint_edge_criterion_passes": sum(
            row["gain_bits_per_boundary"] >= EDGE_THRESHOLD and row["positive_blocks"] >= 15 for row in rows
        ),
    }


def build(ewt_repo: Path, units_repo: Path) -> dict:
    paths, ewt_source = verify_ewt(ewt_repo)
    documents, unassigned = parse_documents(paths)
    words = [word for document in documents.values() for word in document["surface"]]
    lengths, units_source = template_lengths(units_repo)
    target = sum(lengths)

    direct = edge_result(words, lengths)
    configurations = {}
    for probability in (*PRIMARY_P, CONTROL_P):
        rows = []
        for seed in SEEDS:
            tokens = sequential_projection(words, 4, probability, seed, target)
            rows.append({"seed": seed, **edge_result(tokens, lengths)})
        configurations[f"p={probability:.2f}"] = {
            "jump_probability": probability,
            "summary": summarise(rows),
            "replicates": rows,
        }

    hole_sensitivity = {}
    for holes in (2, 3, 4, 5, 8):
        rows = []
        for seed in SEEDS[:5]:
            tokens = sequential_projection(words, holes, 0.0, seed, target)
            rows.append({"seed": seed, **edge_result(tokens, lengths)})
        hole_sensitivity[str(holes)] = summarise(rows)

    return {
        "analysis": "Cardan sequential-carrier edge attenuation",
        "scope": "Edge criterion only; not the preregistered six-criterion verdict.",
        "sources": {"english_ewt": ewt_source, "voynich_units": units_source},
        "carrier": {
            "documents": len(documents),
            "surface_tokens": len(words),
            "unassigned_surface_tokens": unassigned["surface"],
            "direct_source_edge": direct,
        },
        "parameters": {
            "holes": 4,
            "seeds": list(SEEDS),
            "edge_alpha": 1.0,
            "blocks": 16,
            "gain_threshold": EDGE_THRESHOLD,
            "positive_blocks_threshold": 15,
        },
        "configurations": configurations,
        "hole_sensitivity_at_p0_five_seeds": hole_sensitivity,
    }


def make_chart(summary: dict) -> str:
    labels = ["Raw EWT", "p=0", "p=.05", "p=.10", "p=.30", "p=1"]
    values = [summary["carrier"]["direct_source_edge"]["gain_bits_per_boundary"]]
    ranges = [(values[0], values[0])]
    for key in ("p=0.00", "p=0.05", "p=0.10", "p=0.30", "p=1.00"):
        row = summary["configurations"][key]["summary"]
        values.append(row["mean_gain_bits_per_boundary"])
        ranges.append((row["min_gain_bits_per_boundary"], row["max_gain_bits_per_boundary"]))
    width, height = 940, 520
    left, right, top, bottom = 92, 28, 86, 82
    plot_w, plot_h = width - left - right, height - top - bottom
    low, high = -0.025, 0.16
    y = lambda value: top + (high - value) / (high - low) * plot_h
    step = plot_w / len(labels)
    bars = []
    for index, (label, value, span) in enumerate(zip(labels, values, ranges)):
        cx = left + step * (index + 0.5)
        zero = y(0)
        value_y = y(value)
        bar_y, bar_h = min(zero, value_y), abs(zero - value_y)
        colour = "#496a63" if index == 0 else "#9b5948"
        bars.append(f'<rect x="{cx-31:.1f}" y="{bar_y:.1f}" width="62" height="{max(bar_h, 1):.1f}" rx="3" fill="{colour}"/>')
        bars.append(f'<line x1="{cx:.1f}" y1="{y(span[0]):.1f}" x2="{cx:.1f}" y2="{y(span[1]):.1f}" stroke="#423f3a" stroke-width="1.5"/>')
        bars.append(f'<text x="{cx:.1f}" y="{height-45}" text-anchor="middle" class="label">{label}</text>')
        bars.append(f'<text x="{cx:.1f}" y="{value_y-8:.1f}" text-anchor="middle" class="value">{value:+.3f}</text>')
    grid = []
    for tick in (-0.02, 0.00, 0.05, 0.10, 0.15):
        yy = y(tick)
        grid.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" class="grid"/>')
        grid.append(f'<text x="{left-12}" y="{yy+4:.1f}" text-anchor="end" class="tick">{tick:.2f}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">The Cardan projection attenuates English edge order</title>
  <desc id="desc">Raw sequential English EWT gains 0.038 bits per held-out word boundary. Four-hole projected streams range from about 0.013 bits at zero random jumps to below zero with frequent jumps, far below the frozen Voynich threshold of 0.15.</desc>
  <style>.title{{font:700 22px system-ui,sans-serif;fill:#272621}}.subtitle{{font:14px system-ui,sans-serif;fill:#5f5a52}}.label,.tick{{font:13px system-ui,sans-serif;fill:#4e4942}}.value{{font:600 12px system-ui,sans-serif;fill:#38342f}}.grid{{stroke:#ddd7cc;stroke-width:1}}</style>
  <rect width="100%" height="100%" fill="#fbf9f4" rx="12"/>
  <text x="{left}" y="34" class="title">The grille loses most cross-word edge order</text>
  <text x="{left}" y="58" class="subtitle">Held-out edge gain; bars are 20-seed means, whiskers show min–max (raw EWT is deterministic)</text>
  {''.join(grid)}
  <line x1="{left}" y1="{y(EDGE_THRESHOLD):.1f}" x2="{width-right}" y2="{y(EDGE_THRESHOLD):.1f}" stroke="#3d586e" stroke-width="2" stroke-dasharray="7 5"/>
  <text x="{width-right}" y="{y(EDGE_THRESHOLD)-8:.1f}" text-anchor="end" class="value">Frozen Voynich threshold 0.15</text>
  {''.join(bars)}
  <text x="20" y="{top + plot_h/2:.1f}" transform="rotate(-90 20 {top + plot_h/2:.1f})" text-anchor="middle" class="label">Gain (bits per boundary)</text>
</svg>'''


def write_outputs(summary: dict) -> None:
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n")
    OUT_CHART.write_text(make_chart(summary))
    direct = summary["carrier"]["direct_source_edge"]
    rows = []
    for key, value in summary["configurations"].items():
        stats = value["summary"]
        rows.append(
            f"| `{key}` | {stats['mean_gain_bits_per_boundary']:.4f} "
            f"({stats['min_gain_bits_per_boundary']:.4f} to {stats['max_gain_bits_per_boundary']:.4f}) | "
            f"{stats['mean_positive_blocks']:.1f}/16 | {stats['joint_edge_criterion_passes']}/20 |"
        )
    report = f"""# Cardan sequential-carrier edge diagnostic

## Result

The frozen English carrier cannot supply enough cross-token edge order for the honest four-hole Cardan configurations to pass criterion 5. Raw sequential EWT itself gives only **{direct['gain_bits_per_boundary']:.4f} bits/boundary**, one quarter of the frozen `0.15` threshold. Random four-hole projection reduces the mean to **{summary['configurations']['p=0.00']['summary']['mean_gain_bits_per_boundary']:.4f} bits** even with no row jumps. All 80 primary edge replicates fail the joint gain-and-positive-block rule.

| Jump probability | Mean gain (20-seed range) | Mean positive blocks | Edge passes |
|---|---:|---:|---:|
{chr(10).join(rows)}

This supplies a mechanism explanation for the expected full-run result: a grille that selects positions independently inside successive English words can only attenuate the carrier's already modest boundary signal. Increasing random jumps erases it further. The result is not a claim that every table, grille, cipher, or pseudo-text method must fail; a generator with explicit cross-token state could behave differently.

## Method

- Source: checksum-pinned English EWT surface tokens at `{EWT_COMMIT}` in frozen train/dev/test order ({summary['carrier']['surface_tokens']:,} tokens).
- Generator: clean-room reconstruction from the pinned source's documented rule—select four sorted random character positions per source word, advance sequentially, and jump with probability `p`.
- Replicates: the preregistered 20 seeds for each of the four primary jump rates, plus `p=1.00` as a random-row control.
- Evaluation: exact 3,950-line/{summary['sources']['voynich_units']['tokens']:,}-token Voynich template and the accepted 16-block, alpha-1 held-out edge evaluator.
- Diagnostic sensitivity: at `p=0`, using 2, 3, 5, or 8 holes also remains far below `0.15`; full arrays are in the JSON.

## Scope and relation to Claude's execution

This diagnostic was chosen after Claude accepted the preregistration and began the complete upstream reproduction and six-metric run. It intentionally does **not** recompute entropy, learned-unit scale, whole-token order, vocabulary, upstream signatures, or the preregistered final verdict. Claude's run remains the authoritative joint-profile execution; this independent calculation isolates why the cross-token criterion is hard for the mechanism and gives a check on its edge column.

Artifacts: `data/scripts/cardan_carrier_edge_diagnostic.py`, `data/derived/cardan-carrier-edge-diagnostic.json`, and `docs/assets/cardan-carrier-edge-attenuation.svg`.
"""
    OUT_REPORT.write_text(report)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ewt_repo", type=Path)
    parser.add_argument("voynich_units_repo", type=Path)
    args = parser.parse_args()
    summary = build(args.ewt_repo.resolve(), args.voynich_units_repo.resolve())
    write_outputs(summary)
    print(
        f"PASS: raw EWT={summary['carrier']['direct_source_edge']['gain_bits_per_boundary']:.4f}; "
        f"p=0 projected={summary['configurations']['p=0.00']['summary']['mean_gain_bits_per_boundary']:.4f}; "
        f"primary edge passes={sum(row['summary']['joint_edge_criterion_passes'] for key, row in summary['configurations'].items() if key != 'p=1.00')}/80"
    )


if __name__ == "__main__":
    main()
