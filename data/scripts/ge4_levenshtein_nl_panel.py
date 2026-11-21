#!/usr/bin/env python3
"""Adjacent edit-distance profile on the seven pinned UD natural-language controls.

Precommit: logs/2026-11-21-ge4-levenshtein-nl-panel-selfreview.md (pushed 9b6c450 before this file existed).
Blocks built by ge4_natural_language_control (unchanged); statistic/null = ge4_levenshtein_profile.profile (unchanged).
Usage: python3 -I data/scripts/ge4_levenshtein_nl_panel.py [cache_dir]   (needs rapidfuzz; corpora never committed)
"""
import json, sys, tempfile
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ge4_natural_language_control as g4
import ge4_levenshtein_profile as lev

OUT = HERE.parent / "derived" / "ge4-levenshtein-nl-panel.json"
SEED, TOL = 20261125, 0.10


def main():
    cache = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix="ge4-ud-"))
    ref = json.loads((HERE.parent / "derived" / "ge4-levenshtein-profile.json").read_text())["streams"]["voynich_ZL3b_eva"]
    g4ref = json.loads((HERE.parent / "derived" / "ge4-natural-language-control.json").read_text())
    T, m = g4ref["voynich_tokens_T"], g4ref["mean_paragraph_len_m"]
    seqs = iter(np.random.SeedSequence(SEED).spawn(16))
    out = {"precommit": "logs/2026-11-21-ge4-levenshtein-nl-panel-selfreview.md", "seed": SEED, "reps": lev.REPS, "tol": TOL,
           "T": T, "m": m, "voynich_ref": {b: ref[b]["ratio"] for b in lev.BINS}, "corpora": {}}
    for c in g4.corpora():
        rng = np.random.default_rng(next(seqs))
        try:
            paths = [g4.fetch(c, n, s, cache) for n, s in c["files"]]
        except Exception as e:
            out["corpora"][c["key"]] = {"error": repr(e)}; print(c["key"], "ERROR", e, flush=True); continue
        bl, _ = g4.blocks_nl(paths, c["use_newdoc"], T, m)
        r = lev.profile(bl, [[False] * len(b) for b in bl], rng)
        r["blocks"] = len(bl)
        out["corpora"][c["key"]] = r
        print(c["key"], r["tokens"], {b: round(r[b]["ratio"], 3) for b in lev.BINS}, flush=True)
    ok = [v for v in out["corpora"].values() if "error" not in v]
    fails = []
    for b in ("d1", "d2", "d3"):
        rs = [v[b]["ratio"] for v in ok]
        lo, hi = min(rs) - TOL, max(rs) + TOL
        if not lo <= ref[b]["ratio"] <= hi:
            fails.append({"bin": b, "voynich": ref[b]["ratio"], "band": [lo, hi]})
    out["verdict"] = {"n_corpora": len(ok), "consistent": not fails, "failing_bins": fails}
    print(json.dumps(out["verdict"], indent=1))
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
