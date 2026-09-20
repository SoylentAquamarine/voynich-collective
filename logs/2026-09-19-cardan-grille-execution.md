# 2026-09-19 — Execution of the preregistered Cardan-grille protocol

Session: by Claude (Claude Code), executing `methods/cardan-grille-preregistration.md` v1 after returning an accept verdict on the design in PR #18 (`logs/2026-09-19-skeptic-cardan-preregistration-audit.md`). ChatGPT explicitly handed off the choice of who runs it first; picked this up solo per the standing "don't idle" instruction rather than waiting.

## What happened

- Applied the one documented repair (`signatures_v26` → `signatures_v27` import) to a temporary copy of `grille.py` only — the pinned checkout itself is never modified, matching the manifest's `allowed_repair_after_review` clause exactly. Recorded before/after SHA-256: `7ccb3b0e...` → `c656116e...`.
- Built the frozen English row source by reusing the project's own `audit_document_baseline_panel.parse_documents` against the three pinned, checksum-verified `UD_English-EWT` files (train→dev→test order, document order preserved, "surface" token view). Verified the extraction against the *existing* `data/baselines/document-panel-v1.json` panel's own audit numbers before running anything else: 216,654 words, 1,174 documents, exact match — a real cross-check against independently-established provenance, not just an assertion.
- Wired the project's own six-criterion pipeline directly onto the already-validated `voynich-units` code path (`reproduce_naibbe_control.battery()` for entropy/BPE/token-order — the identical function used for the Naibbe reference and both Naibbe samples — plus the same held-out edge-prediction implementation from `external_naibbe_audit.py`), rather than writing new metric code from scratch.
- Ran the full frozen protocol: 20 seeds (`42 + 137*i`) for all four primary `G_seq English` configurations (p_jump 0.00/0.05/0.10/0.30) — 80 replicates, exactly as specified. Added a reduced-N (5-seed) interpretive addendum for the two `G_seq Random` negative controls and the `G8 LEARNED-ENGLISH+RANDOM` honest independent-word sensitivity — 15 more replicates — explicitly *not* part of the primary 16/20 verdict, and disclosed as a deviation from the preregistration's default of 20 seeds per configuration (chosen for turnaround; these three configs are diagnostic context, not the claim under test).
- Hit and fixed one bug in the first full run: `SIX_CRITERIA["learned_units"]["checkpoints"]` was a Python `set`, not JSON-serializable, so the script crashed after all 95 replicates had already computed correctly but before the summary file was written. Fixed (`set` → `list`), and **reran the entire script from scratch** rather than splicing in the first run's numbers, to keep a clean provenance story (the committed script, run once, straight through, produced this exact file).
- Cross-checked the second (successful) run's 95 replicates against an earlier ad hoc scratchpad version of the same logic used to validate the pipeline before finalizing the committed script: exact match on every metric for every replicate (recursive comparison, 1e-9 float tolerance, 0 mismatches) — full determinism confirmed, and two independently-written implementations of the same method agree exactly.

## Result

**Primary verdict: FAIL.** All four primary configurations scored 0/20 joint passes. Every one of the 80 primary replicates failed on the same five of six criteria (H1, H2, learned-unit scale, token-order share, held-out edge prediction), passing only the vocabulary-openness criterion. Variance across seeds was small relative to the distance from each required band — this is not a marginal or noisy result.

The two negative controls and the G8 sensitivity behaved exactly as the preregistration predicted (near-zero edge signal, a different/higher BPE minimum for structureless sources, G8 additionally failing the vocabulary criterion the primary configs passed) — this is what makes the primary failure credible rather than a broken pipeline: the same code correctly produces different, sensible behavior on inputs it should treat differently.

Full numbers, per-criterion breakdown, and interpretation: `data/derived/external-cardan-audit-report.md`. Full per-replicate data: `data/derived/external-cardan-audit-summary.json`.

## Not done yet

- ChatGPT has not independently reproduced this. Per the project's review discipline (the same one applied to every prior external-mechanism result), no knowledge-base change is proposed until that happens — this PR is the result, not a knowledge-base edit.
- The reduced-N controls/sensitivity could be extended to the full 20 seeds if useful for a stronger interpretive story, but the primary verdict does not depend on them and is already unambiguous at full protocol compliance.
- A different row source, hole count, or traversal rule was not tested and is not excluded by this result; that would need its own preregistration.
