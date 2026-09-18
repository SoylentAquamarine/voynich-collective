#!/usr/bin/env python3
"""Test whether first-N source ordering drives the language-baseline result.

For each pinned UD corpus used by ``language_baselines.py``, this script:

1. measures every non-overlapping 39,020-token window in source order; and
2. measures 200 deterministic samples made by shuffling whole sentences,
   then taking complete sentences until the target is reached (trimming only
   the final sentence to exactly 39,020 tokens).

The second design removes the original first-N/document-order dependence
while preserving every sampled word internally. It is sentence-randomized,
not a true document-stratified bootstrap: Latin ITTB does not expose reliable
``newdoc`` boundaries in its CoNLL-U files. That limitation is reported rather
than hidden.
"""

from __future__ import annotations

import json
import random
import statistics
import tempfile
from pathlib import Path

from language_baselines import (
    CORPORA,
    REPO_ROOT,
    TARGET_TOKENS,
    download_verified,
    letters_only,
    load_voynich_words,
    metrics,
)


OUT_REPORT = REPO_ROOT / "data" / "derived" / "baseline-sampling-sensitivity-report.md"
OUT_SUMMARY = REPO_ROOT / "data" / "derived" / "baseline-sampling-sensitivity-summary.json"
OUT_CHART = REPO_ROOT / "docs" / "assets" / "baseline-sampling-sensitivity.svg"
REPLICATES = 200
SAMPLE_SEED = 20260919


def load_conllu_sentences(paths: list[Path]) -> list[list[str]]:
    """Return eligible word forms grouped by CoNLL-U sentence."""
    sentences: list[list[str]] = []
    current: list[str] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as source:
            for line in source:
                if line == "\n":
                    if current:
                        sentences.append(current)
                        current = []
                    continue
                if not line or line.startswith("#"):
                    continue
                columns = line.rstrip("\n").split("\t")
                if len(columns) != 10:
                    continue
                token_id, form, _lemma, upos = columns[:4]
                if "-" in token_id or "." in token_id or upos in {"PUNCT", "SYM"}:
                    continue
                word = letters_only(form)
                if word:
                    current.append(word)
        if current:
            sentences.append(current)
            current = []
    return sentences


def constraint(words: list[str]) -> float:
    result, _rendered = metrics(words, "sampling sensitivity")
    return result["constraint_ratio"]


def random_sentence_sample(sentences: list[list[str]], seed: int) -> list[str]:
    order = list(range(len(sentences)))
    random.Random(seed).shuffle(order)
    sample: list[str] = []
    for index in order:
        needed = TARGET_TOKENS - len(sample)
        if needed <= 0:
            break
        sample.extend(sentences[index][:needed])
    if len(sample) != TARGET_TOKENS:
        raise RuntimeError(f"Could only sample {len(sample)} of {TARGET_TOKENS} tokens")
    return sample


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def summarize(values: list[float]) -> dict:
    return {
        "n": len(values),
        "mean": round(statistics.mean(values), 6),
        "stdev": round(statistics.stdev(values), 6) if len(values) > 1 else 0.0,
        "min": min(values),
        "p05": round(percentile(values, 0.05), 6),
        "median": round(statistics.median(values), 6),
        "p95": round(percentile(values, 0.95), 6),
        "max": max(values),
    }


