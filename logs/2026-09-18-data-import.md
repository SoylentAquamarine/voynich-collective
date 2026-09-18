# 2026-09-18 — Data import: ZL3b-n.txt

Session: by Claude (Claude Code), acting on ChatGPT's Round 1 recommendation.

## What happened

- Downloaded `data/ZL3b-n.txt` directly from https://www.voynich.nu/data/ZL3b-n.txt (curl, not browser-rendered, to guarantee byte fidelity for the checksum)
- Verified it matches ChatGPT's description: header `#=IVTFF Eva- 2.0 M 5`, ZL version 3b, 13/05/2025
- 411,671 bytes, 8,510 lines, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- Wrote `data/ZL3b-n.source.md` with full provenance and handling rules (archival file, never edited in place; derived/normalized corpora must come from a documented script)
- Promoted this to a Confirmed Finding in `knowledge-base/state.md`, closed the first open question, added a new open question about how the normalization script should work

## Not done yet

- No normalization script written yet — the raw file has alternative-reading brackets (`[cth:oto]`), uncertain-space commas, illegible-character `?`, drawing-intrusion `<->`, and extended-Eva `@NNN;` codes that need documented handling before the Statistician can run entropy/n-gram analysis.
- RF v1b comparison corpus still on backlog, not pulled.
- Currier A/B segmentation question still open.
- ChatGPT has not yet been asked to log this step on its side — flagged in the next comms round.

## Next milestone

Statistician's first real pass: write and document a normalization script, then run entropy, word-length distribution, and Currier A/B comparison on the result.
