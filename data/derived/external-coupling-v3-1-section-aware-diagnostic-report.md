# Section-aware coupling-v3.1 diagnostic: does not construct the real Currier A/B gap

**Correction, 2026-09-25, later cycle:** the "Interpretation" section below claims that *more* substitution dosage *lowers* a section's generated H2, and uses that to explain the wrong-signed gap. This is wrong, caught by ChatGPT's independent arithmetic check (`comms/FromChatGPTToClaude.md` Round 34), verified here against the raw JSON: paired against the reversed-assignment run (`external-coupling-v3-1-section-aware-reversed-diagnostic-summary.json`), giving a section the *stronger* dosage (0.02 vs 0.01) *increases* that section's own H2 by a small but consistently positive amount (A: +0.0028 bits mean; B: +0.0035 bits mean, both across the same 5 seeds) — the opposite of what's claimed below. The actual driver of the negative gap in this run is a baseline asymmetry present regardless of dosage assignment: B's generated H2 is higher than A's in every one of the 5 seeds under *both* dosage assignments tested (see the reversed report's own table). The original numeric result (-0.0178 bits, wrong-signed, ~6.4% of the real gap) is unaffected and still stands — only the causal story below is corrected. The rest of this document is left as originally written, including the incorrect reasoning, so the record of what was actually claimed and why is not lost; read the corrected reasoning in the reversed-assignment report's own correction note and in `knowledge-base/state.md`.

Design reasoning and honesty precommitment (written before this ran):
`logs/2026-09-25-claude-section-aware-coupling-v3-1-selfreview.md`.
Script: `data/scripts/external_coupling_v3_1_section_aware_diagnostic.py`.
Raw output: `data/derived/external-coupling-v3-1-section-aware-diagnostic-summary.json`.

## Headline result

**Negative result, wrong-signed.** Section-varying coupling-v3.1's substitution
top-up dosage (`nu_sub_A=0.02`, `nu_sub_B=0.01` — both reused unchanged from
coupling-v2's own already-executed sensitivity grid, not chosen for this test)
while holding beta (0.15) and the boundary-shift rate (1.0) fixed across both
sections produces a mean pooled character-bigram-entropy gap of **-0.0178
bits** across 5 seeds — the *opposite* sign from the real Voynich Currier A/B
gap (+0.278 bits), and only ~6.4% of its magnitude even ignoring the sign
flip.

| Seed | A_H2 (bits) | B_H2 (bits) | Gap (A−B) | % of real gap (signed) |
|---:|---:|---:|---:|---:|
| 42 | 2.2306 | 2.2480 | -0.0175 | -6.3% |
| 179 | 2.2161 | 2.2296 | -0.0135 | -4.9% |
| 316 | 2.2288 | 2.2411 | -0.0123 | -4.4% |
| 453 | 2.2141 | 2.2396 | -0.0255 | -9.2% |
| 590 | 2.2139 | 2.2338 | -0.0200 | -7.2% |
| **Mean** | | | **-0.0178** | **-6.4%** |

Real Voynich gap (recomputed fresh as a sanity check, same method as
`external_currier_ab_diagnostic.py`): **+0.2780 bits**, matching the
previously reported figure exactly.

## Interpretation

This closes off, for this specific mechanism and this specific already-frozen
dosage pair, the possibility that coupling-v3.1's larger H2 headroom (3.7x
coupling-v2's own) translates into an ability to construct the real Currier
A/B asymmetry via section-varying substitution dosage alone. Assigning the
*stronger* substitution dosage to Currier A (the section with the *higher*
real bigram-conditional entropy) produced *lower* generated entropy for A
than B — backwards from what would be needed. This is directionally
consistent with how substitution-driven novelty generally interacts with
bigram entropy in this project's whole novelty-rule sequence (see
`knowledge-base/state.md`'s five-design substitution-novelty synthesis):
*more* substitution activity tends to *lower*, not raise, a section's H2,
because each successful substitution search actively seeks a bigram-favored
replacement. Naively assigning "more dosage" to the section that needs
*higher* entropy was, in hindsight, working against the mechanism's own
known behavior — but this was not known to bear on section assignment
specifically until this test ran, and the assignment itself was disclosed as
arbitrary before the result existed, per the self-review log.

**What this does and does not show:** this is one disclosed configuration
(one dosage pair, one fixed beta, one arbitrary section assignment), not an
exhaustive search of the parameter space, and per the precommitment it is
not retried with a different pairing or assignment without a fresh
precommitment. It does not show that no configuration of this mechanism
family could ever construct the real gap — only that this specific,
non-circularly-chosen one does not, and does not even point in the right
direction. Unlike the bigram-novelty-null base mechanism tested in PR #39
(38–111% of the real gap, correct sign), coupling-v3.1's own family has now
been tested on this question once, honestly, and come back negative.

**Does not bear on coupling-v3.1's own already-established result** (six-
criterion PASS, validly attributed, reported earlier this cycle) — that
result concerned the pooled, non-section-split profile and is unchanged.
**Does not identify a mechanism or bear on the manuscript's actual origin**,
per every other constructive-null result in this project's history.

## What remains open

Whether *reversing* the section assignment (weaker dosage to A) would perform
any better is a live, named, untested question — but testing it now, after
seeing this result go the wrong way, would be exactly the outcome-directed
re-selection this project's precommitment discipline exists to prevent. It
stays open, unattempted, for a future cycle with its own fresh
precommitment, not chased here.
