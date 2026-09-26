# Anchor-bias diagnostic: localized to boundary-shift-v2, not coupling itself

Design reasoning and honesty precommitment (written before this ran): `logs/2026-09-26-claude-anchor-bias-diagnostic-selfreview.md`.
Scripts: `data/scripts/external_anchor_bias_diagnostic.py`, `data/scripts/external_anchor_bias_diagnostic_coupling_only.py`.
Raw output: `data/derived/external-anchor-bias-diagnostic-{,coupling-only-}summary.json`.

## Headline result

**The section-varying-beta check's anchor bias (-0.0557 bits/boundary at uniform beta=0.5) is
conclusively localized to `boundary-shift-v2`, not to `coupling-v2`'s own coupling mechanism.**

Four configurations, same 3 seeds throughout, mean generated edge-gain-gap (Currier A − B):

| Configuration | Mean edge-gain-gap | Notes |
|---|---:|---|
| Raw Naibbe, no postprocessing | -0.0041 | Essentially zero — noise floor |
| Coupling-v2 alone (beta=0.5), no boundary-shift, no top-up | +0.0064 | Essentially zero, and flips sign across seeds |
| Coupling-v2 + boundary-shift-v2, no top-up | -0.0575 | Matches the full anchor almost exactly |
| Full anchor (coupling + boundary-shift + substitution top-up) | -0.0557 | Original result from last cycle |

Adding `boundary-shift-v2` to coupling alone moves the mean gap from +0.0064 (noise) to -0.0575 — the
entire bias appears at that one step. Adding the substitution top-up on top of that changes the result
by only 0.0018, confirming (independently of the ordering here) that step contributes essentially
nothing to this particular bias.

## Interpretation

This confirms the guess named in last cycle's section-varying-beta report: `boundary-shift-v2`
interacts with Currier A/B's real line-length asymmetry (A: mean 6.82, B: mean 9.30, already measured)
in a way that produces a differential edge-gain effect between sections, independent of any deliberate
section-aware manipulation of `beta` or `nu_sub`. `boundary-shift-v2` works by combining adjacent
token pairs and re-splitting them at a new boundary — its behavior is sensitive to where lines are cut
(the line-length template), so a section with shorter average lines (Currier A) has more line-boundary
positions per token, which plausibly changes how often eligible cross-line shifts occur relative to a
longer-lined section (Currier B). This is a plausible mechanism for the observed asymmetry, disclosed
as a plausible account consistent with the data, not independently proven by a further test in this
diagnostic.

**What this means for the section-varying-beta result**: since the anchor's own bias is now
attributable to `boundary-shift-v2` (a step neither this diagnostic nor the beta design varied by
section), the beta design's own -0.3070 result is confounded with this same boundary-shift artifact
throughout — the -0.0557 baseline is present regardless of the beta values chosen, riding underneath
whatever effect varying `beta` itself contributes. This does not mean `beta` contributes nothing (the
design's gap, -0.3070, is much larger in magnitude than the -0.0557 baseline alone, leaving room for a
real `beta` effect on top of it) — but it means the clean "manipulation check passes, so the design
result is attributable to beta" logic this project's discipline requires cannot be satisfied by this
design as specified, since the confound is now identified but not removed.

**What remains open**: a corrected design could either (a) explicitly measure and subtract the
boundary-shift-only baseline before interpreting any future beta-pair's own gap, or (b) hold line
lengths equal across sections for the purposes of this specific test (e.g. resampling or restructuring
the template) — both are new design choices needing their own fresh precommitment, not attempted here.
This diagnostic's job was to localize the confound, which it did cleanly; correcting for it is a
distinct next step.

**Does not bear on `coupling-v2`'s own pooled six-criterion PASS**, which is unaffected — this
diagnostic only concerns the per-section edge-gain-gap question, not the pooled criteria.
