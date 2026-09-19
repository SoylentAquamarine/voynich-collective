#!/usr/bin/env python3
"""Audit the published Naibbe cipher against the Voynich joint profile.

This script runs the checksum-pinned Naibbe positive-control driver in the
external ``voynich-units`` reproduction bundle, selects its word-level results,
and adds a project-built held-out edge-prediction comparison.  Voynich and both
Naibbe samples use the same 3,950 line-length template and the same 16
contiguous held-out blocks.

Usage:
    python data/scripts/external_naibbe_audit.py ../paper-audit/voynich-units
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-naibbe-audit-summary.json"
OUT_REPORT = ROOT / "data" / "derived" / "external-naibbe-audit-report.md"
OUT_CHART = ROOT / "docs" / "assets" / "external-naibbe-edge-crossfit.svg"

EXPECTED_COMMIT = "956a7c4fc39981f4d116fa3f4edfccce6d065571"
EXPECTED_HASHES = {
    "analysis/reproduce_naibbe_control.py": "df9f01ed8f5eefa03830e4e31904d7163e902119988e9138074ac5cb1e9ecd8e",
    "data/controls/naibbe/naibbe_tables.json": "46c1235ad1dfdcaabd7866895c0557bb0e98c465f3e324fdb10dca150933826a",
    "data/controls/naibbe/greshko_nathist_output_ciphertext.txt": "9cdf2de12f371ac7efdb2e78713f229ada508286c1717758184238a59cd64326",
    "data/controls/naibbe/greshko_nathist_pre_encryption_respaced_plaintext.txt": "4979b6826c75dd47b90d6c95ac212a34cd3735b1151ca2a524e9d13b4112e93b",
}
ALPHAS = (0.1, 0.5, 1.0, 5.0, 20.0)
BLOCKS = 16


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_external(repo: Path) -> dict:
    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if commit != EXPECTED_COMMIT:
        raise RuntimeError(f"external repository is at {commit}, expected {EXPECTED_COMMIT}")
    statuses = {}
    for relative, expected in EXPECTED_HASHES.items():
        actual = sha256(repo / relative)
        statuses[relative] = {"expected": expected, "actual": actual, "matches": actual == expected}
        if actual != expected:
            raise RuntimeError(f"checksum mismatch for {relative}: {actual}, expected {expected}")
    return {"commit": commit, "files": statuses}


def run_external(repo: Path, output: Path, ciphertext: Path) -> None:
    command = [
        sys.executable,
        str(repo / "analysis" / "reproduce_naibbe_control.py"),
        str(repo / "voynich_decipherment_repro_bundle"),
        "--skip-attack",
        "--json-output",
        str(output),
        "--dump-ciphertext",
        str(ciphertext),
    ]
    subprocess.run(command, text=True, capture_output=True, check=True)


def load_external_lines(repo: Path, ciphertext: Path):
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
    voynich, _, _, _ = scale.load_voynich_lines(bundle, plant.LOCUS_RE, plant.collapse, plant.strip_markup)
    lengths = [len(line) for line in voynich]
    # The driver's dump preserves every generated token and therefore cycles the
    # 3,950-line template.  The published comparison uses its first full template.
    caesar = [line.split() for line in ciphertext.read_text(encoding="utf-8").splitlines()][: len(lengths)]
    shipped_tokens = (repo / "data/controls/naibbe/greshko_nathist_output_ciphertext.txt").read_text(
        encoding="utf-8"
    ).split()
    pliny = scale.wrap_to_lengths(shipped_tokens, lengths)
    if [len(line) for line in caesar] != lengths:
        raise RuntimeError("generated Naibbe line template differs from Voynich reference")
    return {"voynich": voynich, "naibbe_caesar": caesar, "greshko_pliny": pliny}


def edge_rows(lines: list[list[str]]) -> list[tuple[int, str, str]]:
    return [
        (line_index, left[-1], right[0])
        for line_index, line in enumerate(lines)
        for left, right in zip(line, line[1:])
    ]


def edge_crossfit(lines: list[list[str]], alpha: float, blocks: int = BLOCKS) -> dict:
    rows = edge_rows(lines)
    folds = []
    total_gain = 0.0
    total_pairs = 0
    for fold in range(blocks):
        lower = fold * len(lines) // blocks
        upper = (fold + 1) * len(lines) // blocks
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
            conditional = (context[(left, right)] + alpha) / (left_count[left] + alpha * categories)
            baseline = (marginal[right] + alpha) / (len(training) + alpha * categories)
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
        "alpha": alpha,
        "blocks": blocks,
        "pairs": total_pairs,
        "gain_bits_per_boundary": total_gain / total_pairs,
        "positive_blocks": sum(row["gain_bits_per_boundary"] > 0 for row in folds),
        "folds": folds,
    }


def selected_metrics(row: dict) -> dict:
    bpe64 = row["bpe"]["curve"]["64"]
    order = row["order"]["order_by_cap"]["2000"]
    vocabulary = row["order"]["vocabulary"]
    entropy = row["entropy"]["collapsed"]
    return {
        "entropy_H1": entropy["H1"],
        "entropy_H2": entropy["H2"],
        "bpe_minimum_checkpoint": row["bpe"]["minimum_checkpoint"],
        "bpe_k64_gap_bits": bpe64["gap"],
        "bpe_k64_mean_unit_length": bpe64["mean_len"],
        "token_order_share": order["share"],
        "vocabulary_types": vocabulary["types"],
        "hapax_share_of_types": vocabulary["hapax_share_of_types"],
        "top_50_token_coverage": vocabulary["top_50_token_coverage"],
    }


def build_summary(repo: Path) -> dict:
    source = verify_external(repo)
    with tempfile.TemporaryDirectory(prefix="naibbe-audit-") as directory:
        temporary = Path(directory)
        driver_json = temporary / "driver.json"
        ciphertext = temporary / "naibbe-caesar.txt"
        run_external(repo, driver_json, ciphertext)
        result = json.loads(driver_json.read_text(encoding="utf-8"))
        lines = load_external_lines(repo, ciphertext)

    reference = {
        "entropy": result["reference"]["voynich_entropy"],
        "bpe": result["reference"]["voynich_bpe"],
        "order": result["reference"]["voynich_order"],
    }
    profiles = {
        "voynich": {
            "entropy_H1": reference["entropy"]["collapsed"]["H1"],
            "entropy_H2": reference["entropy"]["collapsed"]["H2"],
            "bpe_minimum_checkpoint": reference["bpe"]["minimum_checkpoint"],
            "bpe_k64_gap_bits": reference["bpe"]["curve"]["64"]["gap"],
            "bpe_k64_mean_unit_length": reference["bpe"]["curve"]["64"]["mean_len"],
            "token_order_share": reference["order"]["order_by_cap"]["2000"]["share"],
            "vocabulary_types": reference["order"]["vocabulary"]["types"],
            "hapax_share_of_types": reference["order"]["vocabulary"]["hapax_share_of_types"],
            "top_50_token_coverage": reference["order"]["vocabulary"]["top_50_token_coverage"],
        },
        "naibbe_caesar": selected_metrics(result["naibbe_caesar"]),
        "greshko_pliny": selected_metrics(result["greshko_pliny"]),
    }
    crossfit = {
        name: [edge_crossfit(corpus, alpha) for alpha in ALPHAS]
        for name, corpus in lines.items()
    }
    alpha_one = {name: next(row for row in rows if row["alpha"] == 1.0) for name, rows in crossfit.items()}
    comparisons = {}
    for control in ("naibbe_caesar", "greshko_pliny"):
        differences = [
            left["gain_bits_per_boundary"] - right["gain_bits_per_boundary"]
            for left, right in zip(alpha_one["voynich"]["folds"], alpha_one[control]["folds"])
        ]
        comparisons[control] = {
            "voynich_higher_blocks": sum(value > 0 for value in differences),
            "blocks": len(differences),
            "minimum_paired_difference": min(differences),
            "one_sided_exact_sign_p": 0.5 ** len(differences) if all(value > 0 for value in differences) else None,
        }
    table_check = result["greshko_pliny"]["table_check"]
    return {
        "source": source,
        "driver": {
            "command_mode": "default published driver with --skip-attack; 100 order shuffles",
            "deviations_from_greshko": result["cipher"]["deviations"],
            "shipped_sample_table_check": table_check,
        },
        "profiles": profiles,
        "edge_crossfit": crossfit,
        "paired_edge_comparisons": comparisons,
    }


def make_chart(summary: dict) -> str:
    rows = {
        name: next(item for item in values if item["alpha"] == 1.0)["folds"]
        for name, values in summary["edge_crossfit"].items()
    }
    width, height = 1040, 520
    left, right, top, bottom = 86, 45, 95, 70
    plot_w, plot_h = width - left - right, height - top - bottom
    all_values = [row["gain_bits_per_boundary"] for values in rows.values() for row in values]
    low, high = min(all_values) - 0.025, max(all_values) + 0.025

    def x(block: int) -> float:
        return left + (block - 1) * plot_w / (BLOCKS - 1)

    def y(value: float) -> float:
        return top + (high - value) / (high - low) * plot_h

    colors = {"voynich": "#496a63", "naibbe_caesar": "#9b5948", "greshko_pliny": "#826b93"}
    labels = {"voynich": "Voynich", "naibbe_caesar": "Naibbe / Caesar", "greshko_pliny": "Naibbe / Pliny"}
    parts = [f'<line x1="{left}" y1="{y(0):.1f}" x2="{left+plot_w}" y2="{y(0):.1f}" stroke="#6e675c" stroke-dasharray="4 4"/>']
    legend = []
    for legend_index, (name, values) in enumerate(rows.items()):
        points = " ".join(f"{x(row['block']):.1f},{y(row['gain_bits_per_boundary']):.1f}" for row in values)
        parts.append(f'<polyline points="{points}" fill="none" stroke="{colors[name]}" stroke-width="2.5"/>')
        for row in values:
            parts.append(f'<circle cx="{x(row["block"]):.1f}" cy="{y(row["gain_bits_per_boundary"]):.1f}" r="3.6" fill="{colors[name]}"><title>{labels[name]}, block {row["block"]}: {row["gain_bits_per_boundary"]:+.4f} bits</title></circle>')
        lx = left + legend_index * 180
        legend.append(f'<line x1="{lx}" y1="69" x2="{lx+24}" y2="69" stroke="{colors[name]}" stroke-width="3"/><text x="{lx+31}" y="73" class="legend">{labels[name]}</text>')
    ticks = []
    for block in range(1, BLOCKS + 1):
        ticks.append(f'<text x="{x(block):.1f}" y="{top+plot_h+24}" text-anchor="middle" class="tick">{block}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Voynich edge prediction separates from the Naibbe cipher</title>
  <desc id="desc">Across sixteen held-out contiguous line blocks, Voynich last-glyph to next-first-glyph prediction is positive in every block. Two Naibbe samples remain near zero.</desc>
  <style>
    .title {{ font: 700 22px Georgia, serif; fill: #2d2922; }}
    .subtitle, .legend, .tick, .axis {{ font: 12px Arial, sans-serif; fill: #665f53; }}
    .axis {{ font-size: 13px; }}
  </style>
  <rect width="100%" height="100%" fill="#f6f0e3"/>
  <text x="{left}" y="31" class="title">Naibbe matches word structure, but not cross-token edge order</text>
  <text x="{left}" y="54" class="subtitle">Last glyph predicts the next token's first glyph; 16 held-out blocks, alpha=1, identical line-length template</text>
  {''.join(legend)}
  {''.join(parts)}
  {''.join(ticks)}
  <text x="{left+plot_w/2:.1f}" y="{height-18}" text-anchor="middle" class="axis">Held-out contiguous line block</text>
  <text x="22" y="{top+plot_h/2:.1f}" transform="rotate(-90 22 {top+plot_h/2:.1f})" text-anchor="middle" class="axis">Predictive gain (bits per boundary)</text>
</svg>'''


def make_report(summary: dict) -> str:
    profiles = summary["profiles"]
    edge = {
        name: next(row for row in rows if row["alpha"] == 1.0)
        for name, rows in summary["edge_crossfit"].items()
    }
    profile_rows = []
    labels = {"voynich": "Voynich", "naibbe_caesar": "Naibbe / Caesar", "greshko_pliny": "Naibbe / shipped Pliny"}
    for name in ("voynich", "naibbe_caesar", "greshko_pliny"):
        row = profiles[name]
        profile_rows.append(
            f"| {labels[name]} | {row['entropy_H1']:.3f} | {row['entropy_H2']:.3f} | "
            f"{row['bpe_minimum_checkpoint']} | {row['bpe_k64_gap_bits']:.3f} | "
            f"{100*row['token_order_share']:.2f}% | {100*row['hapax_share_of_types']:.1f}% | "
            f"{edge[name]['gain_bits_per_boundary']:+.4f} | {edge[name]['positive_blocks']}/16 |"
        )
    table = summary["driver"]["shipped_sample_table_check"]
    return f"""# Naibbe cipher: mechanism-level positive-control audit

