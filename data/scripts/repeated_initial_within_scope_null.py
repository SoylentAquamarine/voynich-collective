#!/usr/bin/env python3
"""Within-page (N4) and within-paragraph (N5) shuffle nulls for long same-initial runs.

Precommit: logs/2026-11-17-initial-run-within-scope-shuffle-selfreview.md (pushed 297bf66 before this code).
Parse/segmentation/paragraph scope imported unchanged from repeated_initial_run_null.py.
S1 = maximal runs >= 8 within paragraph; S2 = adjacent same-initial pairs within paragraph.
Usage: python3 -I data/scripts/repeated_initial_within_scope_null.py
"""
import hashlib, json, sys
from pathlib import Path
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
import repeated_initial_run_null as base  # reused unchanged

OUT = REPO / "data" / "derived" / "repeated-initial-within-scope-null.json"
REPS, SEED = 2000, 20261117


def build_with_pages(rows, seg):
    inits, scope, secs = base.build(rows, seg, "paragraph")
    pages = []
    for page, sec, tchar, words in rows:
        pages.extend([page] * len(words))
    assert len(pages) == len(inits)
    return inits, scope, np.array(pages)


def s2(codes, scope):
    return ((codes[:, 1:] == codes[:, :-1]) & (scope[1:] == scope[:-1])[None, :]).sum(axis=1)


def cell(rows, seg, rng):
    inits, scope, pages = build_with_pages(rows, seg)
    vocab = sorted({x for x in inits if x is not None})
    idx = {u: i for i, u in enumerate(vocab)}
    codes = np.array([idx[x] if x is not None else -(i + 1) for i, x in enumerate(inits)])
    obs1 = int(base.runs_ge(codes[None, :], scope)[0][0])
    obs2 = int(s2(codes[None, :], scope)[0])
    groups = {"N4_within_page": [np.flatnonzero(pages == p) for p in np.unique(pages)],
              "N5_within_paragraph": [np.flatnonzero(scope == s) for s in np.unique(scope)]}
    res = {"words": len(codes), "paragraphs": int(len(np.unique(scope))),
           "observed_S1_runs_ge8": obs1, "observed_S2_adjacent_same": obs2, "nulls": {}}
    for name, grp in groups.items():
        grp = [g for g in grp if g.size > 1]
        st1, st2 = [], []
        for start in range(0, REPS, 200):
            R = min(200, REPS - start)
            sim = np.tile(codes, (R, 1))
            for g in grp:
                keys = rng.random((R, g.size)).argsort(axis=1)
                sim[:, g] = codes[g][keys]
            st1.append(base.runs_ge(sim, scope)[0]); st2.append(s2(sim, scope))
        st1, st2 = np.concatenate(st1), np.concatenate(st2)
        res["nulls"][name] = {
            "S1_mean": float(st1.mean()), "S1_q95": float(np.quantile(st1, .95)),
            "S1_p": (1 + int((st1 >= obs1).sum())) / (REPS + 1),
            "S2_mean": float(st2.mean()), "S2_sd": float(st2.std()),
            "S2_p": (1 + int((st2 >= obs2).sum())) / (REPS + 1)}
    return res


def main():
    out = {"precommit": "logs/2026-11-17-initial-run-within-scope-shuffle-selfreview.md",
           "reps": REPS, "seed": SEED, "bonferroni_alpha": 0.05 / 8,
           "primary": "ZL3b|eva|paragraph|N5_within_paragraph|S1", "inputs": {}, "cells": {}}
    ch = iter(np.random.SeedSequence(SEED).spawn(4))
    for t, path in base.SOURCES.items():
        out["inputs"][t] = hashlib.sha256(path.read_bytes()).hexdigest()
        rows = base.parse(path)
        for seg in ("eva", "atomic"):
            k = f"{t}|{seg}|paragraph"
            out["cells"][k] = c = cell(rows, seg, np.random.default_rng(next(ch)))
            print(k, c["observed_S1_runs_ge8"], c["observed_S2_adjacent_same"],
                  json.dumps(c["nulls"]), flush=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
