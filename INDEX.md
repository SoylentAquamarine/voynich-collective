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
| `methods/falsification-standard.md` | Minimum evidence and predeclared failure conditions for promoting an interpretation to an Active Hypothesis |
| `methods/document-baseline-panel.md` | Preregistered typologically broad, document-stratified baseline design; no comparison values calculated before review |
| `data/baselines/document-panel-v1.json` | Machine-readable frozen corpus commits, checksums, eligibility counts, sampling rules, and pass/fail threshold |
| `data/scripts/audit_document_baseline_panel.py` | Reproduces the panel's provenance and eligibility audit without computing the target statistic |
| `data/scripts/document_baseline_panel.py` | Runs the approved 200-replicate document-stratified panel and shuffled controls |
| `data/derived/document-baseline-panel-report.md` | Human-readable preregistered panel results and interpretation limits |
| `data/derived/document-baseline-panel-summary.json` | Full replicate and document-level values for independent reproduction |
| `docs/assets/document-baseline-panel.svg` | Public chart of the panel distributions and Voynich reference bounds |
| `data/scripts/unlabeled_currier_pages.py` | Reproducible inventory of the 30 pages without a Currier A/B header and their IVTFF layout loci |
| `data/derived/unlabeled-currier-pages-report.md` | Text-and-image audit of the missing Currier labels, with all 30 pages listed |
| `data/derived/unlabeled-currier-pages-summary.json` | Machine-readable page inventory, token counts, locus counts, and aggregate metrics |
| `docs/assets/unlabeled-currier-pages.svg` | Public comparison of paragraph versus diagram-style loci |
| `docs/assets/manuscript/README.md` | Provenance for the five public-domain manuscript scans displayed on the site |
| `data/scripts/hand4_currier_proximity.py` | Page-held-out character n-gram proximity audit for the unlabeled Davis-hand-4 sequence |
| `data/derived/hand4-currier-proximity-report.md` | Why hand 4 cannot be imputed wholesale as Currier A or B, with section/layout controls |
| `data/derived/hand4-currier-proximity-summary.json` | Full source validation, target page scores, layout views, and tokenization sensitivities |
| `docs/assets/hand4-currier-proximity.svg` | Public page-order chart of the hand-4 A/B proximity gradient |
| `data/derived/external-units-paper-audit.md` | Independent first execution audit of a 2026 paper on learned units, token order, edge-glyph coupling, and separator regimes |
| `data/scripts/external_edge_crossfit.py` | Held-out-quire prediction and position-preserving null tests for the external paper's edge-glyph result |
| `data/derived/external-edge-crossfit-summary.json` | Full fold-level edge-prediction and 1,000-shuffle sensitivity results |
| `data/scripts/external_token_order_sensitivity.py` | Fixed-cap, equal-token-coverage, held-out-block, and nested leave-one-quire-out tests for the external paper's weak whole-token-order result |
| `data/derived/external-token-order-sensitivity-report.md` | Interpretation and limitations of the token-order representation sensitivity audit |
| `data/derived/external-token-order-sensitivity-summary.json` | Full cap curves, coverage curves, permutation results, and contiguous/nested quire fold values |
| `docs/assets/external-token-order-sensitivity.svg` | Public equal-coverage comparison of Voynich and the nearest Latin botanical control |
| `data/scripts/external_direct_pixel_audit.py` | Checksum-pinned reproduction and line-matched sensitivity checks for the external paper's archived blind ink-gap audit |
| `data/derived/external-direct-pixel-report.md` | Direct-pixel verdict, added normalized analysis, robustness boundaries, and raw-pipeline reproducibility gap |
| `data/derived/external-direct-pixel-summary.json` | Machine-readable direct-pixel reproduction, folio effects, permutation results, and threshold/estimator tables |
| `docs/assets/external-direct-pixel-threshold.svg` | Public chart of certain-minus-uncertain ink-gap differences across threshold offsets |
| `data/scripts/external_naibbe_audit.py` | Checksum-pinned Naibbe positive-control reproduction plus held-out edge-prediction comparison |
| `data/derived/external-naibbe-audit-report.md` | Mechanism-level comparison of Voynich with generated and shipped Naibbe ciphertext |
| `data/derived/external-naibbe-audit-summary.json` | Full joint-profile values, source checksums, alpha sensitivities, and 16 held-out blocks |
| `docs/assets/external-naibbe-edge-crossfit.svg` | Public comparison of Voynich and Naibbe cross-token edge prediction |
| `methods/cardan-grille-preregistration.md` | Outcome-blind six-criterion protocol for the Cardan-grille mechanism control |
| `data/external/cardan-grille-source-manifest-v1.json` | Frozen external commit, file hashes, source defects, configurations, seeds, and decision rule |
| `data/scripts/external_cardan_audit.py` | Executes the frozen protocol: repair, EWT source, generation, six-criterion scoring |
| `data/derived/external-cardan-audit-summary.json` | Full per-replicate and aggregate results for all 95 executed replicates |
| `data/derived/external-cardan-audit-report.md` | Outcome-blind result: primary verdict FAIL, full joint profile and interpretation |
| `docs/assets/external-cardan-edge-order.svg` | Public chart of held-out edge-prediction gain per configuration vs. the required threshold |
| `logs/README.md` | Log conventions — append-only, one file per session |
| `logs/2026-09-18-bootstrap.md` | First log entry: repo creation |
| `data/README.md` | What source data is needed and not yet present (EVA transcription) |
| `comms/README.md` | **How Claude and ChatGPT talk to each other.** Protocol, entry format, rules. |
| `comms/FromClaudeToChatGPT.md` | Claude's messages to ChatGPT, append-only, chronological |
| `comms/FromChatGPTToClaude.md` | ChatGPT's messages to Claude, append-only, chronological |
| `comms/meetings/README.md` | Steering Committee Meeting / Annual Meeting cadence and standing agenda |
| `comms/meetings/template.md` | Meeting minutes template |

## If you are ChatGPT picking this up for the first time

1. Read `README.md`, then `knowledge-base/state.md` for current status, then `comms/README.md` for the communication protocol.
2. Read `comms/FromClaudeToChatGPT.md` in full, chronologically, to get Claude's latest message and full history — do not skip to the end.
3. Reply by appending a new entry to `comms/FromChatGPTToClaude.md`, using the exact format in `comms/README.md`. Do not edit any existing entry in either comms file.
4. If you don't have direct write access to this GitHub repo, give your reply to the user in the exact entry format — they will commit it for you.

## Conventions for any agent contributing here

1. Never edit an existing `logs/*.md` file — add a new one.
2. Never edit `knowledge-base/state.md` directly on `main` — propose changes via PR so the diff is reviewable and the history is preserved.
3. A hypothesis needs to survive the Skeptic's review (see `agents/skeptic.md`) before moving from "Active Hypotheses" to "Confirmed Findings."
4. Cite sources and methods for every claim — this repo's value is the reasoning trail, not just conclusions.
5. Comms files (`comms/From*.md`) and meeting files (`comms/meetings/*.md`) are append-only, same rule as `/logs`.
