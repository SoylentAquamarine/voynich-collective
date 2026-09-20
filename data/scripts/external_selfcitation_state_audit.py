#!/usr/bin/env python3
"""Audit where the published self-citation generator stores sequential state.

The checksum-pinned external driver is run unchanged with its published built-in
calibration, five seeds, and no substitution attack.  This wrapper adds the
project's held-out last-glyph -> next-first-glyph prediction test and compares
that signal with the driver's own adjacent-token edit-similarity diagnostic.

Usage:
    python data/scripts/external_selfcitation_state_audit.py \
        ../paper-audit/voynich-units
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-selfcitation-state-summary.json"
OUT_REPORT = ROOT / "data" / "derived" / "external-selfcitation-state-report.md"
OUT_CHART = ROOT / "docs" / "assets" / "external-selfcitation-edge.svg"

EXPECTED_COMMIT = "956a7c4fc39981f4d116fa3f4edfccce6d065571"
EXPECTED_DRIVER_HASH = "005eef529b314aabb917273bdd906d1cc3aff42ab348ff1b73445d494f6e84d9"
REFERENCE_LINES = 3950
SEEDS = 5
SHUFFLES = 20
BLOCKS = 16
ALPHA = 1.0

SUBS = [
    ("cth", "T"), ("ckh", "K"), ("cph", "P"), ("cfh", "F"),
    ("ch", "C"), ("sh", "S"), ("iin", "N"), ("in", "I"), ("ee", "E"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_external(repo: Path) -> dict:
    commit = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()
    driver = repo / "analysis" / "reproduce_selfcitation_control.py"
    actual_hash = sha256(driver)
    if commit != EXPECTED_COMMIT:
        raise RuntimeError(f"external repository is at {commit}, expected {EXPECTED_COMMIT}")
    if actual_hash != EXPECTED_DRIVER_HASH:
        raise RuntimeError(
            f"checksum mismatch for {driver}: {actual_hash}, expected {EXPECTED_DRIVER_HASH}"
        )
    return {"commit": commit, "driver_sha256": actual_hash}


def collapse(word: str) -> str:
    word = word.lower().strip()
    for source, replacement in SUBS:
        word = word.replace(source, replacement)
    return word


def load_lines(path: Path) -> list[list[str]]:
    lines = [line.split() for line in path.read_text(encoding="utf-8").splitlines()]
    lines = [line for line in lines if line][:REFERENCE_LINES]
    if len(lines) != REFERENCE_LINES:
        raise RuntimeError(f"{path} has {len(lines)} usable lines; expected {REFERENCE_LINES}")
    return [[collapse(token) for token in line] for line in lines]


def edge_rows(lines: list[list[str]]) -> list[tuple[int, str, str]]:
    return [
        (line_index, left[-1], right[0])
        for line_index, line in enumerate(lines)
        for left, right in zip(line, line[1:])
    ]


def edge_crossfit(lines: list[list[str]]) -> dict:
    rows = edge_rows(lines)
    folds = []
    total_gain = 0.0
    total_pairs = 0
    for fold in range(BLOCKS):
        lower = fold * len(lines) // BLOCKS
        upper = (fold + 1) * len(lines) // BLOCKS
        training = [row for row in rows if not lower <= row[0] < upper]
        testing = [row for row in rows if lower <= row[0] < upper]
        marginal = Counter(right for _, _, right in training)
        context = Counter((left, right) for _, left, right in training)
        left_count = Counter(left for _, left, _ in training)
        alphabet = set(marginal)
        categories = len(alphabet) + 1
        gain = 0.0
        for _, left, observed in testing:
            right = observed if observed in alphabet else "<unknown>"
            conditional = (context[(left, right)] + ALPHA) / (
                left_count[left] + ALPHA * categories
            )
            baseline = (marginal[right] + ALPHA) / (
                len(training) + ALPHA * categories
            )
            gain += math.log2(conditional / baseline)
        value = gain / len(testing)
        folds.append(
            {
                "block": fold + 1,
                "first_line": lower + 1,
                "last_line": upper,
                "pairs": len(testing),
                "gain_bits_per_boundary": value,
            }
        )
        total_gain += gain
        total_pairs += len(testing)
    return {
        "gain_bits_per_boundary": total_gain / total_pairs,
        "positive_blocks": sum(row["gain_bits_per_boundary"] > 0 for row in folds),
        "pairs": total_pairs,
        "folds": folds,
    }


def run_driver(repo: Path, directory: Path) -> tuple[dict, Path]:
    output = directory / "driver.json"
    dumps = directory / "dumps"
    command = [
        sys.executable,
        str(repo / "analysis" / "reproduce_selfcitation_control.py"),
        str(repo / "voynich_decipherment_repro_bundle"),
        "--skip-calibration",
        "--skip-attack",
        "--seeds",
        str(SEEDS),
        "--shuffles",
        str(SHUFFLES),
        "--json-output",
        str(output),
        "--dump-dir",
        str(dumps),
    ]
    subprocess.run(command, check=True, text=True, capture_output=True)
    return json.loads(output.read_text(encoding="utf-8")), dumps


def summarize_stream(name: str, driver_row: dict, edge: dict) -> dict:
    profile = driver_row["profile"]
    similarity = driver_row["adjacent_similarity_collapsed"]
    order = driver_row["token_order"]["order_by_cap"]["2000"]
    entropy = driver_row["entropy"]["collapsed"]
    return {
        "name": name,
        "entropy_H1": entropy["H1"],
        "entropy_H2": entropy["H2"],
        "bpe_minimum_checkpoint": driver_row["bpe"]["minimum_k"],
        "token_order_share": order["share"],
        "hapax_share_of_types": profile["hapax_share"],
        "adjacent_levenshtein_le2_observed": similarity["lev_le2"],
        "adjacent_levenshtein_le2_shuffled": similarity["lev_le2_shuffled"],
        "adjacent_levenshtein_le2_excess": (
            similarity["lev_le2"] - similarity["lev_le2_shuffled"]
        ),
        "edge_crossfit": edge,
    }


def aggregate(rows: list[dict], key_path: tuple[str, ...]) -> dict:
    values = []
    for row in rows:
        value = row
        for key in key_path:
            value = value[key]
        values.append(value)
    return {
        "mean": statistics.mean(values),
        "minimum": min(values),
        "maximum": max(values),
    }


def svg_chart(summary: dict) -> str:
    rows = [
        ("Voynich", summary["reference"]["edge_gain_bits_per_boundary"], "#496a63"),
        *[
            (f"Self-citation {index}", row["edge_crossfit"]["gain_bits_per_boundary"], "#9b5948")
            for index, row in enumerate(summary["selfcitation_seeds"], 1)
        ],
        ("Crude copy/mutate", summary["crude_control"]["edge_crossfit"]["gain_bits_per_boundary"], "#826b93"),
    ]
    width, height = 1040, 520
    left, right, top, bottom = 245, 975, 95, 450
    x_min, x_max = -0.03, 0.21

    def x(value: float) -> float:
        return left + (value - x_min) / (x_max - x_min) * (right - left)

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '  <title id="title">Self-citation state does not reproduce Voynich edge prediction</title>',
        '  <desc id="desc">Voynich has 0.187 held-out predictive bits per token boundary. Five published self-citation generator seeds and a crude copy-mutate control remain far below the preregistered 0.15 threshold.</desc>',
        '  <style>.title{font:700 22px Georgia,serif;fill:#2d2922}.subtitle,.tick,.label,.value{font:12px Arial,sans-serif;fill:#665f53}.label{font-size:13px}.value{font-weight:700}</style>',
        '  <rect width="100%" height="100%" fill="#f6f0e3"/>',
        '  <text x="70" y="34" class="title">Local copying state is not the same as boundary-glyph state</text>',
        '  <text x="70" y="58" class="subtitle">Held-out last-glyph → next-first-glyph gain; 16 contiguous line blocks, alpha=1</text>',
    ]
    for tick in (-0.02, 0.00, 0.05, 0.10, 0.15, 0.20):
        tx = x(tick)
        elements.append(f'  <line x1="{tx:.1f}" y1="{top}" x2="{tx:.1f}" y2="{bottom}" stroke="#d8cdbc" stroke-width="1"/>')
        elements.append(f'  <text x="{tx:.1f}" y="476" text-anchor="middle" class="tick">{tick:+.2f}</text>')
    threshold_x = x(0.15)
    elements.append(f'  <line x1="{threshold_x:.1f}" y1="{top-8}" x2="{threshold_x:.1f}" y2="{bottom}" stroke="#2d2922" stroke-width="2" stroke-dasharray="6 5"/>')
    elements.append(f'  <text x="{threshold_x+7:.1f}" y="87" class="tick">frozen 0.15 threshold</text>')
    zero_x = x(0.0)
    row_gap = 47
    for index, (label, value, color) in enumerate(rows):
        y = 120 + index * row_gap
        start = min(zero_x, x(value))
        bar_width = max(2.0, abs(x(value) - zero_x))
        elements.append(f'  <text x="232" y="{y+5}" text-anchor="end" class="label">{label}</text>')
        elements.append(f'  <rect x="{start:.1f}" y="{y-13}" width="{bar_width:.1f}" height="22" rx="3" fill="{color}"/>')
        anchor = "start" if value >= 0 else "end"
        offset = 7 if value >= 0 else -7
        elements.append(f'  <text x="{x(value)+offset:.1f}" y="{y+4}" text-anchor="{anchor}" class="value">{value:+.4f}</text>')
    elements.append('  <text x="610" y="505" text-anchor="middle" class="label">Predictive gain (bits per boundary)</text>')
    elements.append('</svg>')
    return "\n".join(elements) + "\n"


def report(summary: dict) -> str:
    edge = summary["aggregate"]["edge_gain"]
    hapax = summary["aggregate"]["hapax_share"]
    lev = summary["aggregate"]["levenshtein_le2_excess"]
    seed_lines = []
    for row in summary["selfcitation_seeds"]:
        seed_lines.append(
            f"| {row['name']} | {row['edge_crossfit']['gain_bits_per_boundary']:+.4f} | "
            f"{row['edge_crossfit']['positive_blocks']}/16 | "
            f"{100*row['hapax_share_of_types']:.1f}% | "
            f"{100*row['adjacent_levenshtein_le2_excess']:+.2f} pp | "
            f"{row['bpe_minimum_checkpoint']} | {100*row['token_order_share']:.2f}% |"
        )
    return f"""# Self-citation state audit

