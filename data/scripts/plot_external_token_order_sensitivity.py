#!/usr/bin/env python3
"""Render the closest equal-coverage token-order comparison as SVG."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    result = json.loads(args.summary.read_text())
    names = ("Voynich observed separators", "Latin botanical")
    labels = ("Voynich", "Latin botanical control")
    colors = ("#8f2d2d", "#356a8a")
    coverages = [0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.975]
    focused = result["closest_coverage_comparison"]["rows"]

    matplotlib.rcParams["svg.hashsalt"] = "voynich-token-order-sensitivity"
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    figure, axis = plt.subplots(figsize=(7.6, 4.6))
    for name, label, color in zip(names, labels, colors):
        values = []
        for coverage in coverages:
            row = result["corpora"][name]["coverage_sensitivity"][str(coverage)]
            value = 100 * row["share_of_entropy"]
            if coverage == 0.70:
                value = 100 * focused[name]["share_of_entropy"]
            values.append(value)
        axis.plot(
            [100 * value for value in coverages],
            values,
            marker="o",
            linewidth=2,
            color=color,
            label=label,
        )

    axis.axhline(0, color="#777777", linewidth=0.8)
    axis.axvline(70, color="#999999", linewidth=0.8, linestyle="--")
    axis.annotate(
        "Near-tie at 70%\n1.841% vs 1.859%",
        xy=(70, 1.85),
        xytext=(74, 2.8),
        arrowprops={"arrowstyle": "->", "color": "#555555"},
        fontsize=9,
    )
    axis.set_title(
        "Token-order separation depends on retained vocabulary coverage",
        loc="left",
        fontweight="bold",
    )
    axis.set_xlabel("Retained token coverage (%)")
    axis.set_ylabel("Shuffle-corrected adjacent order (% of token entropy)")
    axis.grid(axis="y", color="#dddddd", linewidth=0.7)
    axis.legend(frameon=False, loc="upper right")
    axis.text(
        0,
        -0.24,
        "Broad grid: 30 within-line shuffles; highlighted 70% comparison: 1,000 shuffles.\n"
        "Equal coverage removes the fixed-type-cap advantage but does not test every corpus choice.",
        transform=axis.transAxes,
        fontsize=8.2,
        color="#555555",
    )
    figure.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.output, format="svg", metadata={"Date": None})


if __name__ == "__main__":
    main()
