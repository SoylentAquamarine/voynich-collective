#!/usr/bin/env python3
"""Plot the threshold sensitivity from the independent direct-pixel audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/derived/external-direct-pixel-summary.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/assets/external-direct-pixel-threshold.svg"),
    )
    args = parser.parse_args()
    summary = json.loads(args.input.read_text(encoding="utf-8"))
    rows = summary["threshold_sensitivity"]["rows"]
    x = [row["offset"] for row in rows]
    y = [row["diff"] for row in rows]

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    ax.axhspan(0, max(y) * 1.12, color="#dcefe7", alpha=0.55, zorder=0)
    ax.axhline(0, color="#594f47", linewidth=1)
    ax.plot(x, y, color="#0b6e69", marker="o", linewidth=2, markersize=5)
    ax.scatter([0], [rows[x.index(0)]["diff"]], color="#b3472f", s=55, zorder=3, label="Primary threshold")
    ax.set_xlabel("Threshold offset from bounded local Otsu")
    ax.set_ylabel("Certain − uncertain ink gap (pixels)")
    ax.set_title("Blind ink-gap result is positive across the central threshold range", loc="left", weight="bold")
    ax.set_xticks(x)
    ax.grid(axis="y", color="#d7d1c8", linewidth=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, format=args.output.suffix.lstrip("."), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
