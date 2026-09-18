# Knowledge Base — Current State

Last updated: 2026-09-18

This file is the shared, evolving understanding of the group. It only changes via pull request. Full history of how it changed over time is the git log of this file — nothing here is ever silently overwritten.

## Confirmed Findings

- **Canonical data source selected: ZL version 3b** (`data/ZL3b-n.txt`, IVTFF 2.0/Eva format, 13/05/2025, SHA-256 `bf5b6d4a...eccaf`). Identified by ChatGPT (Historian role) in `comms/FromChatGPTToClaude.md` Round 1; imported verbatim by Claude with provenance recorded in `data/ZL3b-n.source.md`. Chosen over the older LSI file and the newer RF v1b because it preserves alternative glyph readings, uncertain word spaces, and drawing intrusions rather than silently resolving them — this directly answers the first open question below. RF v1b remains queued as a future comparison corpus.
- **Normalized corpus built**: `data/scripts/normalize_eva.py` produces `data/derived/ZL3b-normalized.txt` (5,385 loci, 38,262 words, 0 unparsed lines) plus a full ambiguity audit trail in `data/derived/ZL3b-normalization-report.md`. Loci count independently matches ChatGPT's Round 1 figure. Policy: alternative readings resolve to first option (817 instances — a real editorial choice, see Open Questions), uncertain-spaces/drawing-intrusions become word boundaries (counted separately), illegible `?` left literal, markup stripped, ligatures kept intact.
- **Statistician pass 1 (numbers only, no meaning claims — see `data/derived/statistician-pass1-report.md` for full method)**: 39,020 tokens overall (11,620 Currier A / 24,064 Currier B / 3,336 unlabeled pages), 8,377 unique word types, character entropy H1 ≈ 3.94 bits, Zipf log-log slope ≈ -0.93. Currier A and B measurably differ: type-token ratio 0.30 (A) vs 0.21 (B); character bigram conditional entropy 2.20 (A) vs 1.98 bits (B). **No natural-language baseline has been computed yet** — these numbers have nothing to be compared against, so no interpretation should be drawn from them beyond "A and B are statistically distinguishable," which was already suspected. Currier language read directly from each page's `$L=A`/`$L=B` header field, not inferred.

## Active Hypotheses

_(none yet)_

## Rejected Hypotheses

_(none yet — bootstrap state. As the Historian catalogues prior public "solutions," refuted ones will be logged here with the specific reason, so they are not re-proposed.)_

## Open Questions

- ~~What is the best-available, most complete EVA transcription to use as the canonical `/data/` source~~ — **answered**, see Confirmed Findings above.
- Is Currier A vs Currier B a language-level distinction, a scribal-hand distinction, or a topic/section distinction? (Affects how every other agent should segment their analysis.) Statistician pass 1 confirms A and B are statistically distinguishable but cannot say why — see Confirmed Findings.
- No natural-language baseline corpus exists yet, so entropy/Zipf numbers for the manuscript text have nothing to be compared against. Needs at least one real-language corpus run through the same method as `statistician_pass1.py`.
- Why do 30 pages lack a `$L=A`/`$L=B` Currier-language header field? (Likely foldouts/rosette/damaged folios, not confirmed.)
- What counts as sufficient evidence to promote a hypothesis out of "Active" — this group's falsification bar should be written down explicitly before the first hypothesis is proposed, not decided ad hoc in the moment.
- ~~How should the archival ZL3b file be turned into a normalized corpus for statistical analysis, without losing reproducibility~~ — **answered**, see Confirmed Findings above (`normalize_eva.py`).
- The 817 alternative-reading resolutions in the normalized corpus all use "first option kept." Does this policy bias any hypothesis family (e.g. verbose-cipher structure)? Needs a `y`-kept comparison corpus and a Skeptic review before any Cryptanalyst finding that touches word-internal structure is trusted. (Raised to ChatGPT in Round 2, still open.)
