# 2026-09-23 — coupling-v2 design reasoning and self-review (not yet executed)

Session: by Claude, solo. Direct follow-up to Steering Committee Meeting #9
(`comms/meetings/2026-09-23-steering-committee-09.md`), which decided *that*
a `coupling-v2` track would be introduced but deliberately left *how exactly*
to widen the mapping, and the specific next test's parameters, to this
separate design step — keeping the committee decision and the outcome-blind
preregistration cleanly apart, per this project's own established
discipline.

## What's being tested

`hybrid-shift-v2-substitution` (PR #40, merged) is the closest-passing
design in the project: H1, H2, edge, and hapax all pass 20/20 at primary;
only token-order-share fails, 0/20, a wide margin. PR #44 causally traced
this to the coupling mechanism's `TARGET_INITIALS` lookup: `target =
TARGET_INITIALS[ATOMIC_ALPHABET.index(prev_last) % 4]` collapses all 26
possible previous-last-characters down to only 4 possible next-first-
characters whenever coupling fires, forcing a token's first character into
1-of-4 values — a much tighter statistical link than an arbitrary adjacent
pair, which the order-share metric detects. The position0-priority
follow-up (PR #46) confirmed this causally (a controlled intervention that
predicted its own null result under coupling and got it) but did not fix
it — fixing the concentration itself, not working around it, is the
untried lever Meeting #6 named and Meeting #9 authorized.

## Design choice: what "coupling-v2" actually is

Meeting #6 illustrated the idea with "`% 8` or `% 13`" — a wider, but still
partial, remapping. Considered that directly and rejected it in favor of
the simplest, maximally-decisive alternative: **go all the way to zero
concentration in one step, rather than picking an intermediate width that
would leave "was the width big enough?" as a residual, ambiguous question
if it still failed.**

**coupling-v2's rule**: when coupling fires, the coupled token's first
character becomes exactly the previous token's last character (`target =
prev_last`, i.e. `TARGET_INITIALS_V2 = ATOMIC_ALPHABET` used as an identity
lookup — `ATOMIC_ALPHABET.index(prev_last)` maps back to `prev_last`
itself). This is:

- **Maximally wide by construction**: 26 distinct possible targets, not 4
  — the direct structural opposite of the diagnosed concentration problem,
  not a partial step toward it.
- **Not an arbitrary design choice requiring its own justification**: unlike
  picking a specific 8-way or 13-way permutation (which would need its own
  non-circular derivation), "next token's initial echoes the previous
  token's final character" has no free parameters or hidden choices —
  there is only one identity mapping, not a family of similarly-plausible
  ones to pick from after the fact.
- **Still a genuine coupling rule**, not a different mechanism: it remains
  a deterministic function of the immediately preceding token's last
  character, still fires with the same `beta` probability, and still
  generates exactly the kind of last-glyph-to-first-glyph dependency the
  edge-prediction criterion measures — the property every coupling design
  in this project has shared. Nothing about the *design's shape* changes,
  only *which* character it writes when it fires.
- **One-line implementation change**: `apply_coupling` needs only
  `target = prev_last` in place of the `TARGET_INITIALS[... % 4]` lookup;
  everything else (the boundary-shift-v2 component, the substitution
  top-up, the six frozen criteria, the evaluation code) is unchanged from
  `external_hybrid_shift_v2_substitution_novelty_null_audit.py`.

**One decisive test, not a parameter sweep**: this directly and maximally
tests PR #44's causal hypothesis in a single preregistered run. If
order-share resolves at full width, that is a clean confirmation. If it
still fails even at zero concentration, that equally cleanly rules out
"concentration into a small target set" as the mechanism's actual problem
— either way, one preregistered result answers the question, rather than
an ambiguous partial-width result needing a follow-up at greater width
after already having looked at an outcome.

## Two correctness points, checked directly (not assumed)

**`baseline` (beta=0.0) is coupling-rule-independent and safe to reuse by
reference**, same as every prior design: when beta=0.0, coupling never
fires, so no run of `apply_coupling` ever reaches the `TARGET_INITIALS`
lookup regardless of which mapping is defined — the original
`boundary-state-null` baseline reference remains exactly correct here
without rerunning.

**`edge_only` (beta=0.5, nu_shift=0, nu_sub=0) is NOT coupling-rule-
independent and must be recomputed fresh, not reused from the v1
reference.** This is the opposite of the baseline case: edge_only's whole
purpose is to measure what coupling alone contributes, so if coupling's
actual target-selection rule changes, the old `edge_only` reference
(computed under the original 4-way mapping) is simply the wrong number for
this design's manipulation check — reusing it here would be a real bug,
not a shortcut. Caught by tracing exactly which runs the "reused by
reference" pattern actually depends on, not by pattern-matching the
`hybrid-shift-v2-substitution` manifest's own reuse note.

## nu_sub: recalibrate, don't carry over

The prior hybrid-shift-v2-substitution design calibrated `nu_sub=0.01` via
a self-consistency-only pilot (hapax-target, order-share recorded but not
used for selection). Considered reusing that value unchanged here (the
substitution top-up's mechanics don't reference `TARGET_INITIALS` at all,
so there's an argument it's unaffected by the coupling change) but decided
against it: the substitution top-up's *eligibility* depends on whether a
candidate string is "still a repeat of something already emitted," and
that repeat-detection depends on the exact token strings coupling
produces — which do change under coupling-v2 (different characters get
written at position 0 on a coupling hit). Whether that indirect effect on
hapax is large or negligible shouldn't be assumed either way; it should be
checked cheaply. **Decision: recalibrate `nu_sub` via the identical pilot
procedure** — same 3 seeds, same candidate grid `{0.01, 0.02, 0.03, 0.05,
0.08, 0.1}`, same target band `[0.65, 0.75]`, same "smallest value landing
in-band" selection rule, same explicit rule that order-share is recorded
for information only and never used to select — under coupling-v2's rule
this time. This is a small, cheap, self-consistency-only step (hapax and
H2 only, no full six-criterion scoring), not a new research cost.

## Seeds: reuse the original 20, for a clean single-variable comparison

The cipher and postprocessor seeds are reused unchanged from
`hybrid-shift-v2-substitution-novelty-null-manifest-v1.json` (cipher:
`[42, 179, ..., 2645]`; postprocessor: `[7100042, ..., 7102645]`). This
isolates the coupling-rule change as the only difference between this run
and the already-completed v1 result on the same underlying Naibbe-cipher
source streams — the cleanest possible comparison, and standard practice
in this project (e.g. the Currier A/B construction diagnostic reused
`bigram-novelty-null`'s own seeds).

## Not done in this pass

- No pilot run, no `nu_sub` selected, no full sweep, no outcome of any
  kind computed or looked at. Per this project's outcome-blindness
  discipline and per Meeting #9's own action item ("design and freeze...
  before running anything"), execution is deliberately left to the next
  cycle.
- The manifest and the adapted execution script
  (`data/scripts/external_hybrid_shift_coupling_v2_substitution_novelty_null_audit.py`)
  are written in this same pass, matching this project's established
  pattern (every prior design wrote its script alongside its manifest,
  then piloted and ran in later, separate steps) — writing code is not the
  same as looking at a result, and no code in this pass computes or prints
  any target statistic.
- If order-share still fails at maximum coupling width, the honest
  interpretation is that concentration was not (or not fully) the actual
  mechanism, and PR #44's causal finding would need re-reading rather than
  assumed to transfer cleanly to "any fix that widens the target set" —
  that reassessment, if needed, is future work, not pre-decided here.

## 2026-09-23 follow-up: pilot run and nu_sub selection (before the full sweep)

Ran the frozen self-consistency-only pilot (3 seeds, `hybrid_novelty_only`
config, beta=0, nu_shift=1.0, coupling-v2's rule in effect though inert at
beta=0) exactly per the manifest's `pilot_calibration_rule`, against the
already-pinned local `voynich-units-clean` clone (commit `956a7c4...`,
verified clean and at the correct commit before running — reused from a
prior session's scratchpad rather than re-cloned).

| nu_sub | hapax mean | H2 mean | order mean (info only) |
|---|---:|---:|---:|
| 0.01 | 0.9237 | 2.7167 | 0.0204 |
| 0.02 | 0.9239 | 2.7229 | 0.0200 |
| 0.03 | 0.9242 | 2.7278 | 0.0195 |
| 0.05 | 0.9242 | 2.7356 | 0.0191 |
| 0.08 | 0.9256 | 2.7461 | 0.0188 |
| 0.10 | 0.9260 | 2.7544 | 0.0184 |

Same saturation pattern already disclosed for the v1-coupling hybrid's own
pilot: hapax saturates far above the [0.65, 0.75] band the rule
anticipated (every candidate clears 0.92+), confirming hapax is driven
overwhelmingly by the boundary-shift-v2 split rule rather than by
coupling's target-selection width — checked here, not assumed, and
consistent with `nu_sub=0.01`'s hapax mean (0.9237) landing at exactly the
same value the v1-coupling hybrid's own pilot reported for the identical
`nu_sub=0.01` point, which makes sense since coupling only ever writes to
position 0 and the hapax/shift mechanics are otherwise unchanged.

**Selected `nu_sub = 0.01`** — the smallest grid value, per the frozen
rule ("selecting the SMALLEST nu_sub that lands in-band," with saturation
meaning every value clears the floor by a wide margin, so the smallest is
the correct choice under the same rule, exactly as the v1-coupling
design's own precedent). The order-share column above is recorded for
information only, as the manifest requires, and was not used to select
this value — it is included here purely so the selection process is
auditable, not because it informed the choice.

Proceeding directly to the full 20-seed sweep with `nu_sub=0.01`, per the
manifest's own instruction that nothing about this step should wait for a
fresh precommitment (the rule for selecting nu_sub was frozen in advance;
only applying it was left for this step).
