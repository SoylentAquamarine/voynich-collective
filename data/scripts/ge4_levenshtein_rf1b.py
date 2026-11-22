#!/usr/bin/env python3
"""Transcription robustness of the adjacent edit-distance profile: ZL3b-EVA (control rerun) vs RF1b-er.

Precommit: logs/2026-11-22-ge4-levenshtein-rf1b-transcription-selfreview.md (pushed 580061b before this file existed).
profile() is imported unchanged from ge4_levenshtein_profile; blocks are built exactly as in its main().
Usage: python3 data/scripts/ge4_levenshtein_rf1b.py  (needs rapidfuzz)
"""
import hashlib, json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import repeated_initial_run_null as base
import ge4_levenshtein_profile as lp

OUT = HERE.parent / "derived" / "ge4-levenshtein-rf1b.json"
SHA = {"ZL3b": "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
       "RF1b-er": "eb857a1f353b18983fbc25b954e1bbce227a26d99cefabfda9206ff9b57644d2"}
RF_SEED, TOL = 20261122, 0.10


def blocks(src):
    rows = base.parse(base.SOURCES[src])
    _, scope, _ = base.build(rows, "eva", "paragraph")
    words = [w for _, _, _, ws in rows for w in ws]
    vb, vbad = [], []
    for s in np.unique(scope):
        idx = np.flatnonzero(scope == s)
        vb.append([words[i] for i in idx]); vbad.append(["?" in words[i] for i in idx])
    return vb, vbad


def main():
    for t, h in SHA.items():  # fail closed before any computation
        if hashlib.sha256(base.SOURCES[t].read_bytes()).hexdigest() != h:
            raise SystemExit(f"{t} SHA-256 mismatch")
    committed = json.loads((HERE.parent / "derived" / "ge4-levenshtein-profile.json").read_text())["streams"]["voynich_ZL3b_eva"]
    zl_rng = np.random.default_rng(next(iter(np.random.SeedSequence(lp.SEED).spawn(64))))
    zl = lp.profile(*blocks("ZL3b"), zl_rng)
    control = all(zl[b]["obs"] == committed[b]["obs"] and abs(zl[b]["ratio"] - committed[b]["ratio"]) < 1e-12 for b in lp.BINS)
    print("ZL3b control reproduces:", control, flush=True)
    if not control:
        raise SystemExit("ZL3b control did not reproduce; stopping per precommit")
    rf = lp.profile(*blocks("RF1b-er"), np.random.default_rng(RF_SEED))
    checks = {b: {"zl3b": zl[b]["ratio"], "rf1b": rf[b]["ratio"], "diff": rf[b]["ratio"] - zl[b]["ratio"],
                  "within_tol": abs(rf[b]["ratio"] - zl[b]["ratio"]) <= TOL} for b in ("d1", "d2", "d3")}
    robust = all(c["within_tol"] for c in checks.values()) and rf["d1"]["p_upper"] <= 0.01
    out = {"precommit": "logs/2026-11-22-ge4-levenshtein-rf1b-transcription-selfreview.md", "reps": lp.REPS,
           "zl3b_seed": f"SeedSequence({lp.SEED}).spawn(64)[0]", "rf1b_seed": RF_SEED, "tol": TOL,
           "rule": "robust iff |rf-zl| <= 0.10 for d1,d2,d3 and RF1b-er d1 p_upper <= .01",
           "zl3b_control_reproduces": control, "streams": {"voynich_ZL3b_eva": zl, "voynich_RF1b_er_eva": rf},
           "checks": checks, "verdict": "transcription-robust" if robust else "transcription-sensitive",
           "P1_robust": robust, "P2_rf_d1_in_1.20_1.42": 1.20 <= rf["d1"]["ratio"] <= 1.42,
           "P3_rf_d0_gt_1": rf["d0_identical"]["ratio"] > 1.0}
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    for name, s in out["streams"].items():
        print(name, {b: (s[b]["obs"], round(s[b]["ratio"], 3), round(s[b]["p_upper"], 4)) for b in lp.BINS}, s["pairs"], s["tokens"])
    print("verdict:", out["verdict"], "P2:", out["P2_rf_d1_in_1.20_1.42"], "P3:", out["P3_rf_d0_gt_1"])


if __name__ == "__main__":
    main()
