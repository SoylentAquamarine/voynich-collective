# Index

A flat file list for any external agent (ChatGPT, a local model, etc.) picking up this repo cold. Start with `README.md`, then `knowledge-base/state.md` for current status, then the relevant `agents/*.md` for whichever role you're acting as.

| File | Purpose |
|---|---|
| `README.md` | Project overview: goal, how the process works, current status |
| `INDEX.md` | This file |
| `knowledge-base/state.md` | **Read this first for current status.** Confirmed findings, active hypotheses, rejected hypotheses, open questions. Only changes via PR. |
| `agents/statistician.md` | Role: corpus statistics (entropy, n-grams, Currier A/B comparison) |
| `agents/linguist.md` | Role: tests "enciphered natural language" hypotheses |
| `agents/cryptanalyst.md` | Role: tests classical cipher structures |
| `agents/historian.md` | Role: paleography, provenance, prior claimed solutions — context only, no decoding |
| `agents/skeptic.md` | Role: falsifies every other agent's leading hypothesis, including "meaningless text" |
| `logs/README.md` | Log conventions — append-only, one file per session |
| `logs/2026-09-18-bootstrap.md` | First log entry: repo creation |
| `data/README.md` | What source data is needed and not yet present (EVA transcription) |

## Conventions for any agent contributing here

1. Never edit an existing `logs/*.md` file — add a new one.
2. Never edit `knowledge-base/state.md` directly on `main` — propose changes via PR so the diff is reviewable and the history is preserved.
3. A hypothesis needs to survive the Skeptic's review (see `agents/skeptic.md`) before moving from "Active Hypotheses" to "Confirmed Findings."
4. Cite sources and methods for every claim — this repo's value is the reasoning trail, not just conclusions.