## Question

Does the published Timm–Schinner self-citation generator already provide the kind of cross-token state needed to explain the Voynich edge signal, or does its state live at a different level?

## Method

- Pinned external bundle: `{summary['source']['commit']}`; driver SHA-256 `{summary['source']['driver_sha256']}`.
- Ran the external driver unchanged with its built-in published calibration (`p_copy=0.10`, replacement weights `30/50/20`), five fixed seeds, 20 shuffle replicates, and the expensive substitution attack disabled.
- Collapsed EVA with the same nine substitutions used by the external bundle.
- Evaluated the first {REFERENCE_LINES:,} generated lines with the project's existing 16-block held-out last-glyph → next-first-glyph predictor (`alpha=1`).
- Compared that edge signal with the generator driver's own adjacent-token Levenshtein≤2 excess over within-line shuffles.

The generator is deliberately favorable to the hypothesis: its parameters were calibrated against Voynich token length/vocabulary, and its default seed line is a real Voynich line. This is a mechanism diagnostic, not an independent natural-language baseline.

## Results

| Stream | Edge gain (bits/boundary) | Positive blocks | Hapax share | Levenshtein≤2 excess | BPE minimum | Token-order share |
|---|---:|---:|---:|---:|---:|---:|
| Voynich | {summary['reference']['edge_gain_bits_per_boundary']:+.4f} | {summary['reference']['positive_blocks']}/16 | {100*summary['reference']['hapax_share_of_types']:.1f}% | {100*summary['reference']['levenshtein_le2_excess']:+.2f} pp | 64 | 0.79% |
{chr(10).join(seed_lines)}
| Crude copy/mutate | {summary['crude_control']['edge_crossfit']['gain_bits_per_boundary']:+.4f} | {summary['crude_control']['edge_crossfit']['positive_blocks']}/16 | {100*summary['crude_control']['hapax_share_of_types']:.1f}% | {100*summary['crude_control']['adjacent_levenshtein_le2_excess']:+.2f} pp | {summary['crude_control']['bpe_minimum_checkpoint']} | {100*summary['crude_control']['token_order_share']:.2f}% |

