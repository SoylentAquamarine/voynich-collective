#!/usr/bin/env python3
"""Family C (1-3 chained mutations per copy) 20-seed panel. Precommit: logs/2026-11-25-ge4-famC-multistep-selfreview.md (94b2fe8)."""
import hashlib, json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import repeated_initial_run_null as base
import ge4_natural_language_control as g4
import ge4_levenshtein_profile as lp
import ge4_levenshtein_atomic_glyph as ag


def famC_blocks(lens, p, rng, vocab, pw, chars, pc):
    def mutate(w, rng):  # verbatim from lp.famB_blocks
        while True:
            op = rng.integers(3); i = rng.integers(len(w) + (op == 1))
            c = rng.choice(chars, p=pc)
            if op == 0: v = w[:i] + c + w[i+1:]
            elif op == 1: v = w[:i] + c + w[i:]
            else: v = w[:i] + w[i+1:]
            if v and v != w: return v
    blocks = []
    for L in lens:
        b = [str(rng.choice(vocab, p=pw))]
        for _ in range(L - 1):
            if rng.random() < p:
                w = b[-1]
                for _ in range(int(rng.integers(1, 4))): w = mutate(w, rng)
                b.append(w)
            else:
                b.append(str(rng.choice(vocab, p=pw)))
        blocks.append(b)
    return blocks

OUT = HERE.parent / "derived" / "ge4-famC-seed-panel.json"
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
ps = [0.005, 0.01, 0.02]
seqs = np.random.SeedSequence(20261126).spawn(len(ps) * 20 * 2)
k = 0; out = {"reps": REPS, "voynich_ext_rescored": {b: vp[b]["ratio"] for b in lp.BINS}, "voynich_committed": V_D, "panel": {}}
for p in ps:
    r = {b: [] for b in ("d1", "d2", "d3")}
    for i in range(20):
        rng = np.random.default_rng(seqs[k]); nr = np.random.default_rng(seqs[k + 1]); k += 2
        bl = famC_blocks(lens, p, rng, vocabB, pwB, charsB, pcB)
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