## Result

The published Naibbe cipher is a striking positive control for how little the project's early aggregate statistics identify mechanism. Two independently generated Naibbe samples nearly reproduce Voynich's character entropy, the 64-merge learned-unit minimum, learned-unit span, weak whole-token order, and low boundary crossing—even though their plaintext is known Latin and the cipher is fully reversible.

But Naibbe fails the two features that the joint-profile work identified as more discriminating:

- **Cross-token edge prediction:** with the same 3,950 line-length template and sixteen contiguous held-out blocks, Voynich gains **{edge['voynich']['gain_bits_per_boundary']:.4f} bits/boundary** and is positive in **{edge['voynich']['positive_blocks']}/16** blocks. The independently generated Caesar Naibbe sample gives **{edge['naibbe_caesar']['gain_bits_per_boundary']:.4f}** ({edge['naibbe_caesar']['positive_blocks']}/16 positive); Greshko's shipped Pliny sample gives **{edge['greshko_pliny']['gain_bits_per_boundary']:.4f}** ({edge['greshko_pliny']['positive_blocks']}/16). Voynich exceeds each control in all 16 paired blocks (one-sided exact sign p={summary['paired_edge_comparisons']['naibbe_caesar']['one_sided_exact_sign_p']:.6f}).
- **Open vocabulary:** Voynich has **{100*profiles['voynich']['hapax_share_of_types']:.1f}%** singleton types, versus **{100*profiles['naibbe_caesar']['hapax_share_of_types']:.1f}%** and **{100*profiles['greshko_pliny']['hapax_share_of_types']:.1f}%** for Naibbe.

