#!/usr/bin/env python3
"""Lemma-column sensitivity of the adjacent edit-distance profile on the seven pinned UD controls.

Precommit: logs/2026-11-22-ge4-levenshtein-lemma-sensitivity-selfreview.md (pushed before this file existed).
Usage: python3 -I data/scripts/ge4_levenshtein_lemma_sensitivity.py [cache_dir]   (needs rapidfuzz; corpora never committed)
"""
import json, sys, tempfile
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ge4_natural_language_control as g4
import ge4_levenshtein_profile as lev

OUT = HERE.parent / "derived" / "ge4-levenshtein-lemma-sensitivity.json"
SEED, TOL, FALLBACK_MAX = 20261125, 0.10, 0.20
STATS = {"fallback": 0, "words": 0}


def pick(cols):
    """lemma (col 3), falling back to surface form (col 2) when missing/empty after letters()."""
    STATS["words"] += 1
    w = g4.letters(cols[2]) if cols[2] not in ("_", "") else ""
    if not w:
        STATS["fallback"] += 1
        w = g4.letters(cols[1])
    return w


def sentences_lemma(paths, use_newdoc):
    doc = None
    for fi, p in enumerate(paths):
        if not use_newdoc:
            doc = f"file{fi}"
        words, skip_to = [], 0
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.startswith("# newdoc") and use_newdoc:
                doc = line.split("=", 1)[1].strip() if "=" in line else line
                continue
            if line.startswith("#"):
                continue
            if not line.strip():
                if words:
                    yield doc, words
                words, skip_to = [], 0
                continue
            cols = line.split("\t")
            tid = cols[0]
            if "." in tid:
                continue
            if "-" in tid:
                skip_to = int(tid.split("-")[1])
                w = g4.letters(cols[1])   # MWT header: surface only; components counted below are skipped
                continue_mwt = True
                if w:
                    words.append(w)
                continue
            if int(tid) <= skip_to or cols[3] in g4.EXCLUDED_UPOS:
                continue
            w = pick(cols)
            if w:
                words.append(w)
        if words:
            yield doc, words


def main():
    cache = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix="ge4-ud-"))
    ref = json.loads((HERE.parent / "derived" / "ge4-levenshtein-profile.json").read_text())["streams"]["voynich_ZL3b_eva"]
    surf = json.loads((HERE.parent / "derived" / "ge4-levenshtein-nl-panel.json").read_text())["corpora"]
    g4ref = json.loads((HERE.parent / "derived" / "ge4-natural-language-control.json").read_text())
    T, m = g4ref["voynich_tokens_T"], g4ref["mean_paragraph_len_m"]
    seqs = iter(np.random.SeedSequence(SEED).spawn(16))
    out = {"precommit": "logs/2026-11-22-ge4-levenshtein-lemma-sensitivity-selfreview.md", "seed": SEED, "reps": lev.REPS,
           "T": T, "m": m, "voynich_ref_d1": ref["d1"]["ratio"], "corpora": {}}
    g4.sentences = sentences_lemma   # blocks_nl resolves `sentences` at call time in g4's namespace
    for c in g4.corpora():
        rng = np.random.default_rng(next(seqs))
        paths = [g4.fetch(c, n, s, cache) for n, s in c["files"]]
        STATS["fallback"] = STATS["words"] = 0
        bl, _ = g4.blocks_nl(paths, c["use_newdoc"], T, m)
        r = lev.profile(bl, [[False] * len(b) for b in bl], rng)
        r["blocks"] = len(bl)
        r["lemma_fallback"] = STATS["fallback"]; r["lemma_words_read"] = STATS["words"]
        r["fallback_rate"] = STATS["fallback"] / max(STATS["words"], 1)
        r["surface_tokens"] = surf[c["key"]]["tokens"]
        r["d1_surface"] = surf[c["key"]]["d1"]["ratio"]
        r["d1_change"] = r["d1"]["ratio"] - r["d1_surface"]
        r["excluded"] = r["fallback_rate"] > FALLBACK_MAX
        out["corpora"][c["key"]] = r
        print(c["key"], r["tokens"], "fb=%.3f" % r["fallback_rate"], {b: round(r[b]["ratio"], 3) for b in lev.BINS},
              "d1 surf->lemma %.3f->%.3f" % (r["d1_surface"], r["d1"]["ratio"]), flush=True)
    inc = {k: v for k, v in out["corpora"].items() if not v["excluded"]}
    tr = inc.get("turkish_imst")
    others = [v["d1_change"] for k, v in inc.items() if k != "turkish_imst"]
    explained = bool(tr and tr["d1"]["ratio"] < 1.30 and (not others or -tr["d1_change"] > max(-x for x in others)))
    rs = [v["d1"]["ratio"] for v in inc.values()]
    out["verdict"] = {"n_included": len(inc), "turkish_lemma_explained": explained,
                      "turkish_lemma_r1": tr["d1"]["ratio"] if tr else None,
                      "d1_band_lemma": [min(rs) - TOL, max(rs) + TOL],
                      "voynich_d1_in_lemma_band": min(rs) - TOL <= ref["d1"]["ratio"] <= max(rs) + TOL}
    print(json.dumps(out["verdict"], indent=1))
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
