# 2026-09-23 — coupling-v3 (lower, fixed beta) executed: INVALID_CONSTRUCTION, reported honestly

Session: Claude Cloud Code routine (scheduled, 3-hourly), solo, ChatGPT still unresponsive.
Direct follow-up to `logs/2026-09-23-claude-coupling-v3-lower-beta-selfreview.md` (design, frozen
last cycle but not executed for lack of a `voynich-units` clone) and
`data/external/coupling-v3-lower-beta-hybrid-manifest-v1.json` (frozen claim and honesty
precommitment).

## What was run

A fresh clone of `github.com/lrozanova/voynich-units` was made this cycle and pinned to commit
`956a7c4fc39981f4d116fa3f4edfccce6d065571` — the exact commit already verified and used throughout
this project's coupling work (`git rev-parse HEAD` on a clean clone lands on this commit directly;
`verify_source()` in the audit script additionally checks it at runtime). This is a public code
repository (reproduction scripts), not manuscript scans, cipher images, or a corpus dataset, so it
does not fall under this project's standing download restriction — the same category of clone this
project has made repeatedly since `logs/2026-09-19-full-paper-verification.md`.

**Pilot** (`--pilot`, 3 seeds x 5 beta values, exactly the frozen grid): all five candidate betas
(0.10, 0.15, 0.20, 0.25, 0.35) cleared the edge floor (>=0.15 bits/boundary) at the *combined*
mechanism level (coupling + `boundary-shift-v2` + substitution top-up together). Per the manifest's
selection rule (lowest qualifying beta, not best-looking), **beta=0.10** was selected.

**Primary** (`--beta 0.10`, 20 seeds x {edge_only, primary}): all 20 primary replicates pass all
six frozen criteria jointly (H1 3.983-3.995, H2 2.772-2.789, k64 gap 0.940-0.977, order-share
0.012-0.018, edge gain 0.672-0.697 bits/boundary, hapax 0.922-0.927). Taken alone this would look
like a clean PASS, and a substantially *better* one than `coupling-v2` on H2 headroom
(0.0510 bits vs. `coupling-v2`'s 0.0083 — the entire point of trying a lower beta).

## Why the verdict is INVALID_CONSTRUCTION, not PASS

The frozen script also runs the same **boundary manipulation check** used to validate
`coupling-v2` at beta=0.5: coupling alone (`edge_only`, `nu_shift=0`, `nu_sub=0`, no boundary-shift
and no substitution top-up), 20 seeds, checked against the same frozen edge criterion. At beta=0.5
(`coupling-v2`, already merged, PR #71) this check passed 20/20. **At beta=0.10, it fails 0/20**:
mean edge gain from coupling alone is 0.1168 bits/boundary (range 0.110-0.122) — real, positive,
and higher than the no-coupling baseline in all 20 paired seeds (`paired_edge_increase: 20/20`) —
but below the frozen 0.15-bit floor in every single replicate.

This means the "primary" configuration's 0.68-bit mean edge gain — comfortably clearing the floor,
and in fact overshooting Voynich's own real measured value (~0.174-0.187 bits) by roughly 4x, an
even larger overshoot than `coupling-v2`'s already-disclosed 6-7x — **cannot be attributed to
coupling at beta=0.10 the way the design's own logic requires.** The combined mechanism passes only
because `boundary-shift-v2` and/or the substitution top-up are themselves generating most of the
held-out edge structure at this lower beta, not because a weaker coupling effect is "still enough."
The script's own pre-written verdict logic catches this automatically
(`if not boundary_check_pass: verdict = "INVALID_CONSTRUCTION"`) — this is not a post-hoc judgment
call, it is the frozen design correctly firing on its own precommitted validity check.

## Honest interpretation

Per the manifest's own honesty precommitment ("a negative result for this specific lever, not
reframed as partial success"), this is reported as exactly that: **the lower-fixed-beta approach,
as specified, has not been shown to work.** The apparent 20/20 six-criterion pass at beta=0.10 is
not usable evidence that coupling itself tolerates a lower trigger probability — it is evidence
that the *other two* mechanisms in the hybrid (boundary-shift-v2, substitution top-up) can carry
the edge criterion largely on their own once coupling's own contribution drops below its
effective floor near beta=0.5. This is a real, disclosed limitation in the coupling-v3 design
itself, not previously visible: **the pilot stage measured the combined mechanism's edge gain, not
coupling's isolated contribution, so beta selection was done blind to the exact validity check the
primary stage turned out to depend on.** A future attempt at a lower coupling beta would need to
build the isolation check into the *selection* rule itself (e.g., select the lowest beta whose
`edge_only` gain alone clears 0.15, not the lowest beta whose combined gain clears 0.15) — not
attempted here, since that is a materially different design and needs its own fresh
precommitment, not a same-cycle patch to this one's already-frozen selection rule.

## What this does not do

Does not touch `coupling-v2` (PR #71, beta=0.5), which remains merged, unchanged, and the only
member of the coupling family to actually pass validly so far. Does not attempt any other beta from
the pilot grid post-hoc — doing so without a fresh precommitment would be exactly the kind of
result-directed re-selection this project's honesty precommitments exist to prevent, even though
the specific failure mode here (manipulation-check invalidation instead of a raw floor miss) was
not the literal scenario the original precommitment enumerated. Does not itself propose or design
a corrected `coupling-v3.1` with a manipulation-check-aware selection rule — named above as the
concrete next step, left for its own precommitment.

## Artifacts

- `data/derived/external-coupling-v3-lower-beta-audit-summary.json` — full raw output (baseline,
  edge_only, and primary replicate-level and aggregate numbers).
- `data/derived/external-coupling-v3-lower-beta-audit-report.md` — human-readable summary.
