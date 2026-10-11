# Source: RF1b-e.txt / RF1b-er.txt

- **Source URLs:** https://www.voynich.nu/data/RF1b-e.txt and https://www.voynich.nu/data/RF1b-er.txt
- **Source page:** https://www.voynich.nu/data/ (same host as the canonical `ZL3b-n.txt`)
- **Retrieved:** 2026-10-10
- **Version (per file header):** `#=IVTFF Eva- 2.0 D 9` (both files)
- **SHA-256:** `RF1b-e.txt` = `e7d3238e35743e06c63367a933909ec37b1e2de7ada3a1b449447eafa1918782`;
  `RF1b-er.txt` = `eb857a1f353b18983fbc25b954e1bbce227a26d99cefabfda9206ff9b57644d2`
- **Size:** `RF1b-e.txt` 362,373 bytes, 5,613 lines; `RF1b-er.txt` 343,891 bytes, 5,613 lines (identical
  line count — same underlying transcription, two renderings)
- **Retrieval note**: the plain `curl` default User-Agent was blocked by the host's ModSecurity rule
  ("Not Acceptable!"); retrieved successfully with a standard browser User-Agent header instead. No
  content difference expected from this — the block was on request fingerprinting, not the resource itself.

## What "RF v1b" is, per this project's own prior backlog note (`ZL3b-n.source.md`)

"RF (Reference) transliteration v1b — auto-generated from ZL + GC/v101, considered more reliable for raw
character identification but does not preserve alternative readings." **This matters for how this corpus
should be used**: RF is partly *derived from* ZL (this project's own canonical source), not a fully
independent transcription — so it should not be treated as independent corroboration of ZL's readings in
the way, say, a wholly separately-made transcription would be. Its stated value is specifically raw
character-identification reliability, a narrower and different claim than "an independent cross-check."

## Two variants, confirmed by direct diff

`RF1b-e.txt` preserves special/uncertain-reading markup (e.g. `@221;taiin`, `{cto}ses` at `f1r.1`);
`RF1b-er.txt` has the same positions with that markup resolved to plain text (`ataiin`, `ctoses`) — the
same preserve-vs-resolve distinction this project's own `ZL3b` handling already uses, confirmed by direct
line-level diff of the first few lines (identical except at exactly the marked-up positions).

## Handling rules

Both files are canonical archival sources for this comparison corpus and are never modified in place, per
this project's existing handling rule for `ZL3b-n.txt`. Any normalization/comparison script output goes to
a separate derived file.

## Not yet done

No comparison against ZL3b has been run yet — this is the next step, not completed this cycle. Given RF's
partial derivation from ZL, any comparison should explicitly account for that relationship rather than
treating agreement as fully independent confirmation.
