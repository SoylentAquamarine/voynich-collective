#!/usr/bin/env python3
"""Decompose S2 (adjacent same-initial pairs) into exact-repeat (E) and distinct-word (D) parts under N5.
Precommit: logs/2026-11-17-s2-adjacency-decomposition-selfreview.md. Usage: python3 -I data/scripts/s2_adjacency_decomposition.py
"""
import hashlib, json, sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
import repeated_initial_run_null as base

OUT = REPO / "data" / "derived" / "s2-adjacency-decomposition.json"
REPS, SEED = 2000, 20261118

def stats(wc, ic, scope):
    same_scope = (scope[1:] == scope[:-1])[None, :]
    si = (ic[:, 1:] == ic[:, :-1]) & same_scope
    e = (wc[:, 1:] == wc[:, :-1]) & same_scope
    return e.sum(axis=1), (si & ~e).sum(axis=1)

def cell(rows, seg, rng):
    inits, scope, _ = base.build(rows, seg, "paragraph")
    words = [w for _, _, _, ws in rows for w in ws]
    assert len(words) == len(inits)
    def code(keys):
        v = {}
        return np.array([v.setdefault(k, len(v)) if k is not None else -(i + 1) for i, k in enumerate(keys)])
    ic = code(inits)
    wc = code([None if "?" in w else w for w in words])
    oe, od = (int(x[0]) for x in stats(wc[None, :], ic[None, :], scope))
    grp = [np.flatnonzero(scope == s) for s in np.unique(scope)]
    grp = [g for g in grp if g.size > 1]
    E, D = [], []
    for start in range(0, REPS, 200):
        R = min(200, REPS - start)
        w2, i2 = np.tile(wc, (R, 1)), np.tile(ic, (R, 1))
        for g in grp:
            k = rng.random((R, g.size)).argsort(axis=1)
            w2[:, g] = wc[g][k]; i2[:, g] = ic[g][k]
        e, d = stats(w2, i2, scope); E.append(e); D.append(d)
    E, D = np.concatenate(E), np.concatenate(D)
    r = {"words": len(wc), "obs_E": oe, "obs_D": od}
    for n, o, a in (("E", oe, E), ("D", od, D)):
        r[n] = {"null_mean": float(a.mean()), "null_sd": float(a.std()), "excess": float(o - a.mean()),
                "ratio": float(o / a.mean()) if a.mean() else None,
                "z": float((o - a.mean()) / a.std()) if a.std() else None,
                "p": (1 + int((a >= o).sum())) / (REPS + 1)}
    tot = r["E"]["excess"] + r["D"]["excess"]
    r["E_share_of_S2_excess"] = r["E"]["excess"] / tot if tot else None
    return r

def main():
    out = {"precommit": "logs/2026-11-17-s2-adjacency-decomposition-selfreview.md", "reps": REPS, "seed": SEED,
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
