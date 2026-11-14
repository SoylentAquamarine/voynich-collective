#!/usr/bin/env python3
"""Rule grid: can any segmentation/scope rule reproduce Turenne Table 12 ({fRos.62, f2v, f8v}) and drop f24v?
Precommit: logs/2026-11-14-table12-selection-rule-grid-selfreview.md. Usage: python3 -I data/scripts/table12_selection_rule_grid.py
48 cells = {ZL3b, RF1b-er} x {P-only, all loci} x {line, paragraph, page} x {comma break, comma join} x {eva, atomic}.
Run length >= 8; words containing '?' break runs. No p-values.
"""
import itertools, json, re, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
import normalize_eva as ne
SRC = {"ZL3b": REPO/"data"/"ZL3b-n.txt", "RF1b-er": REPO/"data"/"RF1b-er.txt"}
UNIT = {"eva": re.compile(r"@\d+;|\{[^}]*\}|."),
        "atomic": re.compile(r"@\d+;|\{[^}]*\}|ckh|cth|cph|cfh|ch|sh|.")}
TARGET = {"fRos", "f2v", "f8v"}

def parse(path, ptype_only, comma):
    rep = {k: [] for k in ("alt_readings","stripped_markup","drawing_intrusions","misaligned_intrusions","illegible_chars")}
    rows = []
    for raw in path.open(encoding="utf-8", errors="replace"):
        line = raw.rstrip("\n")
        if not line or line.startswith("#"): continue
        p = ne.strip_locus_tag(line)
        if p is None: continue
        locus, text = p
        page, rest = locus.split(".", 1)
        lt = rest.split(",", 1)[1]
        if ptype_only and (len(lt) < 2 or lt[1] != "P"): continue
        text = ne.resolve_alt_readings(text, locus, rep)
        text = ne.handle_drawing_intrusion(text, locus, rep)
        text = ne.handle_illegible(text, locus, rep)
        text = ne.strip_markup(text, locus, rep)
        if comma == "join": text = text.replace(",", "")
        rows.append((page, locus, lt, ne.tokenize(text.replace(" ", "."))))
    return rows

def runs(rows, scope, unit):
    out, cur, sid, prev_page, new_after_end = [], [], -1, None, False
    def flush():
        if len(cur) >= 8: out.append(list(cur))
    for page, locus, lt, words in rows:
        if scope == "line": sid += 1
        elif scope == "page":
            if page != prev_page: sid += 1
        else:  # paragraph, same rule as repeated_initial_run_null.py
            if page != prev_page or lt[0] in "@*" or new_after_end: sid += 1
            new_after_end = lt[0] == "="
        prev_page = page
        for w in words:
            ini = None if "?" in w else unit.match(w).group(0)
            if cur and (ini is None or ini != cur[-1][3] or sid != cur[-1][4]):
                flush(); cur = []
            if ini is not None: cur.append((page, locus, w, ini, sid))
    flush()
    return out

cells = []
for name, ptype, scope, comma, seg in itertools.product(SRC, (True, False), ("line","paragraph","page"), ("break","join"), ("eva","atomic")):
    rs = runs(parse(SRC[name], ptype, comma), scope, UNIT[seg])
    pages = sorted({r[0][0] for r in rs})
    f1 = TARGET <= set(pages)
    cells.append({"transcription": name, "loci": "P-only" if ptype else "all", "scope": scope, "comma": comma, "initial": seg,
                  "n_runs": len(rs), "pages": pages, "F1": f1, "F2": f1 and "f24v" not in pages, "F3": set(pages) == TARGET,
                  "has": {k: k in pages for k in ("fRos", "f2v", "f8v", "f24v")},
                  "runs": [{"page": r[0][0], "loci": sorted({x[1] for x in r}), "initial": r[0][3], "n": len(r),
                            "tokens": [x[2] for x in r]} for r in rs if r[0][0] in TARGET | {"f24v"}]})
summ = {"cells": len(cells), "F1": sum(c["F1"] for c in cells), "F2": sum(c["F2"] for c in cells), "F3": sum(c["F3"] for c in cells),
        "f24v_present": sum(c["has"]["f24v"] for c in cells),
        "fRos_present_P_only": sum(c["has"]["fRos"] for c in cells if c["loci"] == "P-only"),
        "f8v_present_RF1b_join": [c["has"]["f8v"] for c in cells if c["transcription"] == "RF1b-er" and c["comma"] == "join"]}
for c in cells:
    print(f'{c["transcription"]:7} {c["loci"]:6} {c["scope"]:9} {c["comma"]:5} {c["initial"]:6} n={c["n_runs"]:3} '
          + " ".join(f'{k}={int(v)}' for k, v in c["has"].items()) + f' F1={int(c["F1"])} F2={int(c["F2"])} F3={int(c["F3"])}')
print(json.dumps(summ))
(REPO/"data"/"derived"/"table12-selection-rule-grid.json").write_text(json.dumps({"summary": summ, "cells": cells}, indent=1)+"\n")
