# Data

Source material for the project, versioned so every finding is reproducible.

## Present

- **`ZL3b-n.txt`** — canonical EVA transcription, ZL version 3b (IVTFF 2.0/Eva format). Archival copy, never edited in place. See `ZL3b-n.source.md` for provenance, checksum, and handling rules. Selected via `comms/` Round 1 — see `knowledge-base/state.md` Confirmed Findings for why.
- **`RF1b-e.txt` / `RF1b-er.txt`** — comparison corpus, pulled 2026-10-10 (three weeks after being queued). Markup-preserving and markup-resolved variants of the same transcription; partly derived from ZL3b itself, not fully independent — see `RF1b.source.md` for provenance and the disclosed derivation caveat.

## Needed

- **Normalization script** — a documented, reproducible script to turn `ZL3b-n.txt`'s alternative-reading brackets, uncertainty markers, and extended-Eva codes into a form the Statistician can run entropy/n-gram analysis on, without losing or silently resolving the ambiguity in the archival copy.
- **An RF1b-vs-ZL3b comparison** — not yet run; needs to account for RF's partial derivation from ZL when interpreting any agreement.
- **Reference corpora** — for the Linguist and Statistician to compare against (natural-language baselines by candidate language family). To be added as specific hypotheses are tested, not bulk-loaded up front.

## Convention

Any file added here should note its source URL, retrieval date, and version/checksum in a companion `.source.md` (or in this README) so provenance is never lost.
