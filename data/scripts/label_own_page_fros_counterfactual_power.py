#!/usr/bin/env python3
"""Concentrated-anchor power for the frozen label own-page test.

fRos-excluded counterfactual variant. Precommit: logs/2026-11-14-fros-excluded-counterfactual-selfreview.md (f4c8c15, before code).
Copy of label_own_page_richest_matched_dose_power.py; only the anchored page sets (cells A/B/C) and seed changed.
Post-hoc diagnostic; per-transcription rate = min(1, 11.8 / eligible label tokens on selected pages).
Reuses label_own_page_power.py helpers unchanged. Anchors are planted only on a hash-random subset of round(f*N) pages,
at per-token rate min(1, q/f). Frozen rule unchanged. Structural only.
"""
from __future__ import annotations
import hashlib, importlib.util, json
from collections import defaultdict
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pw", HERE / "label_own_page_power.py")
pw = importlib.util.module_from_spec(spec); spec.loader.exec_module(pw)
ROOT = pw.ROOT
OUT = ROOT / "data" / "derived" / "label-own-page-fros-counterfactual-power.json"
CELLS = ["A_top5_minus_fRos", "B_top5", "C_fRos_only"]
TARGET = 11.8
REPS, SEED = pw.REPS, 20261114


def h01(*parts):
    d = hashlib.sha256("|".join(map(str, (SEED,) + parts)).encode()).digest()
    return int.from_bytes(d[:8], "big") / 2**64


def main():
    hdr = pw.mq.headers(pw.pr.ZL)
    data = {name: pw.prep(path, hdr) for name, path in pw.INPUTS.items()}
    allpages = sorted(set().union(*[set(d[0]) for d in data.values()]))
    rng = np.random.default_rng(SEED)
    rich = sorted(allpages, key=lambda p: (-max(len(d[1].get(p, [])) for d in data.values()), p))
    print("richest pages:", rich[:6])
    out = {"precommit": "logs/2026-11-14-fros-excluded-counterfactual-selfreview.md", "richest_top6": rich[:6], "reps": REPS,
           "n_perm": pw.NPERM, "seed": SEED, "cells_spec": CELLS, "target_hits": TARGET, "n_union_pages": len(allpages), "cells": []}
    assert rich[0] == "fRos", rich[:6]
    sets = {"A_top5_minus_fRos": rich[1:5], "B_top5": rich[:5], "C_fRos_only": ["fRos"]}
    for f in CELLS:
        anch = set(sets[f]); k = len(anch)
        elig = {n: sum(1 for p in d[0] if p in anch for w in d[1][p] if w not in d[2][p]) for n, d in data.items()}
        rates = {n: min(1.0, TARGET / e) for n, e in elig.items()}
        passes, planted = 0, defaultdict(list)
        for rep in range(REPS):
            ok = True
            for name, (pages, lab, txt, gI, gIL) in data.items():
                t2, n_pl = {}, 0
                for p in pages:
                    s = set(txt[p])
                    if p in anch:
                        for j, w in enumerate(lab[p]):
                            if w not in txt[p] and h01("md", f, name, rep, p, j) < rates[name]:
                                s.add(w); n_pl += 1
                    t2[p] = s
                M = pw.exact_matrix(pages, lab, t2)
                _, _, p1 = pw.perm_p(M, gI, rng)
                _, _, p2 = pw.perm_p(M, gIL, rng)
                planted[name].append(n_pl)
                ok = ok and p1 < 0.01 and p2 < 0.05
            passes += ok
        pwr = passes / REPS
        row = {"cell": f, "pages": sorted(anch), "k_pages": k, "power": pwr, "mc_se": round(float(np.sqrt(pwr * (1 - pwr) / REPS)), 4),
               **{f"eligible_{n}": elig[n] for n in data}, **{f"rate_{n}": round(rates[n], 5) for n in data},
               **{f"planted_mean_{n}": round(float(np.mean(v)), 2) for n, v in planted.items()},
               **{f"planted_sd_{n}": round(float(np.std(v)), 2) for n, v in planted.items()}}
        out["cells"].append(row); print(json.dumps(row), flush=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
