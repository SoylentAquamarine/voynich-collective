#!/usr/bin/env python3
"""Natural-language control for the >=4-shared-leading-character adjacency excess (G4).

Precommit: logs/2026-11-21-ge4-natural-language-control-selfreview.md (pushed before this file existed).
G4 = adjacent word pairs in one scope block, both non-empty, distinct, common char prefix >= 4.
Null: shuffle word order within each block; 2,000 reps. Voynich = ZL3b-n EVA paragraphs (parser imported
unchanged); NL = seven UD treebanks already pinned in this repo, size-matched, blocked to the Voynich mean
paragraph length. Corpora are downloaded to a cache dir (argv[1], default a temp dir) and never committed.
Usage: python3 -I data/scripts/ge4_natural_language_control.py [cache_dir]
"""
import hashlib, json, sys, tempfile, unicodedata, urllib.request
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
import repeated_initial_run_null as base
import language_baselines as lb

OUT = REPO / "data" / "derived" / "ge4-natural-language-control.json"
REPS, SEED = 2000, 20261121
ZL3B_SHA = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
REF_1118 = REPO / "data" / "derived" / "d-prefix-sensitivity.json"
EXCLUDED_UPOS = {"PUNCT", "SYM"}


def corpora():
    out = []
    for c in lb.CORPORA:
        out.append({"key": c["key"], "repository": c["repository"], "commit": c["commit"], "files": list(c["files"]),
                    "use_newdoc": False})
    panel = json.loads((REPO / "data" / "baselines" / "document-panel-v1.json").read_text(encoding="utf-8"))
    for c in panel["corpora"]:
        out.append({"key": c["key"], "repository": c["repository"], "commit": c["commit"],
                    "files": [(f["path"], f["sha256"]) for f in c["files"]], "use_newdoc": True})
    return out


def fetch(c, name, sha, cache):
    dest = cache / c["key"] / name
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        url = f"{c['repository'].replace('github.com', 'raw.githubusercontent.com')}/{c['commit']}/{name}"
        with urllib.request.urlopen(url, timeout=120) as r:
            dest.write_bytes(r.read())
    actual = hashlib.sha256(dest.read_bytes()).hexdigest()
    if actual != sha:
        raise RuntimeError(f"checksum mismatch {c['key']}/{name}: {actual}")
    return dest


def letters(form):
    return "".join(ch for ch in unicodedata.normalize("NFKC", form).lower() if ch.isalpha())


def sentences(paths, use_newdoc):
    """Yield (doc_id, [words]) per sentence; surface view (MWT header once, components skipped)."""
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
                a, b = tid.split("-")
                skip_to = int(b)
                w = letters(cols[1])
                if w:
                    words.append(w)
                continue
            if int(tid) <= skip_to or cols[3] in EXCLUDED_UPOS:
                continue
            w = letters(cols[1])
            if w:
                words.append(w)
        if words:
            yield doc, words


def blocks_nl(paths, use_newdoc, target, m):
    blocks, cur, cur_doc, total = [], [], None, 0
    for doc, ws in sentences(paths, use_newdoc):
        if total >= target:
            break
        if doc != cur_doc and cur:
            if len(cur) >= 2: blocks.append(cur)
            cur = []
        cur_doc = doc
        cur = cur + ws; total += len(ws)
        if len(cur) >= m:
            blocks.append(cur); cur = []
    if len(cur) >= 2: blocks.append(cur)
    return blocks, total


