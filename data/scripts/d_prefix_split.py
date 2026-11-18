#!/usr/bin/env python3
"""Decompose S2 (adjacent same-initial pairs) into exact-repeat (E) and distinct-word (D) parts under N5.
Precommit: logs/2026-11-18-d-prefix-split-selfreview.md. Usage: python3 -I data/scripts/d_prefix_split.py
"""
import hashlib, json, sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
import repeated_initial_run_null as base

OUT = REPO / "data" / "derived" / "d-prefix-split.json"
REPS, SEED = 2000, 20261119

def stats(wc, ic, pc, scope):
    same_scope = (scope[1:] == scope[:-1])[None, :]
    si = (ic[:, 1:] == ic[:, :-1]) & same_scope
    e = (wc[:, 1:] == wc[:, :-1]) & same_scope
    d = si & ~e
    d3 = d & (pc[:, 1:] == pc[:, :-1])
    return (d & ~d3).sum(axis=1), d3.sum(axis=1)

def cell(rows, seg, rng):
    inits, scope, _ = base.build(rows, seg, "paragraph")
    words = [w for _, _, _, ws in rows for w in ws]
    assert len(words) == len(inits)
    def code(keys):
        v = {}
        return np.array([v.setdefault(k, len(v)) if k is not None else -(i + 1) for i, k in enumerate(keys)])
    ic = code(inits)
    wc = code([None if "?" in w else w for w in words])
    pc = code([None if ("?" in w or len(w) < 3) else w[:3] for w in words])
    oe, od = (int(x[0]) for x in stats(wc[None, :], ic[None, :], pc[None, :], scope))
    grp = [np.flatnonzero(scope == s) for s in np.unique(scope)]
    grp = [g for g in grp if g.size > 1]
    E, D = [], []
    for start in range(0, REPS, 200):
        R = min(200, REPS - start)
        w2, i2, p2 = np.tile(wc, (R, 1)), np.tile(ic, (R, 1)), np.tile(pc, (R, 1))
        for g in grp:
            k = rng.random((R, g.size)).argsort(axis=1)
            w2[:, g] = wc[g][k]; i2[:, g] = ic[g][k]; p2[:, g] = pc[g][k]
        e, d = stats(w2, i2, p2, scope); E.append(e); D.append(d)
    E, D = np.concatenate(E), np.concatenate(D)
    r = {"words": len(wc), "obs_D1": oe, "obs_D3": od}
    for n, o, a in (("D1", oe, E), ("D3", od, D)):
        r[n] = {"null_mean": float(a.mean()), "null_sd": float(a.std()), "excess": float(o - a.mean()),
                "ratio": float(o / a.mean()) if a.mean() else None,
                "z": float((o - a.mean()) / a.std()) if a.std() else None,
                "p": (1 + int((a >= o).sum())) / (REPS + 1)}
    tot = r["D1"]["excess"] + r["D3"]["excess"]
    r["D3_share_of_D_excess"] = r["D3"]["excess"] / tot if tot else None
    return r

def main():
    out = {"precommit": "logs/2026-11-18-d-prefix-split-selfreview.md", "reps": REPS, "seed": SEED,
           "inputs": {}, "cells": {}}
    ch = iter(np.random.SeedSequence(SEED).spawn(4))
    for t, path in base.SOURCES.items():
        out["inputs"][t] = hashlib.sha256(path.read_bytes()).hexdigest()
        rows = base.parse(path)
        for seg in ("eva", "atomic"):
            k = f"{t}|{seg}|paragraph"
            out["cells"][k] = c = cell(rows, seg, np.random.default_rng(next(ch)))
            print(k, json.dumps(c), flush=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
