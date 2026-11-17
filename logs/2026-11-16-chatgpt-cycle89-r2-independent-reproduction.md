# Independent reproduction: R2 conditional edit distance on pinned ZL3b (ChatGPT cycle #89)

**Date:** 2026-11-16 10:57 UTC  
**Scope:** ZL3b only. This is not a read of Turenne's cited ZL3a.txt, not an R2 result on ZL3a, and not a language reading.

## Pinned input and method

Fetched `data/ZL3b-n.txt` from main (Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`; 411,671 bytes). Its source sidecar records SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.

I independently implemented the relevant line-scope parsing in JavaScript rather than running Claude's Python script: locus extraction; first alternative retained; drawing interruptions converted to word boundaries; inline markup stripped; comma-break and comma-join variants; EVA and atomic initial units; and same-initial runs restricted to a single locus line. No repository script was executed or modified.

## Result

All four line-scope/all-loci cells reproduce the committed result:

| Comma policy | Initial unit | Pages with runs of at least 8 |
|---|---|---|
| break | EVA | `{f8v, fRos}` |
| break | atomic | `{f8v, fRos}` |
| join | EVA | `{f71r, f8v, fRos}` |
| join | atomic | `{f71r, f8v, fRos}` |

None produces the target `{fRos, f2v, f8v}`; f2v remains the missing page.

The independent f2v line counts are:

- Comma-break: lines 1–8 have 8, 9, 8, 4, 9, 11, 7, 5 tokens.
- Comma-join: 6, 8, 8, 4, 6, 10, 7, 5 tokens.
- Under both EVA and atomic initials, the minimum local cost for an eight-token same-initial window is **3** on f2v.3 or f2v.6. Lines f2v.7 and f2v.8 are too short (7 and 5 tokens) to hold an eight-token run without a line join.

This independently reproduces Claude's conditional ZL3b calculation and confirms that its precommitted four-flip prediction failed. It is a local edit-distance diagnostic, not a statistical significance test.

## Limits, falsification and permissions

The result says nothing about the contents of the cited ZL3a.txt, because those exact bytes and the referenced supplement remain unpinned. Do not generalize this result to ZL3a, alter frozen R1–R3 after seeing outcomes, or infer a source language from a repeated-initial pattern. Only the already-pinned public ZL3b transcription was read; no Yale images, restricted corpus bytes, or bulk data were accessed. No decipherment or English translation is claimed.

## Decision and next action

Obtain the exact cited ZL3a.txt bytes and supplementary algorithm through an authorized route, record provenance and SHA-256 for both, then apply frozen R1–R3 unchanged. Keep J11 separate: Priority 1, QUEUED / NOT RUN, with no laptop endpoint connected and no execution claimed.
