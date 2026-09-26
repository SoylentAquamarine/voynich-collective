# Index

A flat file list for any external agent (ChatGPT, a local model, etc.) picking up this repo cold. Start with `README.md`, then `knowledge-base/state.md` for current status, then the relevant `agents/*.md` for whichever role you're acting as.

| File | Purpose |
|---|---|
| `README.md` | Project overview: goal, how the process works, current status |
| `INDEX.md` | This file |
| `CONTRIBUTING.md` | How an additional AI contributor (and its operator) joins the project: the Guest → Registered process and a ready-to-use starter instruction |
| `LICENSE` | MIT license for this repo's own code/analysis; does not cover separately-attributed third-party material |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR checklist reinforcing the project's disclosure/falsification standard for new contributors |
| `comms/FromGuestsToClaude.md` | Shared introduction channel for contributors at the Guest stage, before they have a dedicated comms pair |
| `comms/meetings/2026-09-22-steering-committee-07.md` | Decision to open the project to additional AI contributors: the Guest → Registered pipeline, how their work is routed, repo public/license prep |
| `comms/meetings/2026-09-23-steering-committee-08.md` | User-directed standing agenda change: every meeting now includes an explicit efficiency check (wasted-cycle audit + one testable process experiment), applied immediately to this session's three deferred mechanism-design threads |
| `config/README.md` | How project-specific Claude/ChatGPT operating configurations are stored and reviewed |
| `procedures/README.md` | Step-by-step checklists for repeated tasks where skipping a step causes a real problem — distinct from `methods/` (evidentiary standards) and `config/` (operating configuration) |
| `procedures/webpage-publishing.md` | What must stay synchronized between `knowledge-base/state.md`'s Confirmed Findings and the public `docs/` site, and the exact steps to check and fix it — written after three real findings went missing from the site on 2026-09-23 |
| `procedures/index-maintenance.md` | Standing rule and a verification command for keeping `INDEX.md` itself synchronized with new files added to the repo — the verification command's first draft (diff-only) was caught missing untracked new files, including this file itself, while writing it |
| `procedures/pr-review-sweep.md` | Checking for open PRs on the routine track by the full list, not just the most recently pushed one — written after PR #58 sat unmerged for ~10 hours because of exactly that mistake |
| `procedures/precommitment-decision-rules.md` | Writing a test's pass/fail logic so a reserved judgment call can't be silently collapsed into one naive boolean — written after a near-miss where SQ-2's illustration-class script would have auto-reported a false "CANDIDATE SIGNAL" |
| `procedures/sidequest-status-sync.md` | Keeping each sidequest's own status note in `config/sidequests.md` current when real work happens on it — written after SQ-3 was found with no status note at all despite substantial progress that session |
| `config/research-department.md` | Shared mission, department structure, translation ladder, laptop compute policy, and evolution loop |
| `config/claude.md` | Claude's lead-manager configuration — accepted with one narrowing (compute policy scoped to what Steering Committee Meeting #5 actually approved); includes Claude's truthful self-description |
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
| `data/scripts/label_atlas_inventory.py` | SQ-1 pilot: deterministic text-side inventory of all 299 Lz (zodiac-figure) label loci across 12 folios |
| `data/derived/label-atlas-lz-pilot.csv` | Full per-locus inventory: folio, descriptor, clock, normalized word, quire/hand/illustration, image availability |
| `data/derived/label-atlas-lz-pilot-summary.json` | Machine-readable summary stats, independently matching ChatGPT's Round 32 feasibility numbers exactly |
| `data/derived/label-atlas-lz-missing-images.json` | Explicit image-availability gate: only 1 of 12 folios has even a candidate (unconfirmed) local scan |
| `data/derived/label-atlas-lz-pilot-report.md` | Report: independent verification table, the confirmed `&Lz`/`@Lz` parser trap, and the image-availability blocker |
| `data/scripts/label_atlas_clock_signal.py` | SQ-1 pilot: independent reimplementation of the leave-one-folio-out clock-position null test |
| `data/derived/label-atlas-lz-clock-signal.json` | Full permutation-null result |
| `data/derived/label-atlas-lz-clock-signal-report.md` | Result: no absolute-position signal (matches ChatGPT's Round 33 exploratory result almost exactly) — clock values stay geometric metadata only |
| `logs/2026-09-22-claude-lz-relative-order-precommitment.md` | Precommitment for the relative labelling-order follow-up, before running |
| `data/scripts/label_atlas_lz_relative_order.py` | SQ-1 follow-up: leave-one-folio-out test of relative labelling-order rank (not clock time) as a recurrence predictor |
| `data/derived/label-atlas-lz-relative-order-signal-report.md` | Result: also null (p=0.28) — two independent axes (clock value, labelling order) both show no positional signal from exact word recurrence |
| `data/external/yale-iiif-manifest-raw.json` | Checksum-pinned raw IIIF manifest from the official Yale/Beinecke digitization of Beinecke MS 408 (213 canvases) |
| `data/scripts/build_yale_iiif_folio_index.py` | Normalizes the raw manifest into a folio → official image URL index; resolves known duplicate/composite foldout labels with disclosed visual evidence |
| `data/external/yale-iiif-folio-index.json` | The resulting folio → image index: 205 of 213 canvases resolved to a specific folio |
| `data/derived/yale-iiif-folio-index-report.md` | Report: unblocks SQ-1's image-availability gate (all 12 Lz folios now have an image) and corrects a real error — `f70v.jpg` is f70v1 (Aries), not f70v2 (Pisces) as previously hedged |
| `logs/2026-09-22-claude-f70v-panel-resolved.md` | Log: how the f70v1/f70v2 identity was definitively resolved, superseding the earlier honest-limits attempt |
| `data/derived/label-atlas-lz-image-verification.md` | SQ-1's "five manually verified examples" deliverable: f70v1, f70v2, f71r, f72v1, f73r checked against their official Yale images — folio identity, sign, and ring-figure count all confirmed |
| `data/derived/boundary-shift-historical-plausibility-review.md` | Literature review: real medieval word-division was demonstrably unreliable independent of any cipher, and the already-tested Naibbe cipher documents period resegmentation-before-substitution — narrows (does not close) the project's open question of what independent evidence a genuine mechanism needs beyond the six-criterion numeric profile |
| `logs/2026-09-22-claude-mechanism-design-and-ring-feature-deferred.md` | Log: why a Naibbe-grounded boundary mechanism, a text-only SQ-2 ring feature, and (2026-09-23 follow-up) a per-locus image-based SQ-2 feature were each investigated and deliberately not started (none could be done without overclaiming or an unverifiable pairing) |
| `data/derived/coupling-mechanism-historical-plausibility-review.md` | Literature review: sandhi (word-boundary phonological assimilation) is a real, well-documented linguistic phenomenon — some historical orthographies (Sanskrit) write it directly into the text — supplying the first non-cipher historical/linguistic candidate source for the "coupling" mechanism's cross-token dependency. **2026-09-23 follow-up**: Tamil's written external-sandhi glide-insertion rule (binary y/v classification of the preceding word's final vowel) is the best cardinality fit found across three candidates (Sanskrit too large, Arabic tajwid wrong category, Tamil's 2-output rule fits within Voynichese's 3-symbol vowel-like class with minimal compression) — not yet used to design an actual test |
| `logs/2026-09-23-claude-tamil-mechanism-design-blocked.md` | Attempted to design an actual Tamil-grounded coupling mechanism and found a real, deeper blocker: no principled, non-circular way to assign Voynichese's 3 undifferentiated vowel-like symbols to Tamil's 2 glide classes (the EVA `y`-glyph/Tamil-y-glide naming coincidence is explicitly rejected as a basis for the split) — the cardinality-fit finding stands, but the mechanism design does not proceed without either new evidence or a disclosed arbitrary choice |
| `data/derived/sq3-source-discovery-candidates.md` | SQ-3 source discovery: continuous-prose candidates (Beinecke MS 985), and a fully usable documented cipher (Domnina 2018's reconstructed 81-sign Nicodemo Tranchedini nomenclator, 1449 Sforza chancellery) — not yet a frozen manifest, but the cipher-transformation gap is now closed |
| `data/derived/herbal-composite-plant-theory-review.md` | Historian-role literature review: is there real support for Voynich herbal plants being composite/grafted from multiple species? A general "copy-of-a-copy" degradation pattern is documented for medieval herbals broadly; the two named specific Voynich identification attempts (Sherwood, Tucker & Talbert) both exist but are significantly criticized on methodological grounds (color-based reasoning undermined by later-added paint, confirmation bias, an accompanying Nahuatl claim called "pseudo-rigorous") — names the pitfalls to avoid before this project attempts its own analysis, not yet started |
| `data/scripts/paragraph_line_position_signal.py` | First test of positional structure in ordinary paragraph text (not just labels): parses `data/ZL3b-n.txt` directly, preserving IVTFF `<%>`/`<$>` paragraph-boundary markers the existing normalized corpus strips |
| `data/derived/paragraph-line-position-signal-report.md` | Result: closely reproduces a long-reported peculiarity (Currier 1976; Feaster CEUR-WS Vol-3313) — 54.39% of Quire 20 paragraphs start with EVA `p` (published 55.14%), a 53.3x enrichment over baseline (published ~55x); every figure independently computed within a fraction of a percentage point of the published numbers |
| `data/scripts/label_atlas_full_inventory.py` | SQ-1 scale-up: full label-locus inventory, all subtypes (not just Lz), joined to page illustration class |
| `data/derived/label-atlas-full-pilot.csv` | 1,029 label loci across all 57 labelled folios — exact independent match to ChatGPT's Round 32 figure, 0 unmatched |
| `data/derived/label-atlas-full-pilot-summary.json` | Machine-readable subtype and illustration-class distributions for the full label inventory |
| `data/derived/label-atlas-full-pilot-report.md` | Report: illustration-class breakdown (299 Zodiac, 234 Pharmaceutical, ... 32 Herbal label loci), motivates the SQ-2 precommitment below |
| `logs/2026-09-22-claude-sq2-illustration-class-precommitment.md` | Frozen SQ-2 test design (not yet executed): does label word-family predict illustration class on held-out folios, vs. frequency-matched and shuffled controls |
| `data/scripts/label_atlas_illustration_class_signal.py` | Executes the frozen SQ-2 precommitment: leave-one-folio-out family-vote prediction, frequency baseline, 10,000-permutation null |
| `data/derived/label-atlas-illustration-class-signal.json` | Full machine-readable result: primary (3-char) and sensitivity (2-char) accuracy, baselines, null distributions |
| `data/derived/label-atlas-illustration-class-signal-report.md` | Result: NULL — clears a naive p≤0.05 check but the margin over baseline is small and the 2-char sensitivity check does not confirm it; reported honestly as a third null in the label-recurrence line, not waved through on a technicality |
| `comms/meetings/2026-09-23-steering-committee-09.md` | Meeting #9: re-raises and decides Meeting #6's deferred coupling-granularity question (adopts a new, separately-labeled `coupling-v2` track alongside the frozen original coupling rule, rather than replacing or indefinitely deferring it); also adds a standing process fix — after 3-4 consecutive no-op loop ticks, sweep meeting action-item tables for a shelved decision before defaulting to another plain no-op |
| `comms/meetings/2026-09-23-steering-committee-10.md` | Meeting #10: user-directed standing agenda change — every meeting now includes a mandatory "Procedure check" (does this cycle warrant a new or updated `procedures/` entry), checked autonomously without the user needing to ask each time; applied immediately (first use: nothing new to add this cycle, checked concretely) |
| `comms/meetings/2026-09-23-steering-committee-11.md` | Meeting #11: designs the two-tier (all-seven-every-cycle / rotating-depth) protocol for ChatGPT to operate across this project and its six new siblings once it resumes on a 3-hour cadence after ~75 hours away; first cycle back is orientation-only, no project ever gates Claude's own continuing work |
| `config/sibling-projects.md` | Durable cross-project reference for ChatGPT: all seven sibling repo URLs, the two-tier cadence and fixed visiting order from Meeting #11, and each project's current single-most-actionable next step as of 2026-09-23. Opens with a note (added same day, Round 92) that the two-tier cadence is calibrated for ChatGPT specifically — the separate Claude Cloud Code routine makes real progress on all seven every cycle regardless |
| `logs/2026-09-23-claude-coupling-v2-selfreview.md` | Design reasoning for coupling-v2: replaces the 4-way `TARGET_INITIALS` lookup (PR #44's diagnosed cause of hybrid-shift-v2-substitution's order-share failure) with a maximally-wide identity mapping (`target = prev_last`, 26 distinct targets, zero concentration by construction) — the single most decisive test of the concentration hypothesis, chosen over an ambiguous intermediate width |
| `data/external/hybrid-shift-coupling-v2-substitution-novelty-null-manifest-v1.json` | Frozen manifest: re-derives `hybrid-shift-v2-substitution` under coupling-v2; reuses the same 20 seeds for a clean single-variable comparison; `edge_only` explicitly recomputed fresh (not reused) since it measures coupling's own contribution; `nu_sub` recalibrated via the same pilot procedure, not carried over |
| `data/scripts/external_hybrid_shift_coupling_v2_substitution_novelty_null_audit.py` | Executes the coupling-v2 protocol |
| `data/derived/external-hybrid-shift-coupling-v2-substitution-novelty-null-audit-summary.json` | Full per-replicate and aggregate results for all 75 executed replicates (baseline reused by reference; edge_only, primary, hybrid_novelty_only, and two sensitivities computed fresh) |
| `data/derived/external-hybrid-shift-coupling-v2-substitution-novelty-null-audit-report.md` | Result: **PASS** — the project's second full six-criterion pass, directly confirming PR #44's causal diagnosis (order-share resolves once coupling's target concentration is removed); read the caveats section before drawing conclusions — H2 passes only barely and edge gain overshoots Voynich's real value by ~6-7× |
| `logs/2026-09-23-claude-section-aware-coupling-v2-declined.md` | A section-aware (Currier A/B-varying dosage) extension of coupling-v2 was checked and honestly declined, with numbers: doubling `nu_sub` from the calibrated 0.01 already breaches H2's ceiling in 1/5 replicates in data already collected, since coupling itself (not the substitution top-up) consumes nearly all of H2's headroom |
| `logs/2026-09-23-claude-coupling-v3-lower-beta-selfreview.md` | Design reasoning for coupling-v3: resolves the fork named in the declined-extension log above by taking option (a) first — a lower, fixed, uniform `beta` (not yet section-varying) — since coupling itself already consumes nearly all of H2's headroom at `beta=0.5`; decided solo, same precedent as Meeting #9, since ChatGPT remains unresponsive and the item was explicitly parked waiting on exactly this |
| `data/external/coupling-v3-lower-beta-hybrid-manifest-v1.json` | Frozen preregistration: a 5-value `beta` pilot grid (0.10-0.35) to find the lowest beta clearing the edge criterion, then a 20-seed primary run testing whether that beta passes all six criteria with strictly more H2 headroom than coupling-v2's own 0.0083-bit margin. **Not yet executed** — no `voynich-units` clone was available in the session that froze it |
| `data/scripts/external_coupling_v3_lower_beta_pilot_and_primary_audit.py` | Executes the coupling-v3 protocol (`--pilot` for the calibration grid, `--beta VALUE` for the full primary run); adapted directly from the verified coupling-v2 script with `beta` parameterized; syntax-checked but not yet run against real data |
| `data/external/coupling-v3-1-corrected-selection-manifest-v1.json` | Frozen preregistration for coupling-v3.1: corrects coupling-v3's selection defect by selecting beta on coupling's isolated `edge_only` contribution instead of the combined mechanism's gain |
| `data/scripts/external_coupling_v3_1_corrected_selection_audit.py` | Executes the coupling-v3.1 protocol (`--pilot` / `--beta VALUE`); result: PASS, validly attributed, beta=0.15, H2 headroom 3.7x coupling-v2's own |
| `logs/2026-09-25-claude-coupling-v3-1-selfreview.md` | Design reasoning for coupling-v3.1, written before any code ran that cycle |
| `logs/2026-09-25-claude-coupling-v3-1-execution.md` | Execution log for coupling-v3.1's pilot and primary runs |
| `logs/2026-09-25-claude-section-aware-coupling-v3-1-selfreview.md` | Design reasoning, written before any code ran, for the section-aware extension of coupling-v3.1 (dosage values reused unchanged from coupling-v2's own sensitivity grid) |
| `data/scripts/external_coupling_v3_1_section_aware_diagnostic.py` | Diagnostic: does section-varying coupling-v3.1's substitution dosage construct the real Currier A/B entropy gap? Result: negative, wrong-signed |
| `data/derived/external-coupling-v3-1-section-aware-diagnostic-report.md` | Result writeup: mean generated gap -0.0178 bits vs. real +0.2780 bits — opposite sign, ~6.4% of magnitude |
| `logs/2026-09-25-claude-section-aware-coupling-v3-1-reversed-selfreview.md` | Design reasoning, written before any code ran, for the reversed-assignment follow-up (same two dosage values, sections swapped) |
| `data/scripts/external_coupling_v3_1_section_aware_reversed_diagnostic.py` | Diagnostic: reversed-assignment follow-up to the section-aware coupling-v3.1 test. Result: still negative, more negative than the first attempt |
| `data/derived/external-coupling-v3-1-section-aware-reversed-diagnostic-report.md` | Result writeup: mean generated gap -0.0240 bits vs. real +0.2780 bits — falsifies the first attempt's own causal explanation; both dosage assignments now exhausted |
| `methods/coupling-v2-section-aware-preregistration.md` | Frozen preregistration (Claude Cloud Code, 2026-09-25): section-aware six-criterion attempt on coupling-v2's own beta=0.5 base |
| `logs/2026-09-25-claude-coupling-v2-section-aware-execution.md` | Execution notes for the already-frozen coupling-v2 preregistration, incl. the anchor-check threshold fixed before any output existed |
| `data/scripts/external_coupling_v2_section_aware_preregistered.py` | Executes the coupling-v2 section-aware preregistration (`--pilot` / `--primary --nu-sub-a X --nu-sub-b Y`). Result: NO_QUALIFYING_PILOT_PAIR, primary not run |
| `data/derived/external-coupling-v2-section-aware-pilot-report.md` | Result writeup: best pilot pair reaches only 4.8% of the real gap and fails six criteria; opposite qualitative trend from the coupling-v3.1 attempts |
| `data/scripts/external_currier_ab_length_repetition_stats.py` | Computes real Currier A/B mean line length and repetition rate directly from the corpus; descriptive grounding data only, no dosage design |
| `data/derived/external-currier-ab-length-repetition-stats-summary.json` | Raw output: A mean length 6.82/repetition 68.1%, B mean length 9.30/repetition 78.7% |
| `logs/2026-09-26-claude-coupling-v2-corpus-derived-dosage-selfreview.md` | Design reasoning, written before any code ran, for two corpus-statistic-derived nu_sub dosage pairs, including a predicted outcome |
| `data/scripts/external_coupling_v2_corpus_derived_dosage_check.py` | Checks the two corpus-derived dosage pairs against coupling-v2's 3 pilot seeds. Result: prediction confirmed almost exactly, ~-6% of the real gap, wrong-signed |
| `data/derived/external-coupling-v2-corpus-derived-dosage-check-report.md` | Result writeup: closes off corpus-derived nu_sub scaling as a viable lever for this mechanism family |
| `data/scripts/external_currier_ab_real_edge_gain_stats.py` | Computes real Currier A/B held-out edge-prediction gain separately (not pooled); grounding data only, no beta design |
| `data/derived/external-currier-ab-real-edge-gain-stats-summary.json` | Raw output: pooled 0.1871, A 0.1069, B 0.2381 bits/boundary — B more than double A |
| `logs/2026-09-26-claude-coupling-v2-section-varying-beta-selfreview.md` | Design reasoning, written before any code ran, for the first section-varying-beta coupling-v2 mechanism, including the fixed anchor-check threshold |
| `data/scripts/external_coupling_v2_section_varying_beta_check.py` | New apply_section_varying_coupling mechanism + generated edge-gain-gap criterion. Result: correct-signed, overshoots real gap, but anchor/manipulation check fails |
| `data/derived/external-coupling-v2-section-varying-beta-check-report.md` | Result writeup: mixed result, can't be cleanly attributed to beta since even uniform beta=0.5 shows a nonzero natural split |
| `logs/2026-09-26-claude-anchor-bias-diagnostic-selfreview.md` | Design reasoning for diagnosing the anchor bias's source (boundary-shift-v2 vs coupling itself) |
| `data/scripts/external_anchor_bias_diagnostic.py` / `_coupling_only.py` | Four-way isolation test: raw Naibbe, coupling alone, coupling+boundary-shift, full anchor |
| `data/derived/external-anchor-bias-diagnostic-report.md` | Result writeup: bias conclusively localized to boundary-shift-v2, not coupling-v2's own mechanism |

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
