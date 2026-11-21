#!/usr/bin/env python3
"""Adjacent edit-distance profile: Voynich ZL3b-EVA vs the two G4-matching toy generator families.

Precommit: logs/2026-11-21-ge4-levenshtein-profile-selfreview.md (pushed e26e457 before this file existed).
Family A = ge4_selfcitation_generator_control.generate (imported unchanged), q=0.8 S2_last10.
Family B = ge4_copy_mutate_generator per-token single-mutation rule, copied verbatim (that module runs main() on import), p=0.01.
Null: within-block shuffle, 500 reps. Usage: python3 data/scripts/ge4_levenshtein_profile.py  (needs rapidfuzz)
"""
import hashlib, json, sys
from collections import Counter
from pathlib import Path
import numpy as np
from rapidfuzz.distance import Levenshtein

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ge4_natural_language_control as g4
import ge4_selfcitation_generator_control as famA
import repeated_initial_run_null as base

OUT = HERE.parent / "derived" / "ge4-levenshtein-profile.json"
SEED, REPS, NSEEDS, TOL = 20261123, 500, 3, 0.10
BINS = ("d0_identical", "d1", "d2", "d3", "d4plus")


def profile(blocks, invalid, rng):
    words = [w for b in blocks for w in b]
    bad = [x for v in invalid for x in v]
    scope = np.repeat(np.arange(len(blocks)), [len(b) for b in blocks])
    vocab = {}
    wc = np.array([-(i + 1) if bd or not w else vocab.setdefault(w, len(vocab)) for i, (w, bd) in enumerate(zip(words, bad))])
    vw = list(vocab)
    same = scope[1:] == scope[:-1]
    cache = {}

    def dist(a, b):
        if a == b:
            return 0
        k = (a, b) if a < b else (b, a)
        v = cache.get(k)
        if v is None:
            v = cache[k] = min(Levenshtein.distance(vw[a], vw[b], score_cutoff=4), 4)
        return v

    def count(W):
        out = np.zeros((W.shape[0], 5), dtype=np.int64)
        ok = same[None, :] & (W[:, 1:] >= 0) & (W[:, :-1] >= 0)
        rr, cc = np.nonzero(ok)
        A, B = W[rr, cc], W[rr, cc + 1]
        d = np.fromiter((dist(int(a), int(b)) for a, b in zip(A, B)), dtype=np.int64, count=len(A))
        np.add.at(out, (rr, d), 1)
        return out

    obs = count(wc[None, :])[0]
    grp = [g for g in (np.flatnonzero(scope == s) for s in range(len(blocks))) if g.size > 1]
    nulls = []
    for start in range(0, REPS, 50):
        R = min(50, REPS - start)
        w2 = np.tile(wc, (R, 1))
        for g in grp:
            k = rng.random((R, g.size)).argsort(axis=1)
            w2[:, g] = wc[g][k]
        nulls.append(count(w2))
    N = np.concatenate(nulls)
    res = {}
    for j, b in enumerate(BINS):
        a = N[:, j]
        res[b] = {"obs": int(obs[j]), "null_mean": float(a.mean()), "null_sd": float(a.std()),
                  "ratio": float(obs[j] / a.mean()) if a.mean() else None,
                  "z": float((obs[j] - a.mean()) / a.std()) if a.std() else None,
                  "p_upper": (1 + int((a >= obs[j]).sum())) / (REPS + 1)}
    res["pairs"] = int(obs.sum()); res["tokens"] = len(words); res["vocab"] = len(vocab)
    return res


def famB_blocks(lens, p, rng, vocab, pw, chars, pc):
    def mutate(w, rng):  # verbatim from ge4_copy_mutate_generator.py
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
            b.append(mutate(b[-1], rng) if rng.random() < p else str(rng.choice(vocab, p=pw)))
        blocks.append(b)
    return blocks


def main():
    zl = base.SOURCES["ZL3b"]
    if hashlib.sha256(zl.read_bytes()).hexdigest() != g4.ZL3B_SHA:
        raise SystemExit("ZL3b-n SHA-256 mismatch")
    rows = base.parse(zl)
    _, scope, _ = base.build(rows, "eva", "paragraph")
    words = [w for _, _, _, ws in rows for w in ws]
    vb, vbad = [], []
    for s in np.unique(scope):
        idx = np.flatnonzero(scope == s)
        vb.append([words[i] for i in idx]); vbad.append(["?" in words[i] for i in idx])
    lens = [len(b) for b in vb]; T = len(words)
    seqs = iter(np.random.SeedSequence(SEED).spawn(64))
    out = {"precommit": "logs/2026-11-21-ge4-levenshtein-profile-selfreview.md", "seed": SEED, "reps": REPS, "tol": TOL,
           "rule": "family consistent iff for d in 1..3 Voynich ratio in [min_seed-0.10, max_seed+0.10]", "streams": {}}
    out["streams"]["voynich_ZL3b_eva"] = v = profile(vb, vbad, np.random.default_rng(next(seqs)))
    print("voynich", {b: round(v[b]["ratio"], 3) for b in BINS}, flush=True)

    # family A inputs exactly as in ge4_selfcitation_generator_control.main()
    poolA = [w for w in words if "?" not in w and w]
    cc = Counter(c for w in poolA for c in w)
    charsA = sorted(cc); cpA = np.array([cc[c] for c in charsA], float); cpA /= cpA.sum()
    # family B inputs exactly as in ge4_copy_mutate_generator.main()
    poolB = [w for w in words if "?" not in w and "{" not in w]
    vocabB, cnt = np.unique(poolB, return_counts=True); pwB = cnt / cnt.sum()
    charsB, ccB = np.unique(list("".join(poolB)), return_counts=True); pcB = ccB / ccB.sum()

    def split(st):
        bl, j = [], 0
        for L in lens:
            bl.append(st[j:j + L]); j += L
        return bl

    cells = [("A_q0.8_S2_last10", "rule"), ("B_p0.01", "rule"), ("A_q0.5_S2_last10", "ref"), ("B_p0", "ref")]
    for name, role in cells:
        for i in range(1, NSEEDS + 1):
            rng = np.random.default_rng(next(seqs))
            if name.startswith("A"):
                q = float(name.split("_")[1][1:])
                bl = split(famA.generate(T, q, "S2_last10", rng, poolA, charsA, cpA))
            else:
                p = float(name.split("_")[1][1:])
                bl = famB_blocks(lens, p, rng, vocabB, pwB, charsB, pcB)
            r = profile(bl, [[False] * len(b) for b in bl], np.random.default_rng(next(seqs)))
            r["role"] = role
            out["streams"][f"{name}_seed{i}"] = r
            print(name, i, {b: round(r[b]["ratio"], 3) for b in BINS}, flush=True)

    verdicts = {}
    for name, role in cells:
        if role != "rule":
            continue
        fails = []
        for b in ("d1", "d2", "d3"):
            rs = [out["streams"][f"{name}_seed{i}"][b]["ratio"] for i in range(1, NSEEDS + 1)]
            lo, hi = min(rs) - TOL, max(rs) + TOL
            if not (lo <= v[b]["ratio"] <= hi):
                fails.append({"bin": b, "voynich": v[b]["ratio"], "band": [lo, hi]})
        verdicts[name] = {"consistent": not fails, "failing_bins": fails}
    out["verdicts"] = verdicts
    print(json.dumps(verdicts, indent=1))
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
