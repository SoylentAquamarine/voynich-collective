#!/usr/bin/env python3
"""Ten-seed anchors and ten-seed beta_A=0.4172 for the damping-ratio thread.

Design and predictions: logs/2026-11-04-damping-ratio-ten-seed-anchors-selfreview.md
(committed before this ran).

Runs (manifest seeds 0-9):
  1. coupling-only, uniform beta 0.5          (re-measures the hard-coded +0.0064 baseline)
  2. full pipeline, anchor 0.5/0.5            (seeds 0-2 reproduce committed rows)
  3. full pipeline + coupling-only, beta_A=0.4172 (seeds 0-2 reproduce committed rows)
  4. beta_A=0.48: committed 10-seed rows reused; seed 42 re-run on both sides as a check.

Usage:
    python data/scripts/external_damping_ratio_ten_seed_anchors_check.py <units_repo>
"""

from __future__ import annotations

import json
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "data" / "scripts"))
import external_coupling_v2_section_aware_preregistered as base
import external_coupling_v2_section_varying_beta_check as prior

DERIVED = ROOT / "data" / "derived"
OUT_JSON = DERIVED / "external-damping-ratio-ten-seed-anchors-check-summary.json"
SEED_COUNT = 10
BOOT_N = 10_000
BOOT_SEED = 20261104
TOL = 1e-9


def committed():
    rec = json.loads((DERIVED / "external-coupling-v2-recalibrated-beta-check-summary.json").read_text())
    iso4172 = json.loads((DERIVED / "external-coupling-only-beta-curvature-check-summary.json").read_text())
    full48 = json.loads((DERIVED / "external-coupling-v2-limit-point-full-pipeline-more-seeds-check-summary.json").read_text())
    iso48 = json.loads((DERIVED / "external-coupling-only-beta-limit-point-more-seeds-check-summary.json").read_text())
    return {
        "full_anchor": {r["cipher_seed"]: r["edge_gain_gap"] for r in rec["anchor"]["rows"]},
        "full_4172": {r["cipher_seed"]: r["edge_gain_gap"] for r in rec["design"]["rows"]},
        "iso_4172": {r["cipher_seed"]: r["edge_gain_gap"] for r in iso4172["rows"]},
        "full_48": [r["edge_gain_gap"] for r in full48["all_rows"]],
        "iso_48": [r["edge_gain_gap"] for r in iso48["all_rows"]],
    }


def coupling_only(atomic, token_labels, beta_a, beta_b, seed):
    rng = random.Random(seed)
    return prior.apply_section_varying_coupling(
        atomic, token_labels, {"A": beta_a, "B": beta_b, "?": beta_b}, rng)


