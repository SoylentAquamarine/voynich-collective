#!/usr/bin/env python3
"""Checks the section-varying-beta design named in
logs/2026-09-26-claude-coupling-v2-section-varying-beta-selfreview.md,
using coupling-v2's own 3 pilot seeds.

New: apply_section_varying_coupling (beta looked up per-token by Currier
section, instead of one global value) and a per-section generated
edge-gain-gap criterion (analogous to section_gap's H2 version, but using
edge_crossfit). Everything downstream (boundary-shift-v2, substitution
top-up) stays at its existing global primary values -- only beta varies.

Usage:
    python data/scripts/external_coupling_v2_section_varying_beta_check.py <units_repo>
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "data" / "scripts"))
import external_coupling_v2_section_aware_preregistered as base

OUT_JSON = ROOT / "data" / "derived" / "external-coupling-v2-section-varying-beta-check-summary.json"

ANCHOR = {"beta_a": 0.5, "beta_b": 0.5}
DESIGN = {"beta_a": 0.2245, "beta_b": 0.5}
BETA_DEFAULT = 0.5
NU_SHIFT_FIXED = 1.0
NU_SUB_FIXED = 0.01
ANCHOR_CHECK_THRESHOLD = 0.05


def apply_section_varying_coupling(atomic_tokens, token_labels, beta_by_label, rng):
    """Identical to apply_coupling_v2, except beta is looked up per-token
    from that token's Currier-label section."""
    output = []
    prev_last = None
    for i, token in enumerate(atomic_tokens):
        candidate = list(token)
        label = token_labels[i] if i < len(token_labels) else "?"
        beta = beta_by_label[label]
        if i > 0 and rng.random() < beta:
            candidate[0] = prev_last
        candidate_str = "".join(candidate)
        output.append(candidate_str)
        prev_last = candidate_str[-1]
    return output


def transform(atomic_tokens, token_labels, beta_a, beta_b, seed):
    rng = random.Random(seed)
    beta_by_label = {"A": beta_a, "B": beta_b, "?": BETA_DEFAULT}
    coupled = apply_section_varying_coupling(atomic_tokens, token_labels, beta_by_label, rng)
    shifted = base.apply_boundary_shift_v2(coupled, NU_SHIFT_FIXED, rng)
    nu_by_label = {"A": NU_SUB_FIXED, "B": NU_SUB_FIXED, "?": NU_SUB_FIXED}
    topped_up = base.apply_section_varying_substitution_topup(shifted, token_labels, nu_by_label, rng)
    return topped_up


def section_edge_gain_gap(expanded_tokens, line_lengths, currier_labels_by_line, scale):
    gen_lines = scale.wrap_to_lengths(expanded_tokens, line_lengths)
    a_lines = [line for line, label in zip(gen_lines, currier_labels_by_line) if label == "A"]
    b_lines = [line for line, label in zip(gen_lines, currier_labels_by_line) if label == "B"]
    a_edge = base.edge_crossfit(a_lines, alpha=1.0, blocks=16)
    b_edge = base.edge_crossfit(b_lines, alpha=1.0, blocks=16)
    return a_edge["gain_bits_per_boundary"] - b_edge["gain_bits_per_boundary"], a_edge, b_edge


def main() -> None:
    units_repo = Path(sys.argv[1]).resolve()
    started = time.time()

    def log(m):
        print(f"[{time.time()-started:7.1f}s] {m}", flush=True)

    (source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args,
     token_labels, line_lengths, currier_labels_by_line, real_gap) = base.setup(units_repo, log)

    real_edge_gap_json = ROOT / "data" / "derived" / "external-currier-ab-real-edge-gain-stats-summary.json"
    real_edge = json.loads(real_edge_gap_json.read_text(encoding="utf-8"))
    real_edge_gain_gap = real_edge["currier_a"]["gain_bits_per_boundary"] - real_edge["currier_b"]["gain_bits_per_boundary"]
    log(f"real edge-gain gap (A-B): {real_edge_gain_gap:.4f} bits/boundary")

    manifest = json.loads(base.COUPLING_V2_MANIFEST_PATH.read_text(encoding="utf-8"))
    pilot_cipher_seeds = manifest["seeds"]["cipher"][:3]
    pilot_post_seeds = manifest["seeds"]["postprocessor"][:3]

    atomic_cache = {}
    for i, cs in enumerate(pilot_cipher_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic_cache[i] = [headlines.collapse(t) for t in encrypted["tokens"]]

    def run_config(name, beta_a, beta_b):
        rows = []
        for i in range(3):
            transformed = transform(atomic_cache[i], token_labels, beta_a, beta_b, pilot_post_seeds[i])
            expanded = [base.expand(t) for t in transformed]
            ev = base.evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
            gap, a_edge, b_edge = section_edge_gain_gap(expanded, line_lengths, currier_labels_by_line, scale)
            rows.append({
                "cipher_seed": pilot_cipher_seeds[i], "all_six_pass": ev["all_six_pass"],
                "H1": ev["H1"], "H2": ev["H2"],
                "pooled_edge_gain": ev["edge_gain_bits_per_boundary"],
                "a_edge_gain": a_edge["gain_bits_per_boundary"], "b_edge_gain": b_edge["gain_bits_per_boundary"],
                "edge_gain_gap": gap,
            })
            log(f"{name} seed {pilot_cipher_seeds[i]}: all_six_pass={ev['all_six_pass']} "
                f"pooled_edge={ev['edge_gain_bits_per_boundary']:.4f} "
                f"A_edge={a_edge['gain_bits_per_boundary']:.4f} B_edge={b_edge['gain_bits_per_boundary']:.4f} "
                f"gap={gap:.4f}")
        mean_gap = sum(r["edge_gain_gap"] for r in rows) / len(rows)
        all_pass = all(r["all_six_pass"] for r in rows)
        return {"name": name, "beta_a": beta_a, "beta_b": beta_b, "rows": rows,
                 "mean_edge_gain_gap": mean_gap, "all_three_seeds_pass_six_criteria": all_pass}

    anchor_result = run_config("anchor", ANCHOR["beta_a"], ANCHOR["beta_b"])
    anchor_check_pass = abs(anchor_result["mean_edge_gain_gap"]) < ANCHOR_CHECK_THRESHOLD
    log(f"anchor check: mean_gap={anchor_result['mean_edge_gain_gap']:.4f} "
        f"threshold={ANCHOR_CHECK_THRESHOLD} pass={anchor_check_pass}")

    design_result = run_config("design", DESIGN["beta_a"], DESIGN["beta_b"])
    log(f"design mean_edge_gain_gap={design_result['mean_edge_gain_gap']:.4f} "
        f"({100*design_result['mean_edge_gain_gap']/real_edge_gain_gap:.2f}% of real "
        f"{real_edge_gain_gap:.4f}) all_pass={design_result['all_three_seeds_pass_six_criteria']}")

    summary = {
        "design_log": "logs/2026-09-26-claude-coupling-v2-section-varying-beta-selfreview.md",
        "real_edge_gain_gap_a_minus_b": real_edge_gain_gap,
        "anchor_check": {"threshold": ANCHOR_CHECK_THRESHOLD, "pass": anchor_check_pass,
                          "mean_edge_gain_gap": anchor_result["mean_edge_gain_gap"]},
        "anchor": anchor_result,
        "design": design_result,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