This rules out no cipher family. It narrows one concrete, historically motivated mechanism: the published Naibbe procedure captures Voynich-like word construction extraordinarily well, but its independently sampled table choices carry essentially no state from one token edge to the next and its vocabulary closes too quickly. Any Naibbe-like explanation would need an additional cross-token state/reuse mechanism and a process that keeps creating rare forms. Adding those mechanisms after seeing the target would require a new preregistered test, not an informal patch.

## Joint profile

| Corpus | H1 | H2 | BPE minimum | k64 gap | Whole-token order | Hapax types | Held-out edge gain | Positive blocks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(profile_rows)}

The closeness of the first five columns is the important caution. Naibbe/Caesar has H1/H2 {profiles['naibbe_caesar']['entropy_H1']:.3f}/{profiles['naibbe_caesar']['entropy_H2']:.3f} versus Voynich {profiles['voynich']['entropy_H1']:.3f}/{profiles['voynich']['entropy_H2']:.3f}; both reach their dependence-gap minimum at 64 learned merges, with k64 gaps {profiles['naibbe_caesar']['bpe_k64_gap_bits']:.3f} and {profiles['voynich']['bpe_k64_gap_bits']:.3f}. A low-entropy, multi-symbol-unit, weak-token-order profile therefore can be produced by meaningful encrypted Latin.

