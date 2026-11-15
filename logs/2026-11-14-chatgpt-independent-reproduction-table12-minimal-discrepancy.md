# Independent reproduction: Turenne Table 12 minimal-discrepancy map

**Date:** 2026-11-14 local / 2026-11-15 UTC  
**Status:** independent reproduction of the committed ZL3b/RF1b-er analysis; not a source reading or translation.

## Pinned inputs
- `data/ZL3b-n.txt` — Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`, 411,671 bytes.
- `data/RF1b-er.txt` — Git blob `85e5d4bcfe270dd4fb54cc477b1b5900020fa3f2`, 343,891 bytes.
- The committed reference implementation is `data/scripts/table12_selection_rule_grid.py`; the result being checked is `data/derived/table12-minimal-discrepancy.json`.

## Independent method
I fetched both complete input files through the authenticated GitHub connector and implemented the parser/run enumeration separately in JavaScript. The implementation did not import or execute the committed Python script. It independently applied the same documented first-choice alternative-reading rule, `<->` and `<~>` word boundaries, inline-markup stripping, illegible-token breaks, comma break/join variants, P-only/all-locus filters, line/paragraph/page scopes, and EVA/atomic initial tokenization. It then recomputed the 48 cells and the stated local edit costs.

## Result
| Measure | Independent result |
|---|---:|
| Grid cells | 48 |
| Feasible cells | 12 |
| Minimum local edit cost | 1 |
| Minimum-cost family | ZL3b / all loci / line scope / comma break |
| Equivalent initial tokenizations | EVA and atomic |
| Required edit | Join f2v.7 + f2v.8 |
| Feasible RF1b-er cells | 0 |
| Minimum paragraph/page cost | 4 |

The target set is `{fRos, f2v, f8v}`. Before the one join, the winning ZL3b cell contains `{fRos, f8v}`; the f2v run is split across lines 7 and 8. The join makes the set match without a non-target f24v run in that cell.

## Limits
This independently reproduces the working-transcription computation only. The cited paper reference names ZL3a, which was not fetched, read or hashed in this run. Therefore the result does not establish what ZL3a contains, does not prove Turenne used this rule, and does not show that the paper is wrong. No p-value, language identification, source reading or English translation follows.
