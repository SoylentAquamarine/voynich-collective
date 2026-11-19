#!/usr/bin/env python3
"""Seed robustness of the Davis-hand >=4 split. Precommit: logs/2026-11-18-hand-ge4-seeds-selfreview.md
Reruns d_ge4_hand.main() unchanged with 20 alternative master seeds (20261201..20261220).
Usage: python3 -I data/scripts/d_ge4_hand_seeds.py [n_procs]"""
import contextlib, io, json, statistics, sys, tempfile
from multiprocessing import Pool
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
SEEDS = list(range(20261201, 20261221))
OUT = REPO / "data" / "derived" / "d-ge4-hand-seeds.json"
THRESH_P, THRESH_R = 0.0125, 1.20

def one(seed):
    import d_ge4_hand as h
    tmp = Path(tempfile.mkdtemp()) / f"hand-{seed}.json"
    h.SEED, h.OUT = seed, tmp
    with contextlib.redirect_stdout(io.StringIO()):
        h.main()
    return seed, json.loads(tmp.read_text())

def main():
    import d_prefix_sensitivity as dps
    dps.verify_inputs()  # parent-process preflight: a SystemExit inside Pool workers hangs p.map (logs/2026-11-19-hand-seeds-preflight-selfreview.md)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    with Pool(n) as p:
        runs = dict(p.map(one, SEEDS))
    inputs = {s: r["inputs"] for s, r in runs.items()}
    assert len({json.dumps(v, sort_keys=True) for v in inputs.values()}) == 1
    cells = {}
    for k in runs[SEEDS[0]]["cells"]:
        ps = [runs[s]["cells"][k]["ge4"]["p"] for s in SEEDS]
        rs = {round(runs[s]["cells"][k]["ge4"]["ratio"], 3) for s in SEEDS}
        passes = sum(runs[s]["cells"][k]["replicated"] for s in SEEDS)
        verdict = "seed-robust" if passes >= 19 else ("fails" if passes <= 1 else "seed-fragile")
        cells[k] = {"obs_pairs": runs[SEEDS[0]]["cells"][k]["ge4"]["obs"], "ratio_values": sorted(rs),
                    "passes_of_20": passes, "p_min": min(ps), "p_median": statistics.median(ps), "p_max": max(ps),
                    "verdict": verdict}
        print(k, cells[k]["obs_pairs"], sorted(rs), passes, round(min(ps), 5), round(statistics.median(ps), 5), round(max(ps), 5), verdict)
    out = {"precommit": "logs/2026-11-18-hand-ge4-seeds-selfreview.md", "base_script": "data/scripts/d_ge4_hand.py",
           "seeds": SEEDS, "reps": 2000, "rule": {"p_max": THRESH_P, "ratio_min": THRESH_R},
           "inputs": inputs[SEEDS[0]], "cells": cells}
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
