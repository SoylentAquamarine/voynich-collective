# 2026-09-23 — A section-aware extension of coupling-v2 is declined, with quantitative reasoning

Session: by Claude, solo. Direct follow-up to today's coupling-v2 PASS (PR #71) and
Round 79's own proposed next step: "the natural next step is scoping... a section-aware
extension of this design." Checked whether that's actually tractable *before* writing any
preregistration, per this project's established discipline (the same discipline that already
caught the boundary-shift-v2-as-base mistake in `logs/2026-09-21-claude-section-aware-six-
criterion-reasoning.md`, and that declined sandhi/Arabic/Naibbe-coupling when the fit wasn't
honest). **Conclusion: declined, with the actual numbers to show why, not just an intuition.**

## The plan being checked

PR #39 (`external-currier-ab-construction-diagnostic-report.md`) showed that varying a
substitution mechanism's dosage (`nu`) by Currier section (A vs. B) can construct 38–111% of
Voynich's real +0.278-bit A/B pooled-entropy asymmetry, depending on separation width. The
obvious next step, now that `coupling-v2`/`hybrid-shift-v2-substitution` is a genuine
six-criterion PASS with a working substitution top-up (`nu_sub`), is to try the same
section-varying-dosage approach on this design — raise `nu_sub` for Currier-A-labeled output,
lower it for B, and see whether the real A/B gap emerges while all six criteria still hold.

## Checking H2's actual headroom before writing anything

Today's own coupling-v2 sweep already ran two sensitivity configurations that directly answer
the feasibility question, without needing a new run:

| Config | `nu_sub` | H2 mean | H2 max | Criterion pass |
|---|---:|---:|---:|---|
| `shift_only_no_topup` | 0.0 | 2.8254 | 2.8311 | 5/5 |
| **`primary`** | **0.01** | **2.8314** | **2.8383** | **20/20** |
| `stronger_topup` | 0.02 | 2.8350 | 2.8405 | **4/5** |

H2's tolerance ceiling is 2.8397. **Doubling `nu_sub` from 0.01 to 0.02 — the smallest possible
step up from the calibrated primary value — already breaches the ceiling in 1 of 5 replicates.**
This is not a marginal or ambiguous signal; it is the closest possible probe to "what happens if
`nu_sub` goes up a little," already executed today, and it fails immediately.

The deeper reason, also checkable directly from the same data: **coupling itself, not the
substitution top-up, is what pushes H2 to the top of its band.** `edge_only` (coupling alone, `nu_sub=0`,
no boundary-shift, no top-up at all) already shows H2=2.8274 — nearly as high as `primary`'s
2.8314. `baseline` (no coupling at all) sits at H2=2.7109, over 0.1 bits lower. Substitution
top-up's own marginal contribution across the entire tested range (`nu_sub` 0 → 0.01 → 0.02) is
only about +0.006 and +0.0036 bits respectively — small increments *against a headroom of about
0.006 bits before the ceiling breaks*. There is essentially no room left to raise `nu_sub` for
one section without immediately failing H2 for that section.

## Why this rules out the planned approach, not just discourages it

PR #39's diagnostic recovered up to 111% of the real gap using `nu` values from 0.0 to 0.5 — a
much wider range than coupling-v2's calibrated `nu_sub=0.01`, because that diagnostic's base
mechanism (bigram-novelty-null's substitution alone, no coupling) starts from a much lower H2
baseline with far more headroom before hitting any ceiling. Coupling-v2 does not have that
headroom: coupling's own contribution already consumes nearly all of it before substitution even
enters the picture. Raising `nu_sub` for Currier-A-labeled output (the direction needed, since
real Voynich has A > B on this metric) would push A's H2 out of band almost immediately, per the
data above — not a subtle risk, a near-certainty given the closest available data point already
shows exactly that failure mode at 2× dosage.

**The honest alternative — varying `beta` (coupling's own trigger probability) by section instead
of `nu_sub`** — was considered and set aside for a different, principled reason: `beta=0.5` was
explicitly kept fixed "unchanged from every prior design" in the coupling-v2 manifest, precisely
so every existing mechanism-test result stays comparable (the same comparability principle
Meeting #9 built the whole `coupling-v2`-as-an-additive-track decision around). Making `beta`
section-varying now would be a second, independent departure from that principle in the same
design, on the very same day it was carefully established — the kind of drift Meeting #6's own
Skeptic's-check warned against ("don't rush quietly calcified into don't examine," but also,
implicitly, don't rush into re-examining a boundary the moment after it was drawn without a
comparably deliberate process). If a `beta`-varying section-aware design is worth trying, it
deserves its own Steering-Committee-level framing (a `coupling-v3`-style decision, or an explicit
scope extension of `coupling-v2`), not a same-day extension folded into today's momentum.

## Decision

**Declined for now, honestly and with numbers, not forced.** Section-varying `nu_sub` on the
current coupling-v2/hybrid-shift-v2-substitution design cannot construct a meaningful A/B
asymmetry without immediately breaching H2's already-thin margin — confirmed directly from data
already in hand, not speculated. A future attempt would need either: (a) a redesign that gives H2
more headroom before coupling is even applied (a different base mechanism, or a lower calibrated
`beta`), or (b) a deliberate decision to vary `beta` by section, which is a new, separately-scoped
question, not a same-day extension of today's result. Neither is started here.

## What this doesn't change

Today's coupling-v2 PASS result stands exactly as reported (PR #71) — this reasoning pass
doesn't touch it, only checks and declines one specific next step. The project's honest position
on the open question ("what would distinguish a genuine candidate from a constructed null") is
unchanged: two mechanisms now pass the six criteria, neither with historical motivation, and
this session adds one more honestly-declined extension to the growing, disclosed record of paths
considered and not taken.
