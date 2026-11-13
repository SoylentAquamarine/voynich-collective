#!/usr/bin/env python3
"""Concentrated-anchor power for the frozen label own-page test.

Precommitted in logs/2026-11-13-label-own-page-concentrated-power-selfreview.md (commit 61c260f, before this script).
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
OUT = ROOT / "data" / "derived" / "label-own-page-concentrated-power.json"
FS = [1.0, 0.5, 0.25, 0.10]
QS = [0.0125, 0.02, 0.04, 0.08]
REPS, SEED = pw.REPS, 20261114


def h01(*parts):
    d = hashlib.sha256("|".join(map(str, (SEED,) + parts)).encode()).digest()
    return int.from_bytes(d[:8], "big") / 2**64


def main():
    hdr = pw.mq.headers(pw.pr.ZL)
    data = {name: pw.prep(path, hdr) for name, path in pw.INPUTS.items()}
    allpages = sorted(set().union(*[set(d[0]) for d in data.values()]))
    rng = np.random.default_rng(SEED)
    out = {"precommit": "logs/2026-11-13-label-own-page-concentrated-power-selfreview.md", "reps": REPS,
           "n_perm": pw.NPERM, "seed": SEED, "f_grid": FS, "q_grid": QS, "n_union_pages": len(allpages), "cells": []}
    for f in FS:
        k = round(f * len(allpages))
        for q in QS:
            rate = min(1.0, q / f)
            passes, planted = 0, defaultdict(list)
            for rep in range(REPS):
                anch = set(sorted(allpages, key=lambda p: h01("sel", f, rep, p))[:k])
                ok = True
                for name, (pages, lab, txt, gI, gIL) in data.items():
                    t2, n_pl = {}, 0
                    for p in pages:
                        s = set(txt[p])
                        if p in anch:
                            for j, w in enumerate(lab[p]):
                                if w not in txt[p] and h01("pl", f, q, rep, p, j) < rate:
                                    s.add(w); n_pl += 1
                        t2[p] = s
                    M = pw.exact_matrix(pages, lab, t2)
                    _, _, p1 = pw.perm_p(M, gI, rng)
                    _, _, p2 = pw.perm_p(M, gIL, rng)
                    planted[name].append(n_pl)
                    ok = ok and p1 < 0.01 and p2 < 0.05
                passes += ok
            row = {"f": f, "k_pages": k, "q": q, "rate_on_anchored": round(rate, 4), "power": passes / REPS,
                   **{f"planted_{n}": round(float(np.mean(v)), 2) for n, v in planted.items()}}
            out["cells"].append(row); print(json.dumps(row), flush=True)
    out["q_power80_by_f"] = {str(f): next((c["q"] for c in out["cells"] if c["f"] == f and c["power"] >= 0.8), None)
                             for f in FS}
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(out["q_power80_by_f"])


if __name__ == "__main__":
    main()