def main() -> None:
    units_repo = Path(sys.argv[1]).resolve()
    t0 = time.time()

    def log(m):
        print(f"[{time.time()-t0:7.1f}s] {m}", flush=True)

    (source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args,
     token_labels, line_lengths, currier_labels_by_line, real_gap) = base.setup(units_repo, log)
    manifest = json.loads(base.COUPLING_V2_MANIFEST_PATH.read_text(encoding="utf-8"))
    cseeds = manifest["seeds"]["cipher"][:SEED_COUNT]
    pseeds = manifest["seeds"]["postprocessor"][:SEED_COUNT]
    known = committed()

    def gap(tokens):
        expanded = [base.expand(t) for t in tokens]
        g, _a, _b = prior.section_edge_gain_gap(expanded, line_lengths, currier_labels_by_line, scale)
        return expanded, g

    rows = {k: [] for k in ("iso_uniform", "full_anchor", "full_4172", "iso_4172")}
    passes = {"full_anchor": [], "full_4172": []}
    repro = []
    for i in range(SEED_COUNT):
        cs, ps = cseeds[i], pseeds[i]
        atomic = [headlines.collapse(t) for t in cipher.encrypt(letters, cs)["tokens"]]
        _, g = gap(coupling_only(atomic, token_labels, 0.5, 0.5, ps)); rows["iso_uniform"].append(g)
        _, g = gap(coupling_only(atomic, token_labels, 0.4172, 0.5, ps)); rows["iso_4172"].append(g)
        for key, ba in (("full_anchor", 0.5), ("full_4172", 0.4172)):
            exp, g = gap(prior.transform(atomic, token_labels, ba, 0.5, ps))
            ev = base.evaluate_replicate(exp, targets, naibbe_module, scale, args, modules)
            rows[key].append(g); passes[key].append(ev["all_six_pass"])
        if i == 0:
            _, g_iso48 = gap(coupling_only(atomic, token_labels, 0.48, 0.5, ps))
            _, g_full48 = gap(prior.transform(atomic, token_labels, 0.48, 0.5, ps))
            repro.append({"what": "iso_48 seed 42", "rerun": g_iso48, "committed": known["iso_48"][0]})
            repro.append({"what": "full_48 seed 42", "rerun": g_full48, "committed": known["full_48"][0]})
        for key in ("full_anchor", "full_4172", "iso_4172"):
            if cs in known[key]:
                repro.append({"what": f"{key} seed {cs}", "rerun": rows[key][-1], "committed": known[key][cs]})
        log(f"seed {cs}: " + " ".join(f"{k}={v[-1]:.5f}" for k, v in rows.items()))

    for r in repro:
        r["abs_diff"] = abs(r["rerun"] - r["committed"])
        r["match"] = r["abs_diff"] <= TOL
    all_match = all(r["match"] for r in repro)
    log(f"reproduction gate: {'PASS' if all_match else 'FAIL'} ({sum(r['match'] for r in repro)}/{len(repro)})")

    rows["full_48"] = known["full_48"]
    rows["iso_48"] = known["iso_48"]
    # 0.0064 is reported as "+0.0064" -- possibly rounded; compare to rerun mean of seeds 0-2.

    def ratio(idx, b):
        m = lambda k: statistics.fmean(rows[k][j] for j in idx)
        return (m(f"full_{b}") - m("full_anchor")) / (m(f"iso_{b}") - m("iso_uniform"))

    full_idx = list(range(SEED_COUNT))
    point = {b: ratio(full_idx, b) for b in ("4172", "48")}
    rng = random.Random(BOOT_SEED)
    boots = {"4172": [], "48": [], "D": []}
    for _ in range(BOOT_N):
        idx = [rng.randrange(SEED_COUNT) for _ in range(SEED_COUNT)]
        r1, r2 = ratio(idx, "4172"), ratio(idx, "48")
        boots["4172"].append(r1); boots["48"].append(r2); boots["D"].append(r1 - r2)

    def ci(xs):
        s = sorted(xs)
        return [s[int(0.025 * len(s))], s[int(0.975 * len(s)) - 1]]

    intervals = {k: ci(v) for k, v in boots.items()}
    D = point["4172"] - point["48"]
    resolved = intervals["D"][0] > 0
    means = {k: statistics.fmean(v) for k, v in rows.items()}
    sds = {k: statistics.stdev(v) for k, v in rows.items()}
    # Consistent-definition recomputation of the on-file 0.48 ratio (committed anchors).
    consistent_on_file_48 = ((statistics.fmean(known["full_48"]) - (-0.05574867702325522))
                             / (statistics.fmean(known["iso_48"]) - 0.0064))
    log(f"means: {json.dumps({k: round(v, 5) for k, v in means.items()})}")
    log(f"ratio 0.4172 = {point['4172']:.4f} CI {intervals['4172']}")
    log(f"ratio 0.48   = {point['48']:.4f} CI {intervals['48']}")
    log(f"D = {D:.4f} CI {intervals['D']} -> resolved={resolved}")
    log(f"on-file 0.48 ratio under consistent definition (committed 3-seed anchors): {consistent_on_file_48:.4f}")

    summary = {
        "design_log": "logs/2026-11-04-damping-ratio-ten-seed-anchors-selfreview.md",
        "external_commit": source["commit"],
        "cipher_seeds": cseeds, "post_seeds": pseeds,
        "rows": rows, "all_six_pass": passes,
        "means": means, "stdevs": sds,
        "iso_uniform_mean_seeds_0_2": statistics.fmean(rows["iso_uniform"][:3]),
        "reproduction_checks": repro, "reproduction_gate_pass": all_match,
        "damping_ratio_10seed": point,
        "bootstrap": {"n": BOOT_N, "seed": BOOT_SEED, "ci95": intervals},
        "D_4172_minus_48": D, "dip_resolved_as_real": resolved,
        "on_file_048_ratio_consistent_definition": consistent_on_file_48,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
