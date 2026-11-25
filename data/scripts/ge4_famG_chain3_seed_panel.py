#!/usr/bin/env python3
"""Family G (1-step p1=.02 + exactly-3-step chain at p3) 20-seed panel.
Precommit: logs/2026-11-25-ge4-famG-chain3-mix-selfreview.md. Generated from ge4_famC_seed_panel.py; only generator, seed and output changed."""
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
    # family G: prob P1 exactly 1 mutation of predecessor, prob p exactly 3 successive mutations, else unrestricted draw
    def mutate(w, rng):  # verbatim from ge4_famC_seed_panel.py
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
            u = rng.random()
            if u < P1 + p:
                w = b[-1]; n = 1 if u < P1 else 3
                for _ in range(n): w = mutate(w, rng)
                if n == 3: CHAIN3.append((b[-1], w))
                b.append(w)
            else:
                b.append(str(rng.choice(vocab, p=pw)))
        blocks.append(b)
    return blocks

P1 = 0.02
CHAIN3 = []
OUT = HERE.parent / "derived" / "ge4-famG-chain3-seed-panel.json"
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
ps = [0.01, 0.02, 0.04]
seqs = np.random.SeedSequence(20261129).spawn(len(ps) * 20 * 2)
from rapidfuzz.distance import Levenshtein
lp_dist = Levenshtein.distance
diag = {}
k = 0; out = {"p1": P1, "reps": REPS, "voynich_ext_rescored": {b: vp[b]["ratio"] for b in lp.BINS}, "voynich_committed": V_D, "panel": {}}
for p in ps:
    r = {b: [] for b in ("d1", "d2", "d3")}
    for i in range(20):
        rng = np.random.default_rng(seqs[k]); nr = np.random.default_rng(seqs[k + 1]); k += 2
        bl = famD_blocks(lens, p, rng, vocabB, pwB, charsB, pcB)
        pr = lp.profile(ag.recode_blocks(bl, recX), [[False] * len(b) for b in bl], nr)
        for b in r: r[b].append(pr[b]["ratio"])
        if i == 0:
            d = [lp_dist(a, c) for a, c in CHAIN3]
            diag[str(p)] = {"n_chain3": len(d), "frac_exact3": float(np.mean([x == 3 for x in d])), "hist": {str(x): int(sum(1 for y in d if y == x)) for x in sorted(set(d))}}
        CHAIN3.clear()
    s = {}
    for b, v in r.items():
        a = np.array(v); t = V_D[b]
        s[b] = {"values": v, "mean": a.mean(), "sd": a.std(ddof=1), "min": a.min(), "max": a.max(),
                "frac_within_0.10": float((abs(a - t) <= 0.10).mean()), "voynich_in_band": bool(a.min() - .1 <= t <= a.max() + .1)}
    f = s["d1"]["frac_within_0.10"]
    s["reading"] = "not distinguishable" if (f >= .25 and s["d1"]["voynich_in_band"]) else "distinguishable" if f < .10 else "ambiguous"
    out["panel"][str(p)] = s
    print(p, {b: (round(s[b]["mean"], 3), round(s[b]["sd"], 3), s[b]["frac_within_0.10"], s[b]["voynich_in_band"]) for b in ("d1", "d2", "d3")}, s["reading"], flush=True)
out["chain3_diag_seed0_raw_eva"] = diag
OUT.write_text(json.dumps(out, indent=1) + "\n")
