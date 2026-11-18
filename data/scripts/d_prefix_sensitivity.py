#!/usr/bin/env python3
"""POST-HOC sensitivity of the D prefix split: bin distinct adjacent same-initial pairs by common-prefix length
(chars and segmentation units; bins L=1, L=2, L=3, L>=4) under the N5 within-paragraph shuffle.
Precommit: logs/2026-11-18-d-prefix-sensitivity-selfreview.md. Usage: python3 -I data/scripts/d_prefix_sensitivity.py
"""
import hashlib, json, sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
import repeated_initial_run_null as base

OUT = REPO / "data" / "derived" / "d-prefix-sensitivity.json"
REPS, SEED = 2000, 20261120
BINS = ("L1", "L2", "L3", "L4+")
OBS_D_1117 = {"ZL3b|eva": 5388, "ZL3b|atomic": 4863, "RF1b-er|eva": 5414, "RF1b-er|atomic": 4823}
OBS_D3_1118 = {"ZL3b|eva": 1225, "ZL3b|atomic": 1225, "RF1b-er|eva": 1216, "RF1b-er|atomic": 1216}

def units(w, rx):
    out, i = [], 0
    while i < len(w):
        m = rx.match(w, i); out.append(m.group(0)); i = m.end()
    return out

def lcp(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y: break
        n += 1
    return n

def cell(rows, seg, rng):
    rx = base.UNIT_EVA if seg == "eva" else base.UNIT_ATOMIC
    inits, scope, _ = base.build(rows, seg, "paragraph")
    words = [w for _, _, _, ws in rows for w in ws]
    assert len(words) == len(inits)
    ok = np.array(["?" not in w for w in words])
    vocab = {}
    wc = np.array([vocab.setdefault(w, len(vocab)) if o else -(i + 1) for i, (w, o) in enumerate(zip(words, ok))])
    iv = {}
    ic = np.array([iv.setdefault(k, len(iv)) if k is not None else -(i + 1) for i, k in enumerate(inits)])
    vw = list(vocab)
    vu = [tuple(units(w, rx)) for w in vw]
    # lookup of bin per (vocab a, vocab b) computed lazily via cache
    cache = {"char": {}, "unit": {}}
    def binof(metric, a, b):
        key = (a, b) if a < b else (b, a)
        c = cache[metric]
        if key not in c:
            L = lcp(vw[a], vw[b]) if metric == "char" else lcp(vu[a], vu[b])
            c[key] = min(L, 4) - 1  # 0..3
        return c[key]
    same = scope[1:] == scope[:-1]
    def count(W, I):
        out = {m: np.zeros((W.shape[0], 4), dtype=np.int64) for m in ("char", "unit")}
        d = (I[:, 1:] == I[:, :-1]) & (W[:, 1:] != W[:, :-1]) & same[None, :] & (W[:, 1:] >= 0) & (W[:, :-1] >= 0)
        rr, cc = np.nonzero(d)
        A, B = W[rr, cc], W[rr, cc + 1]
        for m in out:
            bins = np.fromiter((binof(m, int(a), int(b)) for a, b in zip(A, B)), dtype=np.int64, count=len(A))
            np.add.at(out[m], (rr, bins), 1)
        return out
    obs = {m: v[0] for m, v in count(wc[None, :], ic[None, :]).items()}
    grp = [g for g in (np.flatnonzero(scope == s) for s in np.unique(scope)) if g.size > 1]
    nulls = {"char": [], "unit": []}
    for start in range(0, REPS, 100):
        R = min(100, REPS - start)
        w2, i2 = np.tile(wc, (R, 1)), np.tile(ic, (R, 1))
        for g in grp:
            k = rng.random((R, g.size)).argsort(axis=1)
            w2[:, g] = wc[g][k]; i2[:, g] = ic[g][k]
        for m, v in count(w2, i2).items(): nulls[m].append(v)
    res = {}
    for m in ("char", "unit"):
        N = np.concatenate(nulls[m]); o = obs[m]
        r = {}
        for j, b in enumerate(BINS):
            a = N[:, j]
            r[b] = {"obs": int(o[j]), "null_mean": float(a.mean()), "null_sd": float(a.std()),
                    "ratio": float(o[j] / a.mean()), "z": float((o[j] - a.mean()) / a.std()),
                    "p": (1 + int((a >= o[j]).sum())) / (REPS + 1)}
        for k in (2, 3, 4):
            a = N[:, k - 1:].sum(axis=1); ov = int(o[k - 1:].sum())
            r[f">={k}"] = {"obs": ov, "null_mean": float(a.mean()), "ratio": float(ov / a.mean()),
                           "z": float((ov - a.mean()) / a.std()), "p": (1 + int((a >= ov).sum())) / (REPS + 1)}
        res[m] = r
    return res, {m: int(obs[m].sum()) for m in obs}, int(obs["char"][2:].sum())

def main():
    out = {"label": "POST-HOC sensitivity", "precommit": "logs/2026-11-18-d-prefix-sensitivity-selfreview.md",
           "reps": REPS, "seed": SEED, "inputs": {}, "checks": {}, "cells": {}}
    ch = iter(np.random.SeedSequence(SEED).spawn(4))
    for t, path in base.SOURCES.items():
        out["inputs"][t] = hashlib.sha256(path.read_bytes()).hexdigest()
        rows = base.parse(path)
        for seg in ("eva", "atomic"):
            k = f"{t}|{seg}"
            res, tot, d3 = cell(rows, seg, np.random.default_rng(next(ch)))
            out["checks"][k] = {"sum_bins_char": tot["char"], "sum_bins_unit": tot["unit"], "obs_D_1117": OBS_D_1117[k],
                                "obs_char_ge3": d3, "obs_D3_1118": OBS_D3_1118[k]}
            out["cells"][k] = res
            print(k, json.dumps(out["checks"][k]), {m: {b: round(v["ratio"], 3) for b, v in res[m].items()} for m in res}, flush=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
