#!/usr/bin/env python3
"""Repeated-initial run null (follow-up to steering #72 / PR #116 Turenne audit item 3).

Precommit: logs/2026-11-14-initial-glyph-iid-null-selfreview.md (redesign section).

Event: maximal run of >= 8 consecutive words sharing the same initial unit, within a
scope (line or paragraph). Words containing '?' break runs. Paragraph-text loci only.

Cells: {ZL3b, RF1b-er} x {EVA char, atomic glyph} x {line, paragraph}.
Nulls: N0 uniform-K analytic (reference), N1 global iid initials, N2 section iid
initials, N3 within-section word shuffle. 2,000 replicates each, seed 20261114.

Usage: python3 -I data/scripts/repeated_initial_run_null.py
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
import normalize_eva as ne  # committed normalization policy, reused unchanged

SOURCES = {"ZL3b": REPO / "data" / "ZL3b-n.txt", "RF1b-er": REPO / "data" / "RF1b-er.txt"}
OUT = REPO / "data" / "derived" / "repeated-initial-run-null.json"
REPS = 2000
SEED = 20261114
RUN_MIN = 8
PAGE_HDR = re.compile(r"^<(f[^.,>]+)>\s+<!(.*)>")
UNIT_EVA = re.compile(r"@\d+;|\{[^}]*\}|.")
UNIT_ATOMIC = re.compile(r"@\d+;|\{[^}]*\}|ckh|cth|cph|cfh|ch|sh|.")


def parse(path):
    """Return list of (page, section, locus_type_char, words) for P-type loci."""
    report = {k: [] for k in ("alt_readings", "stripped_markup", "drawing_intrusions",
                              "misaligned_intrusions", "illegible_chars")}
    section = {}
    rows = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            h = PAGE_HDR.match(line)
            if h:
                m = re.search(r"\$I=(\w)", h.group(2))
                section[h.group(1)] = m.group(1) if m else "?"
                continue
            p = ne.strip_locus_tag(line)
            if p is None:
                continue
            locus, text = p
            page, rest = locus.split(".", 1)
            ltype = rest.split(",", 1)[1]
            if len(ltype) < 2 or ltype[1] != "P":
                continue
            text = ne.resolve_alt_readings(text, locus, report)
            text = ne.handle_drawing_intrusion(text, locus, report)
            text = ne.handle_illegible(text, locus, report)
            text = ne.strip_markup(text, locus, report)
            words = ne.tokenize(text.replace(" ", "."))
            rows.append((page, section.get(page, "?"), ltype[0], words))
    return rows


def build(rows, seg, scope):
    unit = UNIT_EVA if seg == "eva" else UNIT_ATOMIC
    inits, scope_id, sec_id = [], [], []
    sid = -1
    prev_page = None
    new_after_end = False
    for page, sec, tchar, words in rows:
        if scope == "line":
            sid += 1
        else:  # paragraph
            if page != prev_page or tchar in "@*" or new_after_end:
                sid += 1
            new_after_end = tchar == "="
        if scope == "line":
            new_after_end = False
        prev_page = page
        for w in words:
            inits.append(None if "?" in w else unit.match(w).group(0))
            scope_id.append(sid)
            sec_id.append(sec)
    return inits, np.array(scope_id), sec_id


def runs_ge(codes, scope, k=RUN_MIN):
    """codes: (R, n) int array; '?' words have unique negative codes. Count maximal runs >= k."""
    same = (codes[:, 1:] == codes[:, :-1]) & (scope[1:] == scope[:-1])[None, :]
    R = same.shape[0]
    pad = np.zeros((R, 1), dtype=np.int8)
    d = np.diff(np.concatenate([pad, same.astype(np.int8), pad], axis=1), axis=1)
    out = np.zeros(R, dtype=np.int64)
    longest = np.zeros(R, dtype=np.int64)
    for r in range(R):
        starts = np.flatnonzero(d[r] == 1)
        ends = np.flatnonzero(d[r] == -1)
        lens = ends - starts + 1  # words in run
        out[r] = int((lens >= k).sum())
        longest[r] = int(lens.max()) if lens.size else 1
    return out, longest


def run_cell(rows, seg, scope, rng):
    inits, scope_arr, secs = build(rows, seg, scope)
    vocab = sorted({x for x in inits if x is not None})
    idx = {u: i for i, u in enumerate(vocab)}
    n = len(inits)
    codes = np.array([idx[x] if x is not None else -(i + 1) for i, x in enumerate(inits)])
    valid = codes >= 0
    obs, obs_long = runs_ge(codes[None, :], scope_arr)
    obs_by_k = {}
    for k in range(4, 9):
        obs_by_k[k] = int(runs_ge(codes[None, :], scope_arr, k)[0][0])
    gcount = Counter(codes[valid].tolist())
    K = len(vocab)
    p0 = np.array([gcount[i] for i in range(K)], dtype=float)
    p0 /= p0.sum()
    # windows of 8 consecutive valid-or-not words within one scope
    _, sc_counts = np.unique(scope_arr, return_counts=True)
    windows = int(np.clip(sc_counts - RUN_MIN + 1, 0, None).sum())
    n0 = windows * K * (1.0 / K) ** RUN_MIN
    n1_window = windows * float((p0 ** RUN_MIN).sum())
    sec_arr = np.array(secs)
    nulls = {}
    for name in ("N1", "N2", "N3"):
        stats = []
        for start in range(0, REPS, 200):
            R = min(200, REPS - start)
            sim = np.tile(codes, (R, 1))
            if name == "N1":
                draw = rng.choice(K, size=(R, int(valid.sum())), p=p0)
                sim[:, valid] = draw
            elif name == "N2":
                for s in np.unique(sec_arr):
                    m = (sec_arr == s) & valid
                    c = Counter(codes[m].tolist())
                    keys = np.array(sorted(c))
                    pr = np.array([c[x] for x in keys], dtype=float)
                    sim[:, m] = keys[rng.choice(len(keys), size=(R, int(m.sum())), p=pr / pr.sum())]
            else:
                for s in np.unique(sec_arr):
                    pos = np.flatnonzero(sec_arr == s)
                    for r in range(R):
                        sim[r, pos] = codes[rng.permutation(pos)]
            st, _ = runs_ge(sim, scope_arr)
            stats.append(st)
        st = np.concatenate(stats)
        nulls[name] = {
            "mean": float(st.mean()), "q95": float(np.quantile(st, 0.95)), "max": int(st.max()),
            "p_one_sided": (1 + int((st >= obs[0]).sum())) / (REPS + 1),
        }
    top = sorted(gcount.items(), key=lambda kv: -kv[1])[:8]
    return {
        "words": n, "scopes": int(len(sc_counts)), "windows_len8": windows,
        "initial_inventory_K": K,
        "top_initials": [[vocab[i], round(c / valid.sum(), 4)] for i, c in top],
        "observed_runs_ge8": int(obs[0]), "observed_longest_run": int(obs_long[0]),
        "observed_runs_ge_k": obs_by_k,
        "N0_uniform_K_expected_windows": n0,
        "N1_analytic_expected_windows": n1_window,
        "nulls": nulls,
    }


def main():
    out = {"precommit": "logs/2026-11-14-initial-glyph-iid-null-selfreview.md",
           "reps": REPS, "seed": SEED, "run_min": RUN_MIN,
           "bonferroni_alpha": 0.05 / 24,
           "primary_cell": "ZL3b|eva|paragraph|N3", "inputs": {}, "cells": {}}
    master = np.random.SeedSequence(SEED)
    children = iter(master.spawn(8))
    for tname, path in SOURCES.items():
        out["inputs"][tname] = hashlib.sha256(path.read_bytes()).hexdigest()
        rows = parse(path)
        for seg in ("eva", "atomic"):
            for scope in ("line", "paragraph"):
                rng = np.random.default_rng(next(children))
                key = f"{tname}|{seg}|{scope}"
                out["cells"][key] = run_cell(rows, seg, scope, rng)
                c = out["cells"][key]
                print(key, c["observed_runs_ge8"], c["observed_longest_run"],
                      {k: (round(v["mean"], 2), v["p_one_sided"]) for k, v in c["nulls"].items()},
                      flush=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
