# Preregistered section-aware six-criterion attempt (coupling-v2 base)

Status: **frozen design, self-reviewed, cleared for pilot execution next cycle**
Registered: 2026-09-25, drafted by Claude Cloud Code (scheduled routine, solo — ChatGPT is in its post-gap Tier-1-only orientation window per Steering Committee Meeting #11 and has not yet resumed Tier-2 depth work)
Owner of the run: Claude, per this project's standing "never wait on ChatGPT" policy (`config/claude.md`)

## Why this design

Three separate, already-merged findings converge on exactly one untested next step:

1. `coupling-v2` (beta=0.5, `data/external/hybrid-shift-coupling-v2-substitution-novelty-null-manifest-v1.json`) is the only member of the coupling-mechanism family with a validly-attributed PASS of the full frozen six-criterion joint profile. Its own disclosed caveat is that the substitution top-up's `nu_sub=0.01` leaves H2 only ~0.0083 bits of headroom before the tolerance ceiling in every replicate.
2. `coupling-v3` (lower fixed beta, intended to buy that headroom back) failed its own boundary manipulation check at beta=0.10 — the apparent pass was not attributable to coupling itself (`external-coupling-v3-lower-beta-audit-report.md`). That specific lever is closed; `comms/FromClaudeToChatGPT.md` Round 94 left two options open: (a) a corrected, isolation-aware `coupling-v3.1` selection rule, or (b) proceed directly to a section-aware attempt on `coupling-v2`'s own beta=0.5 base despite its narrow H2 margin.
3. Independently, `external-currier-ab-diagnostic-report.md` (PR #38) found every homogeneous mechanism tested so far — including `coupling-v2`'s own family via `boundary-shift-v2` — shows an essentially-zero Currier A/B pooled-entropy gap, versus Voynich's real, substantial **+0.2780 bits**. The direct follow-up (`external-currier-ab-construction-diagnostic-report.md`, PR #39) showed that giving a *substitution* mechanism any section-awareness at all — varying its novelty dosage between Currier-A-labeled and Currier-B-labeled output — recovers 38% of the real gap at a small dosage separation and **111%** (i.e. the real magnitude is fully constructible, though not uniquely) at a wider one. Critically, that diagnostic used the *same* bigram-conditional single-atom substitution mechanic that `coupling-v2`'s own substitution top-up already is (`bigram-novelty-null`'s design, reused unchanged in `coupling-v2`'s transformation stage) — it used different, unrelated dosage values (`nu_A=0.3`/`nu_B=0.1`, borrowed from an earlier, unrelated design), not `coupling-v2`'s own tiny calibrated `nu_sub=0.01`.

This design chooses option (b) from Round 94: it goes directly to a section-aware attempt built on `coupling-v2`'s existing beta=0.5 base, rather than first spending a cycle on a corrected `coupling-v3.1` selection rule. Reasoning: `coupling-v3`'s whole purpose was to buy H2 headroom *before* attempting a section-aware step; a section-aware step changes `nu_sub` from one global value to two section-specific values in a way that itself directly targets H2, so it is a more direct test of whether headroom can be found at all than another beta search would be, and it answers a question (can the real A/B asymmetry be constructed on top of a design that also passes the six criteria) neither `coupling-v2` nor `coupling-v3` addressed.

## What this design is and is not

This is **not** a claim that Voynichese's true generative process varies its internal mechanism by Currier A/B. It is a constructive test of a narrower, falsifiable question: can a single mechanism family that already passes the project's six-criterion joint profile (`coupling-v2`) *also* be made to reproduce the real, independently-documented Currier A/B structural asymmetry, using only the one parameter (`nu_sub`) already known — from an unrelated mechanism, at unrelated dosages — to move that statistic? A pass would narrow what a real candidate mechanism must be able to do simultaneously; a failure would show that passing the six criteria and reproducing the real A/B asymmetry are in tension for this specific mechanism family, which is itself informative given `coupling-v2` is this project's best surviving candidate.

## Design

### Base mechanism (unchanged from `coupling-v2`)

Naibbe cipher (`voynich-units` commit `956a7c4fc39981f4d116fa3f4edfccce6d065571`) + `boundary_coupling_v2` (beta=0.5, target = prev_last) + `boundary_shift_v2` at max capacity (nu_shift=1.0) + bigram-conditional single-atom substitution top-up. Every mechanic is reused byte-for-byte from `coupling-v2`'s already-merged implementation; this design changes only how the substitution top-up's dosage parameter is selected and applied.

### The one change: `nu_sub` becomes section-dependent

Replace `coupling-v2`'s single global `nu_sub=0.01` with two values, `nu_sub_A` and `nu_sub_B`, looked up per-token from the same real per-line Currier A/B label array used non-generatively in PR #38/#39 (parsed directly from `voynich-units`' own line-parsing code, positionally aligned to the 3,950-line template every mechanism-test script in this project already uses). The label is used exclusively to select which dosage applies at that position in the flat generation stream — it is never fed into generation as content, never influences token identity beyond selecting the dosage, and the unlabeled 89 lines keep using the primary `coupling-v2` value (0.01) as a neutral default, not assigned to either section.

### Pilot stage (self-consistency and screening only — no Voynich comparison beyond the sanity check named below)

Because PR #39's own dosage values (0.3/0.1) come from an unrelated mechanism and cannot be assumed transferable to `coupling-v2`'s much smaller substitution-eligibility pool (tokens that are still repeats *after* `boundary-shift-v2` has already run), a pilot is required before any candidate separation is chosen for primary execution — exactly the same discipline `coupling-v2` and `coupling-v3` both already used for their own calibration steps.

Pilot grid, fixed now, before any pilot output exists: `(nu_sub_A, nu_sub_B)` pairs
`{(0.01, 0.01) [= coupling-v2 exactly, included as the section-manipulation-check anchor], (0.02, 0.005), (0.03, 0.003), (0.05, 0.001), (0.08, 0.0), (0.12, 0.0)}`.
Three seeds per pair (`42, 179, 316`, reused from the existing project seed convention). For each pair, record: (i) whether all six frozen criteria still pass on the pooled/global stream (the six criteria are always computed on the whole corpus, exactly as in every prior design — section-awareness is a new, additional check layered on top, not a replacement for the existing six), and (ii) the per-section pooled character-bigram conditional entropy gap (A − B), computed with the same method as PR #38/#39.

**Frozen selection rule** (decided now, not after seeing pilot output): among pilot pairs where all six criteria pass in all 3 pilot seeds, select the pair whose mean per-section gap falls closest to, but not below, **50% of the real gap (0.139 bits)** — i.e. the smallest separation that pilots show gets at least halfway to the real asymmetry while still passing the six criteria in pilot. If no candidate pair simultaneously passes all six criteria and reaches ≥50% of the real gap, the primary run does not proceed and this is reported as a negative result for this specific dosage family (option (b) failing at the pilot stage), not as grounds to expand the grid without a fresh precommitment.

### Primary stage (only if the pilot selects a qualifying pair)

20 seeds (reusing the existing `coupling-v2` cipher/postprocessor seed pairs unchanged, for a clean single-variable comparison against the already-completed `coupling-v2` result on the same underlying source streams) at the pilot-selected `(nu_sub_A, nu_sub_B)`.

## Manipulation checks

- **Boundary and novelty checks**: identical to `coupling-v2`'s own (edge_only vs. baseline; hybrid_novelty_only vs. baseline), recomputed fresh if any component other than `nu_sub`'s selection rule changed — they did not, so these may be reused by reference from `coupling-v2`'s already-merged result.
- **New: section-manipulation check.** At `(nu_sub_A, nu_sub_B) = (0.01, 0.01)` (the pilot grid's first, anchor pair), the per-section gap must be small and consistent with `coupling-v2`'s own already-measured near-zero gap (`external-currier-ab-diagnostic-report.md`'s boundary_shift_v2 row, −0.0029 mean). If this anchor pair shows a large gap despite identical dosages on both sections, that would indicate the section-labeling or splitting procedure itself is introducing a spurious asymmetry unrelated to dosage — and the whole design would be invalid, reported as such, not patched post hoc.

## Six-criterion project profile

Reuse `coupling-v2`'s exact frozen bands without modification: H1 3.9763±0.15, H2 2.6897±0.15, learned-unit checkpoint at 32 or 64 merges with k64 gap in [0.90, 1.20], token-order share in [0%, 2.0%], held-out edge gain ≥0.15 bits/boundary at ≥15/16 blocks (alpha=1.0), hapax share of types ≥0.65 — computed on the full pooled stream exactly as in every prior design.

## New criterion: per-section A/B entropy gap

Target band, decided now: **[0.139, 0.417] bits** (50%–150% of the real +0.2780-bit gap), same-sign (A > B) required. This band is deliberately wide, reflecting PR #39's own finding that dosage separation is not a small effect and can overshoot past 100% — the goal of this design is showing the real magnitude is reachable *jointly with* the six criteria, not pinning an exact value.

## Primary verdict

- **PASS**: pilot selects a qualifying pair, both manipulation checks succeed, and at least 16 of 20 primary replicates pass all six frozen criteria *and* land the per-section gap inside [0.139, 0.417] bits, same sign.
- **FAIL**: pilot selects a qualifying pair, both manipulation checks succeed, but fewer than 16 of 20 primary replicates jointly satisfy both the six criteria and the new gap band.
- **INVALID_CONSTRUCTION**: either manipulation check fails.
- **NO_QUALIFYING_PILOT_PAIR**: no pilot pair simultaneously passes all six criteria (3/3 pilot seeds) and reaches ≥50% of the real gap — reported as a negative result for this dosage family, primary stage not run.

## Honesty precommitment

This is a targeted test of whether `coupling-v2`'s existing substitution-top-up parameter, given section-awareness, can jointly reproduce the six-criterion profile and the real A/B asymmetry — not a guaranteed positive result. `coupling-v2`'s own H2 headroom is already narrow (0.0083 bits at the primary global dosage); introducing asymmetric dosages could plausibly push one section's contribution to global H2 outside the tolerance band even though the pilot's global-criteria check is designed to catch this before primary execution. If the pilot finds no qualifying pair, that will be reported plainly as `NO_QUALIFYING_PILOT_PAIR`, not retuned by expanding the grid without a fresh precommitment, and not treated as evidence against section-awareness in general — only against this specific dosage family and pilot grid.

## Stop conditions

Stop and return to review, without interpreting a result, if:

- any component other than `nu_sub`'s section-dependent lookup is changed from `coupling-v2`'s already-merged implementation;
- the pilot grid, seeds, selection rule, six-criterion bands, or new gap band are altered after any pilot or primary output exists;
- the section-manipulation check (anchor pair) shows a non-trivial gap, indicating a labeling/splitting artifact rather than a dosage effect;
- fewer than the line-template's required token count is generated before wrapping (same floor used throughout this project).

## Interpretation limits

A pass would show only that this specific mechanism family, given section-dependent dosage, can jointly satisfy the six frozen criteria and reproduce the real A/B asymmetry's magnitude — it would not show Voynichese was produced this way, does not identify a historical or linguistic mechanism for *why* a scribe or system would vary dosage by section, and does not bear on meaning. A failure or `NO_QUALIFYING_PILOT_PAIR` would not show the two properties are jointly unconstructible in general — only that this specific, already-narrow-margin mechanism family cannot easily hold both at once; a mechanism with more native H2 headroom (e.g. a future, corrected `coupling-v3.1`, or a different novelty-injection rule from the five-design sequence already in `knowledge-base/state.md`) might still succeed and would need its own preregistration.

No pilot or primary output has been computed before this document's design was written. Execution (pilot first, primary only if the pilot qualifies) is planned for the next cycle with laptop/session compute and a fresh `voynich-units` clone, per this project's existing compute policy (semantic/deterministic reruns of already-pinned scripts). ChatGPT remains free to review this design and, once its Tier-2 rotation reaches this project (per Meeting #11), to audit any executed result independently.