Across the five faithful self-citation seeds, edge gain averages **{edge['mean']:+.4f} bits/boundary** (range {edge['minimum']:+.4f} to {edge['maximum']:+.4f}), versus **{summary['reference']['edge_gain_bits_per_boundary']:+.4f}** for Voynich. Voynich is higher in {summary['paired_comparison']['voynich_higher_seed_blocks']}/{SEEDS*BLOCKS} seed/block comparisons. The generator nevertheless preserves a local resemblance signal: its Levenshtein≤2 excess averages **{100*lev['mean']:+.2f} percentage points**, close to Voynich's **{100*summary['reference']['levenshtein_le2_excess']:+.2f} points**.

Vocabulary is intermediate rather than simply closed. Faithful seeds average **{100*hapax['mean']:.1f}%** singleton types (range {100*hapax['minimum']:.1f}–{100*hapax['maximum']:.1f}%), below Voynich's 69.7% but above Naibbe's 40–42%. All five pass the earlier frozen ≥55% openness floor, even though none reaches the Voynich point estimate. The external paper/site shorthand “does not reproduce open vocabulary” should therefore be read as *under-reproduces the Voynich degree of openness*, not “has a closed vocabulary.”

## Interpretation

This is a useful third mechanism data point, not a decipherment result. Self-citation has genuine local copy/mutation state and nearly matches Voynich's adjacent edit-similarity excess, yet remains far below the held-out edge signal. The missing ingredient is therefore narrower than generic “cross-token state”: it must make the final glyph of one token informative about the initial glyph of the next across unseen line blocks. The crude copy/mutate control shows the complementary failure—very high hapax share without the learned-unit scale or edge coupling—so rare-form generation alone is also insufficient.

