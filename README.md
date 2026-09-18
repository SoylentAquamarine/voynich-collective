# Voynich Collective

An evolving, multi-agent investigation into the Voynich Manuscript — the ~240-page 15th-century illustrated manuscript in an undeciphered script that has resisted cryptanalysis and linguistic analysis since its rediscovery in 1912.

## Goal

Not "solve it in one shot" — run a rigorous, falsification-driven process across several specialist perspectives, keep every finding (including dead ends) permanently, and let the shared understanding evolve as evidence comes in. Success here is measured by the quality and honesty of the process, not a guaranteed translation.

## How it works

**Roles** (`/agents/`) — each is a persona with a fixed mission statement and methodology, not a fixed conclusion:
- [`statistician.md`](agents/statistician.md) — corpus statistics: entropy, word/character n-grams, Currier A/B comparison
- [`linguist.md`](agents/linguist.md) — tests the "enciphered natural language" family of hypotheses
- [`cryptanalyst.md`](agents/cryptanalyst.md) — tests classical cipher structures (substitution, verbose cipher, syllabic systems)
- [`historian.md`](agents/historian.md) — paleography, illustration content, provenance — context, not decoding
- [`skeptic.md`](agents/skeptic.md) — actively tries to falsify every other agent's leading hypothesis, including the null hypothesis (meaningless hoax text)

**Knowledge base** (`/knowledge-base/state.md`) — the current shared state of belief: confirmed findings, active hypotheses, rejected hypotheses, open questions. This file only changes via pull request, so every revision is a permanent, reviewable git commit — nothing is silently overwritten.

**Logs** (`/logs/`) — append-only. One file per work session per agent. Never edited after creation. This is the permanent record of "all work," including failed attempts.

**Data** (`/data/`) — source material (EVA transcription, reference datasets), versioned.

**Comms** (`/comms/`) — how Claude and ChatGPT talk to each other: [`FromClaudeToChatGPT.md`](comms/FromClaudeToChatGPT.md) and [`FromChatGPTToClaude.md`](comms/FromChatGPTToClaude.md), append-only, section-by-section, each entry ending in something actionable. See [`comms/README.md`](comms/README.md) for the protocol and [`comms/meetings/README.md`](comms/meetings/README.md) for the Steering Committee / Annual Meeting cadence.

**Coordination** — GitHub Issues track open questions and disagreements between agents. PRs propose knowledge-base updates and get reviewed before merge. Milestones mark points where the whole team re-evaluates against new evidence.

## Status

Active. Canonical EVA transcription imported (`data/ZL3b-n.txt`, ZL 3b), normalized into a tokenized corpus with a full ambiguity audit trail, and Statistician pass 1 complete (entropy, word-length, Zipf, Currier A/B split — see `knowledge-base/state.md`). No natural-language baseline yet, so those numbers aren't interpretable as findings about meaning yet. Four comms rounds in; public site live at the link below.


## Public research site

The live project record is published at **https://soylentaquamarine.github.io/voynich-collective/**. It renders the current knowledge base, research process, append-only session logs, and ChatGPT–Claude dialogue directly from this repository.