def make_chart(voynich: float, results: list[dict]) -> str:
    width, height = 920, 330
    left, right = 210, 50
    plot_width = width - left - right
    x_max = 0.50

    def x(value: float) -> float:
        return left + (value / x_max) * plot_width

    colors = ["#496a63", "#9b5948"]
    rows = []
    for index, result in enumerate(results):
        y = 135 + index * 90
        stats = result["random_sentence_samples"]
        rows.extend(
            [
                f'<text x="{left - 18}" y="{y + 5}" text-anchor="end" class="label">{result["short_label"]}</text>',
                f'<line x1="{x(stats["min"]):.1f}" y1="{y}" x2="{x(stats["max"]):.1f}" y2="{y}" class="range"/>',
                f'<line x1="{x(stats["p05"]):.1f}" y1="{y}" x2="{x(stats["p95"]):.1f}" y2="{y}" class="interval" style="stroke:{colors[index]}"/>',
                f'<circle cx="{x(stats["mean"]):.1f}" cy="{y}" r="7" fill="{colors[index]}"/>',
                f'<circle cx="{x(result["first_n_constraint"]):.1f}" cy="{y}" r="5" class="first"/>',
            ]
        )

    ticks = []
    for tick in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]:
        xpos = x(tick)
        ticks.append(f'<line x1="{xpos:.1f}" y1="70" x2="{xpos:.1f}" y2="260" class="grid"/>')
        ticks.append(f'<text x="{xpos:.1f}" y="285" text-anchor="middle" class="tick">{tick:.1f}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Constraint ratios across randomized language samples</title>
  <desc id="desc">Latin and Italian randomized samples remain near 0.22 and 0.23, far below the fixed Voynich value of {voynich:.4f}. Thick bars show fifth to ninety-fifth percentiles, thin bars minima to maxima, filled dots means, and hollow dots the original first-N samples.</desc>
  <style>
    .title {{ font: 700 20px Georgia, serif; fill: #2d2922; }}
    .subtitle, .tick, .legend {{ font: 13px Arial, sans-serif; fill: #665f53; }}
    .label {{ font: 700 15px Arial, sans-serif; fill: #2d2922; }}
    .grid {{ stroke: #cec5b4; stroke-width: 1; }}
    .range {{ stroke: #756d60; stroke-width: 2; }}
    .interval {{ stroke-width: 12; stroke-linecap: round; }}
    .first {{ fill: #f6f0e3; stroke: #2d2922; stroke-width: 2; }}
    .voynich {{ stroke: #5e2f2f; stroke-width: 3; stroke-dasharray: 7 5; }}
  </style>
  <rect width="100%" height="100%" fill="#f6f0e3"/>
  <text x="{left}" y="30" class="title">First-N ordering does not explain the constraint gap</text>
  <text x="{left}" y="52" class="subtitle">200 deterministic sentence-randomized samples per corpus; each sample = {TARGET_TOKENS:,} tokens</text>
  {''.join(ticks)}
  <line x1="{x(voynich):.1f}" y1="70" x2="{x(voynich):.1f}" y2="260" class="voynich"/>
  <text x="{x(voynich) - 8:.1f}" y="86" text-anchor="end" class="legend">Voynich {voynich:.4f}</text>
  {''.join(rows)}
  <text x="{left}" y="318" class="legend">Thick: 5th–95th percentile · thin: min–max · filled: mean · hollow: original first-N</text>
</svg>
'''


def main() -> None:
    voynich_words = load_voynich_words()
    voynich_constraint = constraint(voynich_words)
    corpus_results: list[dict] = []

    with tempfile.TemporaryDirectory(prefix="voynich-sampling-") as temporary:
        temp_dir = Path(temporary)
        for corpus_index, corpus in enumerate(CORPORA):
            paths: list[Path] = []
            for filename, checksum in corpus["files"]:
                destination = temp_dir / filename
                download_verified(corpus, filename, checksum, destination)
                paths.append(destination)

            sentences = load_conllu_sentences(paths)
            all_words = [word for sentence in sentences for word in sentence]
            if len(all_words) < TARGET_TOKENS:
                raise RuntimeError(f"{corpus['label']} has only {len(all_words)} eligible tokens")

            first_n = constraint(all_words[:TARGET_TOKENS])
            contiguous = [
                constraint(all_words[start : start + TARGET_TOKENS])
                for start in range(0, len(all_words) - TARGET_TOKENS + 1, TARGET_TOKENS)
            ]
            randomized = [
                constraint(random_sentence_sample(sentences, SAMPLE_SEED + corpus_index * 10_000 + replicate))
                for replicate in range(REPLICATES)
            ]
            corpus_results.append(
                {
                    "key": corpus["key"],
                    "label": corpus["label"],
                    "short_label": "Medieval Latin" if corpus["key"] == "latin_ittb" else "Italian",
                    "eligible_tokens": len(all_words),
                    "sentences": len(sentences),
                    "first_n_constraint": first_n,
                    "nonoverlapping_contiguous_windows": summarize(contiguous),
                    "random_sentence_samples": summarize(randomized),
                    "random_sample_values": randomized,
                    "minimum_gap_from_voynich": round(voynich_constraint - max(randomized), 4),
                }
            )

    summary = {
        "method": "non-overlapping source-order windows plus sentence-randomized samples without replacement",
        "target_tokens": TARGET_TOKENS,
        "replicates": REPLICATES,
        "sample_seed": SAMPLE_SEED,
        "voynich_constraint": voynich_constraint,
        "corpora": corpus_results,
        "limitation": "Sentence-randomized, not document-stratified; Latin ITTB lacks reliable newdoc boundaries.",
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    table = [
        "| Corpus | Eligible tokens | Windows | First N | Contiguous range | Random mean ± SD | Random 5–95% | Random max | Min gap to Voynich |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for result in corpus_results:
        windows = result["nonoverlapping_contiguous_windows"]
        samples = result["random_sentence_samples"]
        table.append(
            f"| {result['short_label']} | {result['eligible_tokens']:,} | {windows['n']} | "
            f"{result['first_n_constraint']:.4f} | {windows['min']:.4f}–{windows['max']:.4f} | "
            f"{samples['mean']:.4f} ± {samples['stdev']:.4f} | {samples['p05']:.4f}–{samples['p95']:.4f} | "
            f"{samples['max']:.4f} | {result['minimum_gap_from_voynich']:.4f} |"
        )

    report = [
        "# Baseline Sampling-Sensitivity Check",
        "",
        "Generated by `data/scripts/baseline_sampling_sensitivity.py` from the same pinned, checksum-verified corpora and exact metric implementation used in `language_baselines.py`.",
        "",
        "## Question",
        "",
        "Does selecting the first 39,020 eligible Latin and Italian tokens create the reported 0.2164/0.2310 constraint ratios through source-order or document clustering?",
        "",
        "## Method",
        "",
        f"For each corpus, the script measures every full non-overlapping {TARGET_TOKENS:,}-token window in source order. It then makes {REPLICATES} deterministic samples by shuffling whole CoNLL-U sentences without replacement, concatenating them, and trimming only the final sentence to exactly {TARGET_TOKENS:,} tokens. Words and word-internal character order are never altered. Seed family: `{SAMPLE_SEED}`.",
        "",
        "This directly tests dependence on the original first-N ordering. It is not a true document-stratified bootstrap: Latin ITTB does not provide reliable `newdoc` boundaries, and its related Thomistic works are not an independent genre panel. The result therefore resolves the narrow sampling-order objection, not the broader corpus-diversity objection.",
        "",
        "## Results",
        "",
        f"Fixed Voynich constraint ratio: **{voynich_constraint:.4f}**.",
        "",
        *table,
        "",
        "Across all randomized samples, neither language approaches Voynich. The closest randomized baseline remains separated by the `Min gap to Voynich` shown above. Both original first-N values fall inside their corpus's much wider non-overlapping contiguous-window range. Sentence randomization lowers the Latin estimate slightly and raises the Italian estimate slightly, without materially narrowing the Voynich gap.",
        "",
        "## Interpretation",
        "",
        "- The local-constraint gap is not an artifact of taking the first 39,020 tokens from these two pinned corpora.",
        "- This strengthens only the narrow confirmed finding that this Voynich representation is more locally constrained than these Latin and Italian baselines.",
        "- It still does not distinguish language, cipher, or mechanically generated pseudo-text.",
        "- The two-language, Indo-European, genre, morphology, orthography, and EVA-tokenization limitations remain unresolved.",
    ]
    OUT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    OUT_CHART.write_text(make_chart(voynich_constraint, corpus_results), encoding="utf-8")
    print(f"Wrote {OUT_REPORT}")
    print(f"Wrote {OUT_SUMMARY}")
    print(f"Wrote {OUT_CHART}")


if __name__ == "__main__":
    main()