def lcp(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y: break
        n += 1
    return n


def analyse(blocks, rng, invalid=None, initials=None):
    """blocks: list of word lists. invalid: optional per-block bool lists (True = '?' word, cannot pair)."""
    words = [w for b in blocks for w in b]
    bad = [x for v in invalid for x in v] if invalid else [False] * len(words)
    scope = np.repeat(np.arange(len(blocks)), [len(b) for b in blocks])
    vocab = {}
    wc = np.array([-(i + 1) if bd else vocab.setdefault(w, len(vocab)) for i, (w, bd) in enumerate(zip(words, bad))])
    vw = list(vocab)
    init = {}
    first = [x for v in initials for x in v] if initials else [w[0] for w in words]
    ic = np.array([init.setdefault(f, len(init)) if c >= 0 and f is not None else -(i + 1)
                   for i, (f, c) in enumerate(zip(first, wc))])
    same = scope[1:] == scope[:-1]
    cache = {}
    def binof(a, b):
        k = (a, b) if a < b else (b, a)
        if k not in cache: cache[k] = min(lcp(vw[a], vw[b]), 4) - 1
        return cache[k]
    def count(W, I):
        out = np.zeros((W.shape[0], 4), dtype=np.int64)
        d = (I[:, 1:] == I[:, :-1]) & (W[:, 1:] != W[:, :-1]) & same[None, :] & (W[:, 1:] >= 0) & (W[:, :-1] >= 0)
        rr, cc = np.nonzero(d)
        A, B = W[rr, cc], W[rr, cc + 1]
        bins = np.fromiter((binof(int(a), int(b)) for a, b in zip(A, B)), dtype=np.int64, count=len(A))
        np.add.at(out, (rr, bins), 1)
        return out
    obs = count(wc[None, :], ic[None, :])[0]
    grp = [g for g in (np.flatnonzero(scope == s) for s in range(len(blocks))) if g.size > 1]
    nulls = []
    for start in range(0, REPS, 100):
        R = min(100, REPS - start)
        w2, i2 = np.tile(wc, (R, 1)), np.tile(ic, (R, 1))
        for g in grp:
            k = rng.random((R, g.size)).argsort(axis=1)
            w2[:, g] = wc[g][k]; i2[:, g] = ic[g][k]
        nulls.append(count(w2, i2))
    N = np.concatenate(nulls)
    res = {}
    for j, b in enumerate(("L1", "L2", "L3", "G4")):
        a = N[:, j]
        res[b] = {"obs": int(obs[j]), "null_mean": float(a.mean()), "null_sd": float(a.std()),
                  "ratio": float(obs[j] / a.mean()) if a.mean() else None,
                  "z": float((obs[j] - a.mean()) / a.std()) if a.std() else None,
                  "p": (1 + int((a >= obs[j]).sum())) / (REPS + 1)}
    res["G4"]["shows_excess"] = bool(res["G4"]["ratio"] is not None and res["G4"]["ratio"] >= 1.20 and res["G4"]["p"] <= 0.0125)
    res["tokens"] = len(words); res["blocks"] = len(blocks); res["vocab"] = len(vocab)
    return res


def main():
    zl = base.SOURCES["ZL3b"]
    if hashlib.sha256(zl.read_bytes()).hexdigest() != ZL3B_SHA:
        raise SystemExit("ZL3b-n SHA-256 mismatch")
    cache = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix="ge4-ud-"))
    rows = base.parse(zl)
    inits, scope, _ = base.build(rows, "eva", "paragraph")  # amendment: first EVA unit as initial (matches 11-18)
    words = [w for _, _, _, ws in rows for w in ws]
    assert len(words) == len(scope)
    vblocks, vbad, vinit = [], [], []
    for s in np.unique(scope):
        idx = np.flatnonzero(scope == s)
        vblocks.append([words[i] for i in idx]); vbad.append(["?" in words[i] for i in idx]); vinit.append([inits[i] for i in idx])
    T = len(words); m = T / len(vblocks)
    seqs = iter(np.random.SeedSequence(SEED).spawn(8))
    out = {"precommit": "logs/2026-11-21-ge4-natural-language-control-selfreview.md", "reps": REPS, "seed": SEED,
           "voynich_tokens_T": T, "voynich_paragraphs": len(vblocks), "mean_paragraph_len_m": m,
           "rule": "shows_excess iff G4 ratio >= 1.20 and p <= 0.0125", "corpora": {}}
    v = analyse(vblocks, np.random.default_rng(next(seqs)), vbad, vinit)
    ref = json.loads(REF_1118.read_text())["cells"]["ZL3b|eva"]["char"]["L4+"]["obs"]
    v["reproduces_1118_L4plus_obs"] = {"ref": ref, "match": v["G4"]["obs"] == ref}
    out["corpora"]["voynich_ZL3b_eva"] = v
    print("voynich", v["tokens"], v["blocks"], round(m, 2), v["G4"], v["reproduces_1118_L4plus_obs"], flush=True)
    for c in corpora():
        rng = np.random.default_rng(next(seqs))
        try:
            paths = [fetch(c, n, s, cache) for n, s in c["files"]]
        except Exception as e:  # reported, never substituted
            out["corpora"][c["key"]] = {"error": repr(e)}; print(c["key"], "ERROR", e, flush=True); continue
        bl, tot = blocks_nl(paths, c["use_newdoc"], T, m)
        r = analyse(bl, rng)
        r["source"] = {"repository": c["repository"], "commit": c["commit"], "files": [n for n, _ in c["files"]]}
        out["corpora"][c["key"]] = r
        print(c["key"], r["tokens"], r["blocks"], r["G4"], flush=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
