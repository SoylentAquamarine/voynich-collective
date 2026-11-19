#!/usr/bin/env python3
"""Partition replication of the >=4-shared-char D excess. Precommit: logs/2026-11-18-heldout-ge4-partition-selfreview.md
Usage: python3 -I data/scripts/d_ge4_partition_replication.py"""
import hashlib, json, sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
import repeated_initial_run_null as base
import d_prefix_sensitivity as dps
dps.REPS = 2000
OUT = REPO / "data" / "derived" / "d-ge4-partition-replication.json"
SEED = 20261121

def partitions(rows):
    tags = {r[1] for r in rows}
    A = [r for r in rows if r[1] == "A"]; B = [r for r in rows if r[1] == "B"]
    pages = list(dict.fromkeys(r[0] for r in rows)); h = len(pages) // 2
    first = set(pages[:h])
    return {"P1": {"A": A, "B": B}, "P2": {"early": [r for r in rows if r[0] in first], "late": [r for r in rows if r[0] not in first]}}, \
        {"tags": sorted(tags), "n_unknown_tag": sum(1 for r in rows if r[1] not in "AB"), "n_pages": len(pages)}

def main():
    dps.verify_inputs()  # hash all inputs before any computation (logs/2026-11-19-hash-hoist-selfreview.md)
    out = {"precommit": "logs/2026-11-18-heldout-ge4-partition-selfreview.md", "seed": SEED, "reps": 2000, "inputs": {}, "meta": {}, "cells": {}}
    ss = np.random.SeedSequence(SEED).spawn(16); i = 0
    for t, path in base.SOURCES.items():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()  # fail-closed pin (logs/2026-11-18-input-hash-guard-selfreview.md)
        if dps.EXPECTED_SHA256.get(t) != actual:
            raise SystemExit(f"{t} input SHA-256 mismatch: expected {dps.EXPECTED_SHA256.get(t)}, got {actual}")
        out["inputs"][t] = actual
        rows = base.parse(path)
        parts, meta = partitions(rows); out["meta"][t] = meta
        for pn, halves in parts.items():
            for hn, hr in halves.items():
                for seg in ("eva", "atomic"):
                    res, tot, _ = dps.cell(hr, seg, np.random.default_rng(ss[i])); i += 1
                    c = res["char"]
                    k = f"{t}|{seg}|{pn}|{hn}"
                    ge4 = c[">=4"]
                    out["cells"][k] = {"n_rows": len(hr), "obs_D_total": tot["char"], "ge4": ge4,
                                       "bins": {b: round(c[b]["ratio"], 3) for b in ("L1", "L2", "L3", "L4+")},
                                       "replicated": bool(ge4["ratio"] >= 1.20 and ge4["p"] <= 0.0125),
                                       "underpowered": ge4["obs"] < 200}
                    print(k, len(hr), ge4["obs"], round(ge4["ratio"], 3), round(ge4["z"], 1), ge4["p"], out["cells"][k]["replicated"], flush=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
if __name__ == "__main__":
    main()
