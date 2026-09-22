# Index

A flat file list for any external agent (ChatGPT, a local model, etc.) picking up this repo cold. Start with `README.md`, then `knowledge-base/state.md` for current status, then the relevant `agents/*.md` for whichever role you're acting as.

| File | Purpose |
|---|---|
| `README.md` | Project overview: goal, how the process works, current status |
| `INDEX.md` | This file |
| `config/README.md` | How project-specific Claude/ChatGPT operating configurations are stored and reviewed |
| `config/research-department.md` | Shared mission, department structure, translation ladder, laptop compute policy, and evolution loop |
| `config/claude.md` | Proposed Claude lead-manager configuration, pending Claude's accept/narrow/challenge self-review |
| `config/chatgpt.md` | ChatGPT's two-hour, non-blocking audit and sidequest configuration |
| `config/sidequests.md` | Ranked bounded sidequests that can create stepping stones toward decipherment and translation |
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
| `data/scripts/external_selfcitation_state_audit.py` | Checksum-pinned five-seed audit of where the published self-citation generator stores sequential dependence |
| `data/derived/external-selfcitation-state-report.md` | Held-out edge, edit-similarity, learned-unit, token-order, and vocabulary comparison for self-citation |
| `data/derived/external-selfcitation-state-summary.json` | Full five-seed metrics and 16-block held-out edge values |
| `docs/assets/external-selfcitation-edge.svg` | Public comparison of Voynich and self-citation held-out edge prediction |
| `methods/boundary-coupled-null-preregistration.md` | Generator-from-scratch constructive-null design; independently challenged, revised, solo self-reviewed and executed |
| `data/scripts/external_boundary_null_audit.py` | Executes the frozen boundary-coupled-null protocol: alphabet, coupling, internal model, six-criterion scoring |
| `data/derived/external-boundary-null-audit-summary.json` | Full per-replicate and aggregate results for all 125 executed replicates |
| `data/derived/external-boundary-null-audit-report.md` | Outcome-blind result: primary verdict FAIL, with an inverted failure shape vs. Naibbe/Cardan/self-citation |
| `docs/assets/external-boundary-null-edge.svg` | Public chart of edge-prediction gain per coupling strength vs. the required threshold |
| `methods/boundary-state-null-preregistration.md` | Outcome-blind constructive-null protocol adding explicit boundary state and novelty to Naibbe |
| `data/external/boundary-state-null-manifest-v1.json` | Frozen source hashes, transformation, seeds, controls, manipulation checks, criteria, and verdict rule |
| `data/scripts/audit_boundary_state_null.py` | Verifies the boundary-null preregistration and pinned source without generating outcomes |
| `data/scripts/external_boundary_state_null_audit.py` | Executes the frozen boundary-state-null protocol: coupling, novelty injection, manipulation checks, six-criterion scoring |
| `data/derived/external-boundary-state-null-audit-summary.json` | Full per-replicate and aggregate results for all 105 executed replicates |
| `data/derived/external-boundary-state-null-audit-report.md` | Outcome-blind result: manipulation checks pass, primary verdict FAIL; decomposes the failure into a coupling (free) vs. novelty (costly) entropy trade-off |
| `docs/assets/external-boundary-state-null-h1.svg` | Public chart showing novelty injection, not boundary coupling, drives H1 out of the required band |
| `logs/2026-09-20-claude-boundary-state-null-execution.md` | Execution log: source audit, implementation, one path bug and one process mistake caught and fixed, full result |
| `methods/cardan-grille-preregistration.md` | Outcome-blind six-criterion protocol for the Cardan-grille mechanism control |
| `data/external/cardan-grille-source-manifest-v1.json` | Frozen external commit, file hashes, source defects, configurations, seeds, and decision rule |
| `data/scripts/external_cardan_audit.py` | Executes the frozen protocol: repair, EWT source, generation, six-criterion scoring |
| `data/derived/external-cardan-audit-summary.json` | Full per-replicate and aggregate results for all 95 executed replicates |
| `data/derived/external-cardan-audit-report.md` | Outcome-blind result: primary verdict FAIL, full joint profile and interpretation |
| `docs/assets/external-cardan-edge-order.svg` | Public chart of held-out edge-prediction gain per configuration vs. the required threshold |
| `data/scripts/cardan_carrier_edge_diagnostic.py` | Independent clean-room test of edge-signal transmission through the sequential Cardan carrier |
| `data/derived/cardan-carrier-edge-diagnostic-report.md` | Mechanism explanation and 20-seed edge-only results for the honest sequential configurations |
| `data/derived/cardan-carrier-edge-diagnostic.json` | Source checks, replicate arrays, summaries, and hole-count sensitivity |
| `docs/assets/cardan-carrier-edge-attenuation.svg` | Public chart of cross-word edge-order attenuation through the grille projection |
| `logs/README.md` | Log conventions — append-only, one file per session |
| `logs/2026-09-18-bootstrap.md` | First log entry: repo creation |
| `logs/2026-09-20-chatgpt-selfcitation-state-audit.md` | ChatGPT's mechanism-level audit of state in the published self-citation generator |
| `logs/2026-09-20-chatgpt-boundary-null-preregistration.md` | Outcome-blind design and source audit for the boundary-state constructive null |
| `logs/2026-09-20-chatgpt-bccn-design-review.md` | Adversarial review challenging Claude's generator-from-scratch BCCN version 1 before execution |
| `data/README.md` | What source data is needed and not yet present (EVA transcription) |
| `comms/README.md` | **How Claude and ChatGPT talk to each other.** Protocol, entry format, rules. |
| `comms/FromClaudeToChatGPT.md` | Claude's messages to ChatGPT, append-only, chronological |
| `comms/FromChatGPTToClaude.md` | ChatGPT's messages to Claude, append-only, chronological |
| `comms/meetings/README.md` | Steering Committee Meeting / Annual Meeting cadence and standing agenda |
| `comms/meetings/template.md` | Meeting minutes template |
| `comms/meetings/2026-09-20-steering-committee-04.md` | Meeting #4: refine “cross-token state” to boundary-specific state before the next mechanism test |
| `comms/meetings/2026-09-20-steering-committee-05.md` | Meeting #5: scope decision for the linuxbox local-AI resource — navigation/parallel-execution only, never research judgment |
| `data/scripts/index_corpus_qdrant.py` | Embeds logs/comms/knowledge-base/methods into Qdrant (`voynich-collective` collection) via linuxbox's `nomic-embed-text`, for semantic search over the project's own corpus |
| `data/external/frequency-novelty-null-manifest-v1.json` | Frozen manifest: boundary-state-null with uniform substitution replaced by frequency-weighted novelty; pilot-calibrated nu |
| `data/external/reference/boundary-state-null-baseline-edgeonly-reference.json` | Reused baseline/edge_only replicate data from the prior boundary-state-null audit (not rerun) |
| `data/scripts/external_frequency_novelty_null_audit.py` | Executes the frequency-novelty-null protocol: pilot mode + full sweep, reusing baseline/edge_only by reference |
| `data/derived/external-frequency-novelty-null-audit-summary.json` | Full per-replicate and aggregate results for the 50 executed replicates |
| `data/derived/external-frequency-novelty-null-audit-report.md` | Outcome-blind result: primary FAIL but closest of any mechanism test — H1/order/edge/hapax pass cleanly, units 16/20, only H2 fails universally |
| `docs/assets/external-frequency-novelty-null-h2.svg` | Public chart: frequency-weighted novelty roughly halves H2 damage vs. uniform substitution, doesn't close it |
| `logs/2026-09-20-claude-frequency-novelty-selfreview.md` | Solo design + self-review: caught and fixed a search-thoroughness confound; nu pilot calibration |
| `logs/2026-09-20-claude-frequency-novelty-null-execution.md` | Execution log and result summary |
| `data/external/bigram-novelty-null-manifest-v1.json` | Frozen manifest: frequency-novelty-null with unigram substitution replaced by bigram-conditional novelty; pilot-calibrated nu |
| `data/scripts/external_bigram_novelty_null_audit.py` | Executes the bigram-novelty-null protocol: pilot mode + full sweep, reusing baseline/edge_only by reference |
| `data/derived/external-bigram-novelty-null-audit-summary.json` | Full per-replicate and aggregate results for the 50 executed replicates |
| `data/derived/external-bigram-novelty-null-audit-report.md` | Outcome-blind result: primary FAIL, units improves to 19/20, H2 closes in a majority of seeds at half dosage — reframes the open question as substitution rate, not rule choice |
| `docs/assets/external-bigram-novelty-null-h2.svg` | Public chart comparing H2 across uniform/unigram/bigram substitution statistics |
| `logs/2026-09-21-claude-bigram-novelty-selfreview.md` | Solo design + self-review; nu pilot calibration |
| `logs/2026-09-21-claude-bigram-novelty-null-execution.md` | Execution log and result summary |
| `data/external/budget-capped-novelty-null-manifest-v1.json` | Frozen manifest testing event-placement (front-loaded budget vs. spread probability); includes an explicit honesty precommitment |
| `data/scripts/external_budget_capped_novelty_null_audit.py` | Executes the budget-capped-novelty-null protocol |
| `data/derived/external-budget-capped-novelty-null-audit-summary.json` | Full per-replicate and aggregate results |
| `data/derived/external-budget-capped-novelty-null-audit-report.md` | Outcome-blind result: negative finding — front-loading is worse for H2 than spreading, at matched or lower dosage |
| `docs/assets/external-budget-capped-novelty-null-h2.svg` | Public chart: front-loaded budget vs. spread nu-gating at matched dosage |
| `logs/2026-09-21-claude-budget-capped-novelty-selfreview.md` | Solo design + self-review, including the honesty precommitment; B pilot calibration |
| `logs/2026-09-21-claude-budget-capped-novelty-null-execution.md` | Execution log and negative-result summary |
| `data/external/move-reuse-novelty-null-manifest-v1.json` | Frozen manifest testing cached-move reuse vs. fresh bigram-conditional search; includes an honesty precommitment |
| `data/scripts/external_move_reuse_novelty_null_audit.py` | Executes the move-reuse-novelty-null protocol |
| `data/derived/external-move-reuse-novelty-null-audit-summary.json` | Full per-replicate and aggregate results |
| `data/derived/external-move-reuse-novelty-null-audit-report.md` | Outcome-blind result: negative finding — cached move reuse is worse than fresh search for H2 and units, at matched dosage |
| `docs/assets/external-move-reuse-novelty-null-h2.svg` | Public chart: fresh bigram search vs. cached move-reuse at matched dosage |
| `logs/2026-09-21-claude-move-reuse-novelty-selfreview.md` | Solo design + self-review, including two rejected naive "reuse" formulations; nu pilot calibration |
| `logs/2026-09-21-claude-move-reuse-novelty-null-execution.md` | Execution log and negative-result summary |
| `data/external/boundary-shift-novelty-null-manifest-v1.json` | Frozen manifest testing a non-substitution mechanism (moves token boundaries instead of substituting characters); documents a calibration failure |
| `data/scripts/external_boundary_shift_novelty_null_audit.py` | Executes the boundary-shift-novelty-null protocol |
| `data/derived/external-boundary-shift-novelty-null-audit-summary.json` | Full per-replicate and aggregate results |
| `data/derived/external-boundary-shift-novelty-null-audit-report.md` | Outcome-blind result: INVALID_CONSTRUCTION, but H1/H2 are exactly invariant (a first) and 5/6 criteria pass jointly in every replicate, failing only order |
| `docs/assets/external-boundary-shift-novelty-null-criteria.svg` | Public chart of per-criterion pass counts for the primary configuration |
| `logs/2026-09-21-claude-boundary-shift-novelty-selfreview.md` | Solo design + self-review, including the pilot's calibration-failure diagnosis |
| `logs/2026-09-21-claude-boundary-shift-novelty-null-execution.md` | Execution log and result summary |
| `data/external/hybrid-shift-substitution-novelty-null-manifest-v1.json` | Frozen manifest combining boundary-shift (free) with a small substitution top-up |
| `data/scripts/external_hybrid_shift_substitution_novelty_null_audit.py` | Executes the hybrid protocol |
| `data/derived/external-hybrid-shift-substitution-novelty-null-audit-summary.json` | Full per-replicate and aggregate results |
| `data/derived/external-hybrid-shift-substitution-novelty-null-audit-report.md` | Outcome-blind result: INVALID_CONSTRUCTION (close calibration miss), but H1/H2/edge/hapax all pass 20/20 at primary -- order is now the sole persistent wall |
| `docs/assets/external-hybrid-shift-substitution-novelty-null-criteria.svg` | Public chart of per-criterion pass counts for the primary configuration |
| `logs/2026-09-21-claude-hybrid-shift-substitution-selfreview.md` | Solo design + self-review, including the precommitment not to retune nu_sub after seeing outcomes |
| `logs/2026-09-21-claude-hybrid-shift-substitution-execution.md` | Execution log and result summary |
| `data/external/boundary-shift-v2-novelty-null-manifest-v1.json` | Frozen manifest fixing the order-share problem (exactly-one-new-type split preference), diagnosed by reading the actual scoring code |
| `data/scripts/external_boundary_shift_v2_novelty_null_audit.py` | Executes the boundary-shift-v2 protocol |
| `data/derived/external-boundary-shift-v2-novelty-null-audit-summary.json` | Full per-replicate and aggregate results |
| `data/derived/external-boundary-shift-v2-novelty-null-audit-report.md` | **First joint six-criterion PASS in this project.** A constructive null, not a decipherment — read the interpretation section before drawing conclusions |
| `docs/assets/external-boundary-shift-v2-novelty-null-criteria.svg` | Public chart: all six criteria pass in every replicate |
| `logs/2026-09-21-claude-boundary-shift-v2-selfreview.md` | Solo design + self-review, including the diagnosed order-share mechanism and the reuse-feedback dynamic |
| `logs/2026-09-21-claude-boundary-shift-v2-execution.md` | Execution log, verification steps performed, and careful interpretation |
| `data/scripts/external_currier_ab_diagnostic.py` | Diagnostic: does a six-criterion-passing mechanism also reproduce Voynich's real Currier A/B pooled-entropy asymmetry when split by the real line labels |
| `data/derived/external-currier-ab-diagnostic-summary.json` | Real vs. generated A/B entropy values per replicate |
| `data/derived/external-currier-ab-diagnostic-report.md` | Result: real gap +0.278 bits; boundary-shift-v2 generated gap ~0 (mean -0.0029) — concrete evidence the six criteria miss a real structural property |
| `logs/2026-09-21-claude-currier-ab-diagnostic.md` | Diagnostic log |
| `data/scripts/external_currier_ab_construction_diagnostic.py` | Diagnostic: can section-varying dosage (per-token nu by Currier A/B label) construct the real A/B asymmetry at all |
| `data/derived/external-currier-ab-construction-diagnostic-summary.json` | Per-replicate A/B entropy and gap values |
| `data/derived/external-currier-ab-construction-diagnostic-report.md` | Result: primary dosage (reused unchanged from an unrelated prior design) reaches 38.3% of the real +0.278-bit gap; a frozen wider-separation follow-up (nu_A=0.5, nu_B=0.0, round-number extrapolation) reaches 111.4% — dosage separation scales past the real magnitude rather than saturating below it |
| `data/derived/external-currier-ab-construction-diagnostic-wide-summary.json` | Per-replicate results for the wider-separation follow-up |
| `logs/2026-09-21-claude-currier-ab-construction-diagnostic.md` | Design reasoning (why boundary-shift-v2 was rejected as the base), non-circularity discipline, and execution log |
| `logs/2026-09-21-claude-section-aware-six-criterion-reasoning.md` | Reasoning: why a section-aware six-criterion attempt wasn't tractable yet, and the corrected insight (reading the actual hybrid code) that its order-share failure could reuse an already-validated fix |
| `data/external/hybrid-shift-v2-substitution-novelty-null-manifest-v1.json` | Frozen manifest: swap hybrid's boundary-shift component for the already-validated v2 split rule, keep the substitution top-up unchanged |
| `data/scripts/external_hybrid_shift_v2_substitution_novelty_null_audit.py` | Executes the protocol; diffed against the original hybrid script to confirm only the split-rule changed |
| `data/derived/external-hybrid-shift-v2-substitution-novelty-null-audit-summary.json` | Full per-replicate and aggregate results |
| `data/derived/external-hybrid-shift-v2-substitution-novelty-null-audit-report.md` | Result: FAIL, but cleanly isolated — the v2 fix partially worked (order-share moves from a wide guaranteed failure to right at the boundary once coupling is removed). **Corrected same day**: the residual failure is a coupling×novelty *interaction*, not an independent coupling main effect (coupling alone is harmless to this criterion) — see the report's correction addendum |
| `logs/2026-09-22-claude-hybrid-shift-v2-substitution-selfreview.md` | Self-review, including the pilot's disclosed deviation from the literal calibration band (hapax saturates far above the target at every tested dosage) |
| `logs/2026-09-22-claude-hybrid-shift-v2-substitution-execution.md` | Execution log |
| `data/scripts/external_coupling_order_concentration_diagnostic.py` | Diagnostic: does order-share excess concentrate in pairs where the next token's first char is a coupling-target initial (proxy hypothesis) |
| `data/derived/external-coupling-order-concentration-diagnostic-report.md` | Result: not confirmed — coupling-initial pairs show LOWER predictability than other pairs; the proxy (grouping by letter) was flawed |
| `logs/2026-09-21-claude-coupling-order-interaction-reasoning.md` | Reasoning: the TARGET_INITIALS 4-way collapse mechanism and why order-share only becomes measurable once vocabulary opens |
| `data/scripts/external_frozen_mechanisms_zipf_levenshtein_check.py` | Criterion-(b) check: do already-frozen mechanisms reproduce two already-existing, unrelated-purpose statistics (Zipf slope, Levenshtein-neighbor excess) |
| `data/derived/external-frozen-mechanisms-zipf-levenshtein-check-report.md` | Result: boundary-shift-v2 unpromptedly matches the Zipf slope; neither mechanism reproduces the Levenshtein-neighbor excess |
| `logs/2026-09-22-claude-criterion-b-precommitment.md` | Precommitment written before running the frozen-mechanisms check, explaining why it avoids the statistic-naming trap |
| `data/scripts/external_frozen_mechanisms_wordlength_levenshtein_extension.py` | Extension: word-length mean/stdev and Levenshtein≤1/identical excess against the same two frozen mechanisms |
| `data/derived/external-frozen-mechanisms-wordlength-levenshtein-extension-report.md` | Result: no new match; both mechanisms overshoot word length, and the Levenshtein-neighbor miss generalizes to ≤1 (not just ≤2) — includes a caught representation discrepancy in the real-Voynich word-length reference |
| `logs/2026-09-22-claude-criterion-b-extension-precommitment.md` | Precommitment for the extension, before running |
| `data/scripts/external_frozen_mechanisms_bpe_curve_shape_check.py` | Criterion-(b) check: full BPE dependence-gap curve SHAPE (10 checkpoints), not just the two the six criteria constrain |
| `data/derived/external-frozen-mechanisms-bpe-curve-shape-check-report.md` | Result: boundary-shift-v2 tracks the real curve's shape ~40% more closely than hybrid-shift-v2-substitution, incl. a near-exact match at k=512 — second criterion-(b) statistic (after Zipf slope) favoring boundary-shift-v2. Also discloses a methodology-level mismatch between this pipeline's own reproduced real-Voynich curve and the externally-published reference curve |
| `logs/2026-09-22-claude-bpe-curve-shape-precommitment.md` | Precommitment for the curve-shape check, before running |
| `data/scripts/external_coupling_causal_concentration_diagnostic.py` | Diagnostic: tracks coupling's actual firing event (not the resulting letter) and re-tests the concentration hypothesis directly |
| `data/derived/external-coupling-causal-concentration-diagnostic-report.md` | Result: confirmed — pairs where coupling fired show substantially higher MI (2.692 vs 2.223 bits); the earlier letter-based proxy was the flaw, not the hypothesis |
| `logs/2026-09-22-claude-coupling-causal-concentration.md` | Log: resolves the mechanism question left open since PR #40's interaction correction |
| `data/scripts/external_position0_unprotect_diagnostic.py` | Diagnostic: does widening the substitution top-up's eligible positions to include position 0 reduce order-share |
| `data/derived/external-position0-unprotect-diagnostic-report.md` | Result: right direction, insufficient magnitude (0.0234→0.0227) — position 0 eligible but rarely chosen in a uniform scan |
| `data/external/hybrid-shift-v2-substitution-position0-priority-manifest-v1.json` | Frozen manifest: prioritize position 0 in the substitution top-up rather than merely allowing it |
| `data/scripts/external_hybrid_shift_v2_substitution_position0_priority_audit.py` | Executes the protocol; diffed against the base hybrid-shift-v2-substitution script to confirm only the position-selection logic changed |
| `data/derived/external-hybrid-shift-v2-substitution-position0-priority-audit-summary.json` | Full per-replicate and aggregate results |
| `data/derived/external-hybrid-shift-v2-substitution-position0-priority-audit-report.md` | Result: FAIL, but a controlled intervention that confirms coupling's causal role directly — hybrid_novelty_only improves substantially (7/20→12/20), primary barely moves (still 0/20), exactly as the causal mechanism predicts |
| `logs/2026-09-22-claude-position0-priority-selfreview.md` | Self-review, pilot calibration, and full-run result |

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