Applied diagnostically to the already frozen six-part bands (not as a newly preregistered verdict), faithful self-citation passes the 64-merge scale, weak-token-order, and ≥55% hapax criteria; it fails the ≥0.15 edge threshold and generally misses the entropy bands. That intermediate profile is materially more informative than treating Naibbe and Cardan as the only two observations.

## Scope

This narrows the published Python reimplementation and calibration at five seeds. It does not reject copying-with-mutation generally, does not prove semantic text, and does not show that the edge association is intentional. A next mechanism control should encode **boundary-specific** state and freeze its coupling rule before observing outcomes; merely adding memory or novelty is no longer a discriminating design.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("external_repo", type=Path)
    args = parser.parse_args()
    repo = args.external_repo.resolve()
    source = verify_external(repo)
    with tempfile.TemporaryDirectory(prefix="selfcitation-state-audit-") as directory:
        driver, dumps = run_driver(repo, Path(directory))
        stream_rows = []
        for seed in range(1, SEEDS + 1):
            name = f"selfcite_seed{seed}"
            edge = edge_crossfit(load_lines(dumps / f"{name}.txt"))
            stream_rows.append(summarize_stream(name, driver["streams"][name], edge))
        crude_name = "crude_unit_probe"
        crude = summarize_stream(
            crude_name,
            driver["streams"][crude_name],
            edge_crossfit(load_lines(dumps / f"{crude_name}.txt")),
        )

    naibbe = json.loads(
        (ROOT / "data" / "derived" / "external-naibbe-audit-summary.json").read_text(
            encoding="utf-8"
        )
    )
    voy_edge = next(
        row for row in naibbe["edge_crossfit"]["voynich"] if row["alpha"] == ALPHA
    )
    external_driver_voynich = driver["voynich"]
    vy_similarity = external_driver_voynich["adjacent_similarity_collapsed"]
    reference = {
        "edge_gain_bits_per_boundary": voy_edge["gain_bits_per_boundary"],
        "positive_blocks": voy_edge["positive_blocks"],
        "hapax_share_of_types": external_driver_voynich["profile"]["hapax_share"],
        "levenshtein_le2_excess": vy_similarity["lev_le2"] - vy_similarity["lev_le2_shuffled"],
        "edge_folds": voy_edge["folds"],
    }
    summary = {
        "source": source,
        "configuration": {
            "seeds": SEEDS,
            "shuffles": SHUFFLES,
            "reference_lines": REFERENCE_LINES,
            "blocks": BLOCKS,
            "alpha": ALPHA,
            "external_parameters": driver["parameters"],
            "external_calibration_rerun": False,
        },
        "reference": reference,
        "selfcitation_seeds": stream_rows,
        "crude_control": crude,
        "aggregate": {
            "edge_gain": aggregate(stream_rows, ("edge_crossfit", "gain_bits_per_boundary")),
            "hapax_share": aggregate(stream_rows, ("hapax_share_of_types",)),
            "levenshtein_le2_excess": aggregate(
                stream_rows, ("adjacent_levenshtein_le2_excess",)
            ),
        },
        "paired_comparison": {
            "voynich_higher_seed_blocks": sum(
                vy["gain_bits_per_boundary"] > generated["gain_bits_per_boundary"]
                for row in stream_rows
                for vy, generated in zip(reference["edge_folds"], row["edge_crossfit"]["folds"])
            ),
            "comparisons": SEEDS * BLOCKS,
        },
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    OUT_REPORT.write_text(report(summary), encoding="utf-8")
    OUT_CHART.write_text(svg_chart(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
