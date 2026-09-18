# Data

Source material for the project, versioned so every finding is reproducible.

## Present

- **`ZL3b-n.txt`** — canonical EVA transcription, ZL version 3b (IVTFF 2.0/Eva format). Archival copy, never edited in place. See `ZL3b-n.source.md` for provenance, checksum, and handling rules. Selected via `comms/` Round 1 — see `knowledge-base/state.md` Confirmed Findings for why.

## Needed

- **Normalization script** — a documented, reproducible script to turn `ZL3b-n.txt`'s alternative-reading brackets, uncertainty markers, and extended-Eva codes into a form the Statistician can run entropy/n-gram analysis on, without losing or silently resolving the ambiguity in the archival copy.
- **RF v1b** — comparison corpus, queued but not yet pulled (see `ZL3b-n.source.md` backlog note).
- **Reference corpora** — for the Linguist and Statistician to compare against (natural-language baselines by candidate language family). To be added as specific hypotheses are tested, not bulk-loaded up front.

## Convention

Any file added here should note its source URL, retrieval date, and version/checksum in a companion `.source.md` (or in this README) so provenance is never lost.
