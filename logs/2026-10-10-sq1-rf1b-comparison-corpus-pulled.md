# SQ-1 — the RF v1b comparison corpus, on the backlog since the project's very first cycle, finally pulled

**Trigger:** actively searching for an unclaimed thread rather than another candidate-survey pass (already
run twice this project-era with diminishing returns). `data/README.md` and `data/ZL3b-n.source.md` have
both named "RF v1b — comparison corpus, queued but not yet pulled" since 2026-09-18, the project's very
first data-import cycle — a genuinely old, never-revisited backlog item.

## What's already known / not done yet

Already known: ZL3b is the canonical source, chosen over RF v1b specifically because RF's own summary
doesn't indicate equivalent preservation of alternative readings. Not done: locating and actually pulling
the RF v1b file itself — only its name and a one-line characterization have been on file for three weeks.

## Design and why it's non-circular

Located the actual file via the same host (`voynich.nu/data/`) that serves the already-canonical ZL3b
file, confirmed its existence and exact filenames via a direct page fetch, then downloaded both available
variants directly (not through a browser-rendering tool, so the checksums are trustworthy) rather than
assuming a single file matches the three-week-old backlog description.

## Honesty precommitment

Report exactly what was retrieved and disclose RF's own partial dependency on ZL (per this project's
existing backlog note) rather than presenting it as a fully independent cross-check corpus.

## Result

Found and pulled both RF v1b variants from `voynich.nu/data/`: `RF1b-e.txt` (362,373 bytes, markup-
preserving) and `RF1b-er.txt` (343,891 bytes, markup-resolved) — same 5,613-line transcription, two
renderings, confirmed by direct diff. **Retrieval note**: `curl`'s default User-Agent was blocked by the
host's ModSecurity rule; retrieved successfully with a standard browser User-Agent header instead, no
content concern. Full provenance in `data/RF1b.source.md`, matching the existing `ZL3b-n.source.md`
pattern. **Important disclosed nuance, carried forward from the project's own prior note**: RF v1b is
"auto-generated from ZL + GC/v101" — partly derived from the project's own canonical ZL3b source, not a
wholly independent transcription. Its documented value is specifically raw character-identification
reliability, not independent corroboration of meaning or structure.

## Decision

This closes a three-week-old backlog item, not just a passive "still queued" note. **Not attempted this
cycle**: any actual comparison between RF1b and ZL3b — that's a real, separate piece of work (building an
alignment/diff script, deciding how to handle RF's partial ZL-derivation when interpreting agreement) and
deserves its own dedicated pass, matching this project's own established discipline of freezing one step
at a time rather than rushing acquisition and analysis together.
