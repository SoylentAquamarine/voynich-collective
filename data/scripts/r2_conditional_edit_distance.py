#!/usr/bin/env python3
"""Given R1 false (no f2v.7+8 join), how many token-initial changes on one f2v line would a ZL3b-like
source need for a line-scope, all-loci cell to give exactly {fRos, f2v, f8v}? ZL3b only.
Precommit: logs/2026-11-16-r2-conditional-edit-distance-selfreview.md. Usage: python3 -I data/scripts/r2_conditional_edit_distance.py
Parser and initial-unit rules imported unchanged from table12_selection_rule_grid.py (import re-runs that
grid and rewrites its JSON; the grid is deterministic, so the file must come out byte-identical -- checked by git diff).
"""
import json, sys
from collections import Counter
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "data" / "scripts"))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import table12_selection_rule_grid as g
out = []
for comma in ("break", "join"):
    for seg in ("eva", "atomic"):
        rows = g.parse(g.SRC["ZL3b"], False, comma)
        pages = sorted({r[0][0] for r in g.runs(rows, "line", g.UNIT[seg])})
        best, lines = None, []
        for page, locus, lt, words in rows:
            if page != "f2v": continue
            ini = [None if "?" in w else g.UNIT[seg].match(w).group(0) for w in words]
            rec = {"locus": locus, "n_tokens": len(words)}
            if len(words) >= 8:
                costs = []
                for s in range(len(words) - 7):
                    c = Counter(x for x in ini[s:s+8] if x is not None)
                    top, k = c.most_common(1)[0] if c else (None, 0)
                    costs.append((8 - k, s, top))
                cost, s, top = min(costs)
                rec.update(cost=cost, window_start=s, initial=top, max_same_in_window=8 - cost)
                if best is None or cost < best[0]: best = (cost, locus, s, top)
            else:
                rec["cost"] = None
            lines.append(rec)
        out.append({"comma": comma, "initial": seg, "pages": pages,
                    "fRos": "fRos" in pages, "f8v": "f8v" in pages, "f24v": "f24v" in pages, "f2v": "f2v" in pages,
                    "min_cost": best[0] if best else None, "argmin": {"locus": best[1], "window_start": best[2], "initial": best[3]} if best else None,
                    "f2v_lines": lines})
for c in out:
    print(c["comma"], c["initial"], "pages=", c["pages"], "min_cost=", c["min_cost"], "argmin=", c["argmin"])
    print("   ", [(l["locus"], l["n_tokens"], l["cost"]) for l in c["f2v_lines"]])
(REPO / "data" / "derived" / "r2-conditional-edit-distance.json").write_text(json.dumps(out, indent=1) + "\n")
