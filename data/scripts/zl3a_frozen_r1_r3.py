#!/usr/bin/env python3
"""Fail-closed executable for the frozen R1-R3 checks on a cited ZL3a source.
Rules frozen in logs/2026-11-15-table12-minimal-discrepancy-selfreview.md (R1-R3) and
logs/2026-11-16-r2-conditional-edit-distance-selfreview.md (reading of an R2-true outcome).
Precommit for this runner: logs/2026-11-17-zl3a-frozen-r1-r3-runner-selfreview.md.

Usage: python3 -I data/scripts/zl3a_frozen_r1_r3.py --source PATH --sha256 HEX [--url URL] [--out PATH]
Exit 2 (nothing written) if the file is missing or its SHA-256 differs from --sha256.
Parser / initial units / run rules are imported unchanged from table12_selection_rule_grid.py
(the import re-runs that deterministic grid; its JSON must stay byte-identical -- check with git diff).
No p-values; no claim about language or meaning.
"""
import argparse, contextlib, hashlib, io, itertools, json, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))

ap = argparse.ArgumentParser()
ap.add_argument("--source", required=True)
ap.add_argument("--sha256", required=True)
ap.add_argument("--url", default=None)
ap.add_argument("--out", default=None)
a = ap.parse_args()
src = Path(a.source)
if not src.is_file():
    print(f"FAIL-CLOSED: source not found: {src}", file=sys.stderr); sys.exit(2)
data = src.read_bytes()
h = hashlib.sha256(data).hexdigest()
if h != a.sha256.strip().lower():
    print(f"FAIL-CLOSED: sha256 {h} != pinned {a.sha256}", file=sys.stderr); sys.exit(2)

with contextlib.redirect_stdout(io.StringIO()):
    import table12_selection_rule_grid as g

TARGET = set(g.TARGET)
TAIL = ["chokoishe", "chor", "cheol", "chol"]
HEAD = ["chokeos", "chees", "chr", "cheaiin"]

def contains(seq, sub):
    return any(seq[i:i+len(sub)] == sub for i in range(len(seq) - len(sub) + 1))

# R1
r1 = {}
for comma in ("break", "join"):
    rows = g.parse(src, False, comma)
    hit = [(loc, w) for p, loc, lt, w in rows if p == "f2v" and contains(w, TAIL)]
    r1[comma] = {"tail_loci": [loc for loc, _ in hit],
                 "R1": bool(hit) and any(contains(w, HEAD + TAIL) for _, w in hit),
                 "tail_line_tokens": [w for _, w in hit]}

# R2 (line scope, all loci) and R3 (cross-line cells, f24v reported as-is)
def cell(ptype, scope, comma, seg):
    rs = g.runs(g.parse(src, ptype, comma), scope, g.UNIT[seg])
    pages = sorted({r[0][0] for r in rs})
    return pages, [{"page": r[0][0], "loci": sorted({x[1] for x in r}), "initial": r[0][3], "n": len(r),
                    "tokens": [x[2] for x in r]} for r in rs if r[0][0] in TARGET | {"f24v"}]
r2, r3 = [], []
for comma, seg in itertools.product(("break", "join"), ("eva", "atomic")):
    pages, runs = cell(False, "line", comma, seg)
    r2.append({"comma": comma, "initial": seg, "pages": pages, "R2": set(pages) == TARGET,
               "f2v_runs": [r for r in runs if r["page"] == "f2v"]})
for ptype, scope, comma, seg in itertools.product((True, False), ("paragraph", "page"), ("break", "join"), ("eva", "atomic")):
    pages, runs = cell(ptype, scope, comma, seg)
    r3.append({"loci": "P-only" if ptype else "all", "scope": scope, "comma": comma, "initial": seg,
               "f24v": "f24v" in pages, "f24v_runs": [r for r in runs if r["page"] == "f24v"]})

text = data.decode("utf-8", errors="replace").splitlines()
out = {"source": {"path_basename": src.name, "url": a.url, "sha256": h, "bytes": len(data), "lines": len(text),
                  "header": next((l for l in text if l.startswith("#")), None)},
       "R1": r1, "R1_any": any(v["R1"] for v in r1.values()),
       "R2": r2, "R2_any": any(c["R2"] for c in r2),
       "R3": r3, "R3_f24v_cells": sum(c["f24v"] for c in r3),
       "note": "Infrastructure output; no language/meaning claim. If R2_any, inspect f2v_runs loci: a joined/merged "
               "f2v.7+8 locus = line-break difference; a single original line = token-initial differences (frozen 11-16 reading)."}
print(f"sha256={h} bytes={len(data)} lines={len(text)}")
print("R1:", {k: v["R1"] for k, v in r1.items()}, "tail loci:", {k: v["tail_loci"] for k, v in r1.items()})
for c in r2: print("R2", c["comma"], c["initial"], c["pages"], c["R2"], [r["loci"] for r in c["f2v_runs"]])
print("R3 f24v present in", out["R3_f24v_cells"], "of", len(r3), "cross-line cells")
dest = Path(a.out) if a.out else REPO / "data" / "derived" / f"zl3a-frozen-r1-r3-{h[:12]}.json"
dest.write_text(json.dumps(out, indent=1) + "\n")
print("wrote", dest)
