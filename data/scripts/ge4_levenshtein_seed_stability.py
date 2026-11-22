#!/usr/bin/env python3
"""Monte Carlo seed stability of the adjacent edit-distance profile (ZL3b-EVA and RF1b-er).

Precommit: logs/2026-11-22-ge4-levenshtein-seed-stability-selfreview.md (pushed e8de62a before this file existed).
profile() and blocks() are imported unchanged. Fresh master seed 20261127; children 0-4 -> ZL3b, 5-9 -> RF1b-er.
Usage: python3 data/scripts/ge4_levenshtein_seed_stability.py  (needs rapidfuzz)
"""
import hashlib, json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import repeated_initial_run_null as base
import ge4_levenshtein_profile as lp
import ge4_levenshtein_rf1b as rf1b

OUT = HERE.parent / "derived" / "ge4-levenshtein-seed-stability.json"
MASTER, K, RANGE_TOL = 20261127, 5, 0.02
KEYS = ("d1", "d2", "d3")


def main():
    for t, h in rf1b.SHA.items():
        if hashlib.sha256(base.SOURCES[t].read_bytes()).hexdigest() != h:
            raise SystemExit(f"{t} SHA-256 mismatch")
    committed = json.loads(rf1b.OUT.read_text())["streams"]
    ref = {"ZL3b": committed["voynich_ZL3b_eva"], "RF1b-er": committed["voynich_RF1b_er_eva"]}
    kids = np.random.SeedSequence(MASTER).spawn(2 * K)
    runs = {"ZL3b": [], "RF1b-er": []}
    for i, src in enumerate(("ZL3b", "RF1b-er")):
        b = rf1b.blocks(src)
        for k in range(K):
            r = lp.profile(*b, np.random.default_rng(kids[i * K + k]))
            if any(r[x]["obs"] != ref[src][x]["obs"] for x in lp.BINS):
                raise SystemExit(f"{src} seed {k}: observed counts differ from committed; stopping per precommit")
            runs[src].append(r)
            print(src, k, {x: round(r[x]["ratio"], 4) for x in lp.BINS}, "d1 p", round(r["d1"]["p_upper"], 4), flush=True)
    spread = {src: {x: {"min": min(r[x]["ratio"] for r in rs), "max": max(r[x]["ratio"] for r in rs),
                        "range": max(r[x]["ratio"] for r in rs) - min(r[x]["ratio"] for r in rs),
                        "committed": ref[src][x]["ratio"]} for x in lp.BINS} for src, rs in runs.items()}
    pairs = []
    for k in range(K):
        z, f = runs["ZL3b"][k], runs["RF1b-er"][k]
        diffs = {x: f[x]["ratio"] - z[x]["ratio"] for x in KEYS}
        ok = all(abs(d) <= rf1b.TOL for d in diffs.values()) and f["d1"]["p_upper"] <= 0.01
        pairs.append({"k": k, "diffs": diffs, "rf_d1_p_upper": f["d1"]["p_upper"], "rf1b_rule_holds": ok})
    a = all(spread[s][x]["range"] <= RANGE_TOL for s in spread for x in KEYS)
    b = all(p["rf1b_rule_holds"] for p in pairs)
    out = {"precommit": "logs/2026-11-22-ge4-levenshtein-seed-stability-selfreview.md", "master_seed": MASTER,
           "seeds_per_transcription": K, "reps": lp.REPS, "range_tol": RANGE_TOL,
           "rule": "MC-stable iff ratio range <= 0.02 for d1-d3 in both transcriptions and all 5 seed pairs satisfy the frozen RF1b rule",
           "obs_control_matches_committed": True,
           "runs": {s: [{x: {k2: r[x][k2] for k2 in ("obs", "null_mean", "ratio", "p_upper")} for x in lp.BINS} for r in rs]
                    for s, rs in runs.items()},
           "spread": spread, "pairs": pairs, "a_ranges_ok": a, "b_pairs_ok": b,
           "verdict": "MC-stable" if a and b else "MC-sensitive",
           "P1_mc_stable": a and b,
           "P2_all_ranges_le_0.01": all(spread[s][x]["range"] <= 0.01 for s in spread for x in KEYS),
           "P3_d1_p_min_every_seed": all(abs(r["d1"]["p_upper"] - 1 / (lp.REPS + 1)) < 1e-12 for rs in runs.values() for r in rs)}
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({s: {x: round(v["range"], 4) for x, v in d.items()} for s, d in spread.items()}))
    print("verdict:", out["verdict"], "P2:", out["P2_all_ranges_le_0.01"], "P3:", out["P3_d1_p_min_every_seed"])


if __name__ == "__main__":
    main()
