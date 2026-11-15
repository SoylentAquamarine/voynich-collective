#!/usr/bin/env python3
"""Minimal-discrepancy map: fewest local edits (breaks/joins) turning each 48-grid cell into exactly
Turenne Table 12 {fRos, f2v, f8v}. Precommit: logs/2026-11-15-table12-minimal-discrepancy-selfreview.md
Reuses parse()/runs() from table12_selection_rule_grid.py unchanged (source exec'd up to the cell loop).
Usage: python3 -I data/scripts/table12_minimal_discrepancy.py
"""
import itertools, json, math
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
src = (REPO/"data"/"scripts"/"table12_selection_rule_grid.py").read_text()
g = {"__file__": str(REPO/"data"/"scripts"/"table12_selection_rule_grid.py"), "__name__": "grid"}
exec(src.split("\ncells = []")[0], g)
parse, runs, SRC, UNIT, TARGET = g["parse"], g["runs"], g["SRC"], g["UNIT"], g["TARGET"]

def summarize(rs):
    return [{"page": r[0][0], "n": len(r), "loci": sorted({x[1] for x in r}, key=lambda l: int(l.split(".")[1].split(",")[0]))} for r in rs]

out = []
for name, ptype, scope, comma, seg in itertools.product(SRC, (True, False), ("line","paragraph","page"), ("break","join"), ("eva","atomic")):
    rows = parse(SRC[name], ptype, comma)
    rs = summarize(runs(rows, scope, UNIT[seg]))
    pages = {r["page"] for r in rs}
    edits, cost, why = [], 0, []
    for r in rs:
        if r["page"] not in TARGET:
            k = math.ceil((r["n"] - 7) / 8)
            cost += k; edits.append(f'break {r["page"]} ({r["n"]}-run, {r["loci"][0]}..{r["loci"][-1]}) x{k}')
    para = summarize(runs(rows, "paragraph", UNIT[seg])) if scope == "line" else []
    for t in sorted(TARGET - pages):
        cand = [p for p in para if p["page"] == t and p["n"] >= 8 and len(p["loci"]) == 2]
        if cand:
            cost += 1; edits.append(f'join {cand[0]["loci"][0]}+{cand[0]["loci"][1]} ({t})')
        else:
            cost = math.inf; why.append(f"{t} missing, not recoverable by one join")
    out.append({"transcription": name, "loci": "P-only" if ptype else "all", "scope": scope, "comma": comma,
                "initial": seg, "pages": sorted(pages), "cost": cost, "edits": edits, "infeasible_because": why})
fin = [c for c in out if c["cost"] != math.inf]
mn = min((c["cost"] for c in fin), default=None)
for c in out:
    print(f'{c["transcription"]:7} {c["loci"]:6} {c["scope"]:9} {c["comma"]:5} {c["initial"]:6} cost={c["cost"]} ' + "; ".join(c["edits"] + c["infeasible_because"]))
summ = {"cells": len(out), "feasible": len(fin), "min_cost": mn,
        "min_cells": [f'{c["transcription"]}|{c["loci"]}|{c["scope"]}|{c["comma"]}|{c["initial"]}' for c in fin if c["cost"] == mn],
        "rf1b_feasible": sum(c["transcription"] == "RF1b-er" for c in fin),
        "para_page_min_cost": min((c["cost"] for c in fin if c["scope"] != "line"), default=None)}
print(json.dumps(summ, indent=1))
for c in out:
    if c["cost"] == math.inf: c["cost"] = "inf"
(REPO/"data"/"derived"/"table12-minimal-discrepancy.json").write_text(json.dumps({"summary": summ, "cells": out}, indent=1)+"\n")
