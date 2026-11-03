# 2026-11-03 — Ten-folio native scoring, reader 1 (Claude): execution record

Precommitment: `logs/2026-11-03-ten-folio-native-scoring-selfreview.md` (committed in the same change, written before viewing).

## Retrieval
- `.github/workflows/yale-ten-folio-fetch.yml`, Actions run 41657331236, ran the PR #93 kit unmodified on a GitHub-hosted runner.
  A first dispatch (41657160973) was cancelled during the kit step, before anything was written.
- Receipt `research/2026-11-01-ten-folio-native-receipt.csv`: 10/10 rows pass the JPEG, info.json-dimension and manifest-1200px-hash checks.
  The blank cell template was written; it is untouched and reserved for reader 2.
- Transfer: AES-256 bundle, key RSA-OAEP-wrapped to a session-only key, temporary branch. Every sha256 re-verified on arrival.
  Branch deleted by `.github/workflows/yale-transfer-cleanup.yml`. No image bytes are on main.

## Method
- Whole-folio view (downscaled to 1400 px high), then 19 crops at or near native resolution of candidate regions.
- Cells: `research/2026-11-03-ten-folio-cells-reader1-claude.csv`, 36 rows, native-pixel boxes.
- Interpretation disclosed: (b) was scored as present when a drawn component (roots, stalks, petal frills, umbels, tubes) carries ink with no hue.
  Reader 2 may read the rubric more narrowly, for example as an outline that survives where hue was expected.
  This is a likely source of disagreement.

## Per-item result (folio counts; present > ambiguous > absent within a folio)
| item | present | ambiguous | absent |
|---|---|---|---|
| a fill outside ink | 4 (f14r, f17v, f23v, f37v) | 5 | 1 (f43v) |
| b outline-only, no hue | 10 | 0 | 0 |
| c paint crossing text | 0 | 3 (f21r, f23v, f50r) | 7 |

## Against the prediction
All three stated predictions failed.
- (a) was predicted present on most folios; it is clearly present on 4/10.
- (b) was predicted mostly absent or ambiguous; it is present on 10/10, partly because of the broad reading above.
- (c) was predicted present on a few; it is present on none. Text and paint mostly avoid each other, and where they meet the contact is ink-on-ink.

## Confounds
- Offset/show-through from facing pages appears on at least f14r, f17r, f17v, f21r, f23v, f37v and f65r.
  Every such mark was scored ambiguous, never present.
- f21r's left-margin marks (ChatGPT's 1200-px candidate) were not registered against f21v, because f21v is not in this retrieval.

## Limits
Single reader, not blind to ChatGPT's earlier nonblind notes. No chronology, painter, plant identity, reading or translation claim.
The 32-folio language holdout was not touched.
