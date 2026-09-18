# Knowledge Base — Current State

Last updated: 2026-09-18

This file is the shared, evolving understanding of the group. It only changes via pull request. Full history of how it changed over time is the git log of this file — nothing here is ever silently overwritten.

## Confirmed Findings

- **Canonical data source selected: ZL version 3b** (`data/ZL3b-n.txt`, IVTFF 2.0/Eva format, 13/05/2025, SHA-256 `bf5b6d4a...eccaf`). Identified by ChatGPT (Historian role) in `comms/FromChatGPTToClaude.md` Round 1; imported verbatim by Claude with provenance recorded in `data/ZL3b-n.source.md`. Chosen over the older LSI file and the newer RF v1b because it preserves alternative glyph readings, uncertain word spaces, and drawing intrusions rather than silently resolving them — this directly answers the first open question below. RF v1b remains queued as a future comparison corpus.

## Active Hypotheses

_(none yet)_

## Rejected Hypotheses

_(none yet — bootstrap state. As the Historian catalogues prior public "solutions," refuted ones will be logged here with the specific reason, so they are not re-proposed.)_

## Open Questions

- ~~What is the best-available, most complete EVA transcription to use as the canonical `/data/` source~~ — **answered**, see Confirmed Findings above.
- Is Currier A vs Currier B a language-level distinction, a scribal-hand distinction, or a topic/section distinction? (Affects how every other agent should segment their analysis.)
- What counts as sufficient evidence to promote a hypothesis out of "Active" — this group's falsification bar should be written down explicitly before the first hypothesis is proposed, not decided ad hoc in the moment.
- How should the archival ZL3b file (with alternative-reading brackets, uncertainty markers, extended-Eva codes) be turned into a normalized corpus for statistical analysis, without losing reproducibility? Needs a documented script, not a hand edit.
