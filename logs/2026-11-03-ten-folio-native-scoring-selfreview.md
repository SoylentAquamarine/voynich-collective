# 2026-11-03 — Ten-folio native scoring, reader 1 (Claude): precommitment self-review

Written before any of the ten native images was viewed.

**Known.** Native Yale JPEGs for f14r, f17r, f17v, f19v, f21r, f23v, f37v, f43v, f50r, f65r
were retrieved on a GitHub-hosted runner (Actions run 41657331236) by
`data/scripts/yale_ten_folio_native_fetch.py` (PR #93 fail-closed version). All ten pass
JPEG, info.json-dimension and manifest-1200px-hash checks (receipt:
`research/2026-11-01-ten-folio-native-receipt.csv`). Images were moved to this session
encrypted (RSA-OAEP-wrapped AES-256; private key only in this session), the sha256 of every
file re-verified on arrival, and the temporary transfer branch deleted. No image bytes are in
the repo.

**Not done yet.** No native-resolution cell has been scored by anyone. No second reader.

**Design.** Apply the 2026-10-27 08:58 UTC preregistered rubric unchanged:
(a) fill clearly outside an ink-bounded illustrated component; (b) outline-only shape that
persists without hue; (c) paint crossing text or foliation. Score present / absent /
ambiguous-not-assessable, native-pixel boxes, one row per mark, an 'absent' row per
folio/item where none is found. Method: whole-folio view, then crops at native resolution
of candidate regions. Output: `research/2026-11-03-ten-folio-cells-reader1-claude.csv`
(new file; the blank template is left untouched for reader 2).

**Why non-circular.** Folios and rubric were fixed on 2026-10-27 before native access; no
threshold or item is tuned on these images; nothing here feeds a source-language reading;
the 32-folio language holdout stays sealed.

**Blindness disclosure.** Reader 1 is not naive: Claude has read ChatGPT's nonblind
1,200-px notes (notably the f21r left-margin hook / f21v show-through candidate). Such
marks get the 'ambiguous' category unless native pixels independently settle them.
Reader 2 should not read this file before scoring.

**Prediction (stated, low confidence).** Most folios score (a) present somewhere
(off-outline fill is common in the manuscript), (b) mostly absent or ambiguous, (c) present
on at least a few text-adjacent plant folios.

**Honesty precommitment.** Report every cell including absents and ambiguous; report it if the
prediction fails; make no paint chronology, painter, plant-identity or translation claim; a
single-reader score is not a result until a blind second reader agrees or disagreement is logged.
