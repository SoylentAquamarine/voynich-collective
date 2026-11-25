#!/usr/bin/env python3
"""Family E (non-copy shared-affix-class neighbour) 20-seed panel.
Precommit: logs/2026-11-25-ge4-famE-affixclass-selfreview.md. Generated from ge4_famC_seed_panel.py; only generator, seed and output changed."""
import hashlib, json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import repeated_initial_run_null as base
import ge4_natural_language_control as g4
import ge4_levenshtein_profile as lp
import ge4_levenshtein_atomic_glyph as ag


def famD_blocks(lens, p, rng, vocab, pw, chars, pc):
    # family E: with prob p, next word drawn (freq-weighted) from vocab words sharing first-2 or last-2 chars with predecessor
    blocks = []
    for L in lens:
        b = [str(rng.choice(vocab, p=pw))]
        for _ in range(L - 1):
            w = None
            if rng.random() < p:
                prev = b[-1]
                use_pre = rng.random() < 0.5
                key = prev[:2] if use_pre else prev[-2:]
                m = AFF_PRE.get(key) if use_pre else AFF_SUF.get(key)
                if m is not None:
                    idx = m
                    cand = vocab[idx]; ww = pw[idx] * (cand != prev)
                    if ww.sum() > 0: w = str(rng.choice(cand, p=ww / ww.sum()))
            if w is None: w = str(rng.choice(vocab, p=pw))
            b.append(w)
        blocks.append(b)
    return blocks

OUT = HERE.parent / "derived" / "ge4-famE-affix-seed-panel.json"
REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 100
lp.REPS = REPS
V_D = {"d1": 1.268, "d2": 1.090, "d3": 1.084}
assert hashlib.sha256(base.SOURCES["ZL3b"].read_bytes()).hexdigest() == g4.ZL3B_SHA
rows = base.parse(base.SOURCES["ZL3b"])
_, scope, _ = base.build(rows, "eva", "paragraph")
words = [w for _, _, _, ws in rows for w in ws]
vb, vbad = [], []
for s in np.unique(scope):
    idx = np.flatnonzero(scope == s)
    vb.append([words[i] for i in idx]); vbad.append(["?" in words[i] for i in idx])
lens = [len(b) for b in vb]
recX = ag.recoder(ag.EXTENDED)
vp = lp.profile(ag.recode_blocks(vb, recX), vbad, np.random.default_rng(1))
print("control Voynich ext", {b: round(vp[b]["ratio"], 4) for b in lp.BINS}, flush=True)
poolB = [w for w in words if "?" not in w and "{" not in w]
vocabB, cnt = np.unique(poolB, return_counts=True); pwB = cnt / cnt.sum()
charsB, ccB = np.unique(list("".join(poolB)), return_counts=True); pcB = ccB / ccB.sum()
AFF_PRE = {}; AFF_SUF = {}
for _i, _w in enumerate(vocabB):
    AFF_PRE.setdefault(_w[:2], []).append(_i); AFF_SUF.setdefault(_w[-2:], []).append(_i)
AFF_PRE = {k: np.array(v) for k, v in AFF_PRE.items()}; AFF_SUF = {k: np.array(v) for k, v in AFF_SUF.items()}
ps = [0.005, 0.01, 0.02]
seqs = np.random.SeedSequence(20261128).spawn(len(ps) * 20 * 2)
k = 0; out = {"reps": REPS, "voynich_ext_rescored": {b: vp[b]["ratio"] for b in lp.BINS}, "voynich_committed": V_D, "panel": {}}
for p in ps:
    r = {b: [] for b in ("d1", "d2", "d3")}
    for i in range(20):
        rng = np.random.default_rng(seqs[k]); nr = np.random.default_rng(seqs[k + 1]); k += 2
        bl = famD_blocks(lens, p, rng, vocabB, pwB, charsB, pcB)
        pr = lp.profile(ag.recode_blocks(bl, recX), [[False] * len(b) for b in bl], nr)
        for b in r: r[b].append(pr[b]["ratio"])
    s = {}
    for b, v in r.items():
        a = np.array(v); t = V_D[b]
        s[b] = {"values": v, "mean": a.mean(), "sd": a.std(ddof=1), "min": a.min(), "max": a.max(),
                "frac_within_0.10": float((abs(a - t) <= 0.10).mean()), "voynich_in_band": bool(a.min() - .1 <= t <= a.max() + .1)}
    f = s["d1"]["frac_within_0.10"]
    s["reading"] = "not distinguishable" if (f >= .25 and s["d1"]["voynich_in_band"]) else "distinguishable" if f < .10 else "ambiguous"
    out["panel"][str(p)] = s
    print(p, {b: (round(s[b]["mean"], 3), round(s[b]["sd"], 3), s[b]["frac_within_0.10"], s[b]["voynich_in_band"]) for b in ("d1", "d2", "d3")}, s["reading"], flush=True)
OUT.write_text(json.dumps(out, indent=1) + "\n")
