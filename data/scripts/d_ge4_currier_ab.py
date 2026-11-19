#!/usr/bin/env python3
"""Currier A/B split of the >=4-shared-char D excess. Precommit: logs/2026-11-18-currier-ab-ge4-selfreview.md
Usage: python3 -I data/scripts/d_ge4_currier_ab.py"""
import hashlib, json, re, sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
import repeated_initial_run_null as base
import d_prefix_sensitivity as dps
dps.REPS = 2000
OUT = REPO / "data" / "derived" / "d-ge4-currier-ab.json"
SEED = 20261122
HDR = re.compile(r"^<(f[^.,>]+)>\s+<!(.*)>")
def lang_map():
    m = {}
    for line in (REPO / "data" / "ZL3b-n.txt").read_text(encoding="utf-8", errors="replace").splitlines():
        h = HDR.match(line)
        if h:
            l = re.search(r"\$L=(\w)", h.group(2)); m[h.group(1)] = l.group(1) if l else "?"
    return m
def main():
    dps.verify_inputs()  # hash all inputs before any computation (logs/2026-11-19-hash-hoist-selfreview.md)
    lm = lang_map()
    out = {"precommit": "logs/2026-11-18-currier-ab-ge4-selfreview.md", "seed": SEED, "reps": 2000, "inputs": {}, "meta": {"lang_tag_counts_pages": {k: sum(1 for v in lm.values() if v == k) for k in sorted(set(lm.values()))}}, "cells": {}}
    ss = np.random.SeedSequence(SEED).spawn(8); i = 0
    for t, path in base.SOURCES.items():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()  # fail-closed pin (logs/2026-11-18-input-hash-guard-selfreview.md)
        if dps.EXPECTED_SHA256.get(t) != actual:
            raise SystemExit(f"{t} input SHA-256 mismatch: expected {dps.EXPECTED_SHA256.get(t)}, got {actual}")
        out["inputs"][t] = actual
        rows = base.parse(path)
        out["meta"][t] = {"rows": len(rows), "rows_dropped_no_AB": sum(1 for r in rows if lm.get(r[0], "?") not in "AB")}
        for lang in "AB":
            hr = [r for r in rows if lm.get(r[0], "?") == lang]
            for seg in ("eva", "atomic"):
                res, tot, _ = dps.cell(hr, seg, np.random.default_rng(ss[i])); i += 1
                c = res["char"]; ge4 = c[">=4"]; k = f"{t}|{seg}|{lang}"
                out["cells"][k] = {"n_rows": len(hr), "n_pages": len({r[0] for r in hr}), "obs_D_total": tot["char"], "ge4": ge4,
                    "bins": {b: round(c[b]["ratio"], 3) for b in ("L1", "L2", "L3", "L4+")},
                    "replicated": bool(ge4["ratio"] >= 1.20 and ge4["p"] <= 0.0125), "underpowered": ge4["obs"] < 200}
                print(k, len(hr), ge4["obs"], round(ge4["ratio"], 3), round(ge4["z"], 1), ge4["p"], out["cells"][k]["replicated"], flush=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
if __name__ == "__main__":
    main()
