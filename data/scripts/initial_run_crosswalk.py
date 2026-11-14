#!/usr/bin/env python3
"""Crosswalk: list every >=8 same-initial run (EVA-char initials) with locus and tokens.
Precommit: logs/2026-11-14-fros62-f24v-crosswalk-selfreview.md. Usage: python3 -I data/scripts/initial_run_crosswalk.py
"""
import json, re, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
import normalize_eva as ne
SRC = {"ZL3b": REPO/"data"/"ZL3b-n.txt", "RF1b-er": REPO/"data"/"RF1b-er.txt"}
UNIT = re.compile(r"@\d+;|\{[^}]*\}|.")

def parse(path, ptype_only):
    rep = {k: [] for k in ("alt_readings","stripped_markup","drawing_intrusions","misaligned_intrusions","illegible_chars")}
    rows = []
    for raw in path.open(encoding="utf-8", errors="replace"):
        line = raw.rstrip("\n")
        if not line or line.startswith("#") or re.match(r"^<f[^.,>]+>\s+<!", line):
            continue
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
        rows.append((page, locus, lt, ne.tokenize(text.replace(" ", "."))))
    return rows

def runs(rows, scope):
    out, cur, prev = [], [], None
    def flush():
        if len(cur) >= 8: out.append(list(cur))
    for page, locus, lt, words in rows:
        for w in words:
            key = page if scope == "page" else (locus if scope == "line" else page)
            ini = None if "?" in w else UNIT.match(w).group(0)
            if cur and (ini is None or ini != cur[-1][3] or key != cur[-1][4]):
                flush(); cur = []
            if ini is not None:
                cur.append((page, locus, w, ini, key))
    flush()
    return out

res = {}
for name, path in SRC.items():
    for ptype in (True, False):
        rows = parse(path, ptype)
        for scope in ("line", "page"):
            rs = runs(rows, scope)
            k = f"{name}|{'P-only' if ptype else 'all-loci'}|{scope}"
            res[k] = [{"page": r[0][0], "loci": sorted({x[1] for x in r}), "initial": r[0][3],
                       "n": len(r), "tokens": [x[2] for x in r]} for r in rs]
            print(k, [(r["page"], r["initial"], r["n"]) for r in res[k]])
(REPO/"data"/"derived"/"initial-run-crosswalk.json").write_text(json.dumps(res, indent=1)+"\n")
