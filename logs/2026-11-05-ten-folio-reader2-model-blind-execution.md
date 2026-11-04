# 2026-11-05 — Ten-folio cells, provisional reader 2 (information-blind model subagent): execution record

Precommitment: `logs/2026-11-05-ten-folio-reader2-model-blind-selfreview.md` (commit 84e03d7, pushed before the fetch and before scoring).

## Retrieval
- Actions run 41831909543 (`.github/workflows/yale-ten-folio-reader2-transfer.yml`): all ten native URLs from the receipt re-fetched;
  every sha256 equals the receipt's `native_sha256` (the workflow fails closed otherwise). Re-verified on arrival in this session: 10/10.
- Transfer: AES-256 bundle, key wrapped to a fresh session-only RSA-3072 key (`.github/yale-transfer-pub-r2.pem`; private half deleted
  after decryption). Temporary branch removed with `yale-transfer-cleanup.yml`. Images and crops were deleted from the session after
  scoring. Receipt and blank template on main untouched. No image bytes on main.

## Scorer
- A fresh general-purpose subagent with no conversation context. Its brief contained only the template's rubric lines, the column list,
  the folio list and a scratch directory holding the ten images and a copy of the blank template. It was told not to read anything else
  under the home directory (including this repo) and not to web-search, and to attest to that.
- Attestation returned: it opened nothing outside the scratch directory and made no web searches. I cannot verify this beyond its word and
  the fact that its notes contain no reader-1 vocabulary I did not also give it; disclosed as a limit.
- Output: `research/2026-11-05-ten-folio-cells-reader2-provisional-subagent.csv`, 59 rows, all 30 folio-items covered,
  `reader_id = claude-subagent-blind`. Copied verbatim.

## Comparison (rule fixed in the precommitment: folio-level present > ambiguous > absent)
| | agree | of |
|---|---|---|
| a fill outside ink | 6 | 10 |
| b outline-only, no hue | 8 | 10 |
| c paint crossing text | 4 | 10 |
| **all** | **18** | **30** (raw 0.60; Cohen's kappa 0.37, chance agreement 0.37) |

Disagreements (r1 = reader 1, r2 = this pass):
- a: f17r r1 ambiguous / r2 present; f19v ambiguous / present; f21r ambiguous / present (r2 flags its f21r call as a judgement call: per-leaf outline); f43v absent / ambiguous.
- b: f14r present / ambiguous; f17v present / ambiguous.
- c: f17r, f17v, f19v, f37v r1 absent / r2 ambiguous (r2: mirrored "ghost" paint under text lines); f23v, f50r r1 ambiguous / r2 absent.

**No disagreement is a present-versus-absent flip.** All twelve sit on the ambiguous boundary. Neither reader scores (c) present on any folio.
Both score (b) present on 8 of the same folios. r2 scores (a) present on 7 folios (r1: 4); the four r1 (a)-present folios are all r2 present too.

## Against the prediction
- "Agreement highest on (c), lowest on (b)": **failed, reversed.** (b) agreed most (8/10), (c) least (4/10). Reader 2 read (b) in the same
  broad plain-wording way that reader 1 disclosed as a likely source of disagreement, so it was not one. (c) splits on how to score
  offset/show-through paint lying under text: r1 absent, r2 ambiguous.
- "Raw agreement 0.6–0.8": held, at the bottom edge (0.60).

## What this does and does not show
- Substantive convergence: no paint crosses text on any of the ten folios (both readers), and outline-only components are common.
  Fill outside ink is present on at least 4 folios on both readings.
- The ambiguous category is where readers diverge; a kappa of 0.37 is modest and is driven by that boundary, mainly offset handling.
- Both readers are the same model family. This pass is information-blind, not independent. It does **not** discharge the protocol's
  independent second-reader requirement; whether it counts toward it is a Director/ChatGPT decision.
- No chronology, painter, plant identity, reading or translation claim. The 32-folio language holdout was not touched.
