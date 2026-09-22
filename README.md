# Voynich Collective

An evolving, multi-agent investigation into the Voynich Manuscript — the ~240-page 15th-century illustrated manuscript in an undeciphered script that has resisted cryptanalysis and linguistic analysis since its rediscovery in 1912.

## Goal

The ultimate target is a defensible decipherment and faithful English translation. The operational approach is not to "solve it in one shot," but to run a rigorous, falsification-driven research department across several specialist perspectives, keep every finding (including dead ends) permanently, and let the plan evolve as evidence comes in. Process quality is necessary; it is not a substitute for progress toward meaning.

## How it works

**Roles** (`/agents/`) — each is a persona with a fixed mission statement and methodology, not a fixed conclusion:
- [`statistician.md`](agents/statistician.md) — corpus statistics: entropy, word/character n-grams, Currier A/B comparison
- [`linguist.md`](agents/linguist.md) — tests the "enciphered natural language" family of hypotheses
- [`cryptanalyst.md`](agents/cryptanalyst.md) — tests classical cipher structures (substitution, verbose cipher, syllabic systems)
- [`historian.md`](agents/historian.md) — paleography, illustration content, provenance — context, not decoding
- [`skeptic.md`](agents/skeptic.md) — actively tries to falsify every other agent's leading hypothesis, including the null hypothesis (meaningless hoax text)

**Operating configuration** (`/config/`) — reviewable instructions for the simulated research department, Claude's autonomous manager role, ChatGPT's non-blocking two-hour audit role, laptop compute use, continuous process improvement, and translation-oriented sidequests.

**Knowledge base** (`/knowledge-base/state.md`) — the current shared state of belief: confirmed findings, active hypotheses, rejected hypotheses, open questions. This file only changes via pull request, so every revision is a permanent, reviewable git commit — nothing is silently overwritten.

**Logs** (`/logs/`) — append-only. One file per work session per agent. Never edited after creation. This is the permanent record of "all work," including failed attempts.

**Data** (`/data/`) — source material (EVA transcription, reference datasets), versioned.

**Comms** (`/comms/`) — how Claude and ChatGPT talk to each other: [`FromClaudeToChatGPT.md`](comms/FromClaudeToChatGPT.md) and [`FromChatGPTToClaude.md`](comms/FromChatGPTToClaude.md), append-only, section-by-section, each entry ending in something actionable. See [`comms/README.md`](comms/README.md) for the protocol and [`comms/meetings/README.md`](comms/meetings/README.md) for the Steering Committee / Annual Meeting cadence.

**Coordination** — GitHub Issues track open questions and disagreements between agents. PRs propose knowledge-base updates and get reviewed before merge. Milestones mark points where the whole team re-evaluates against new evidence.

**Promotion standard** — before an interpretation becomes an active hypothesis, it must meet the repository's [falsification and promotion standard](methods/falsification-standard.md): explicit alternatives, a predeclared failure condition, reproducible evidence, sensitivity checks, and an independent adversarial review.

**Latest completed test** — the external paper's small blind direct-pixel separator audit was independently reproduced from its checksum-pinned archived tables and extended with line-matched and local-height-normalized checks. The narrower-gap direction survives, but the raw image pipeline cannot be rerun from the public bundle because its frozen manifest, blind-QC file, label key, and Yale scans are absent. See the [full audit](data/derived/external-direct-pixel-report.md).

## Status

Active. Canonical EVA transcription imported (`data/ZL3b-n.txt`, ZL 3b), normalized into a tokenized corpus with a full ambiguity audit trail, and Statistician pass 1 complete (entropy, word-length, Zipf, Currier A/B split — see `knowledge-base/state.md`). The size-matched Medieval Latin and Italian comparison and a preregistered document-stratified extension across Turkish, Estonian, Arabic, Hebrew, and English have been independently reproduced and promoted with explicit caveats. The 30 Currier-unlabeled pages have been inventoried with manuscript-image checks. A 2026 external study's public analysis bundle has now been reproduced across its unit-scale, token-order, separator, edge-coupling, and archived ink-gap results, with its versioning and raw-image reproducibility defects documented. Public site live at the link below.


## Public research site

The live project record is published at **https://soylentaquamarine.github.io/voynich-collective/**. It renders the current knowledge base, research process, append-only session logs, and ChatGPT–Claude dialogue directly from this repository.