## Provenance and execution

- Naibbe paper: Michael A. Greshko, *The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext*, *Cryptologia* (published 26 November 2025), DOI <https://doi.org/10.1080/01611194.2025.2566408>.
- Author's public code/data: <https://github.com/greshko/naibbe-cipher> and <https://doi.org/10.5281/zenodo.16415087>.
- Audited reproduction driver: Rozanova & Temerev's `voynich-units` commit `{summary['source']['commit']}`. The driver reimplements the published method from transcribed tables rather than executing Greshko's code.

All four pinned files passed SHA-256 verification. The driver reproduced **{table['unigram_tokens_reproduced']:,} unigram + {table['bigram_tokens_reproduced']:,} bigram tokens** from Greshko's shipped Pliny plaintext/ciphertext alignment with **{table['unreproducible_tokens']} failures**. It was run at its default 100 token-order shuffles with the expensive substitution attack disabled; that attack is not needed for the joint-profile comparison and remains outside this audit.

## Added held-out test

`data/scripts/external_naibbe_audit.py` first executes the external driver, then reconstructs three exactly line-matched corpora: collapsed-EVA Voynich, independently generated Naibbe/Caesar, and shipped Naibbe/Pliny. For each of 16 contiguous line blocks it trains a last-glyph -> next-first-glyph model on the other 15 blocks. Vocabulary, marginal probabilities, and transition probabilities are learned only from training blocks; unseen held-out glyphs use an explicit unknown bucket. Alpha 0.1, 0.5, 1, 5, and 20 are stored in the JSON. The Voynich/Naibbe separation is stable across the range; alpha=1 is reported above.

Contiguous blocks are not manuscript quires. That is intentional for a shared comparison because synthetic Naibbe text has no quires; the previously accepted Voynich-only result already survives genuine leave-one-quire-out testing. The line template controls the number and location of excluded line breaks but cannot make the synthetic plaintext/topical sequence equivalent to the manuscript. This is a mechanism control, not proof of language, cipher, or hoax.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("external_repo", type=Path)
    parser.add_argument("--output", type=Path, default=OUT_JSON)
    parser.add_argument("--report", type=Path, default=OUT_REPORT)
    parser.add_argument("--chart", type=Path, default=OUT_CHART)
    args = parser.parse_args()
    summary = build_summary(args.external_repo.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    args.report.write_text(make_report(summary), encoding="utf-8")
    args.chart.write_text(make_chart(summary) + "\n", encoding="utf-8")
    print(f"wrote {args.output}, {args.report}, {args.chart}")


if __name__ == "__main__":
    main()
