# A genuinely new, corpus-derived coupling-v2 dosage design: design reasoning (written before any code runs)

**Trigger:** this project's own note, repeated across several cycles, that "a genuinely new,
non-circularly-justified coupling dosage design... deserves its own dedicated design cycle" —
this is that cycle, using the real Currier A/B grounding statistics computed two cycles ago
(`data/scripts/external_currier_ab_length_repetition_stats.py`).

## What's already known before this design (disclosed up front)

- Real, non-circular Currier A/B statistics (already computed, unrelated purpose at the time):
  Currier A has mean line length 6.82 and repetition rate 68.1%; Currier B has mean line length
  9.30 and repetition rate 78.7%. B's lines are ~1.36x longer than A's; B's repetition rate is
  ~1.15x A's (B's rate ÷ A's rate = 0.7869/0.6812 = 1.155).
- The `coupling-v2` section-aware pilot's own already-executed grid (`external-coupling-v2-section-aware-pilot-summary.json`)
  tested six `(nu_sub_A, nu_sub_B)` ratios: 1.00, 4.00, 10.00, 50.00, and two "B=0" (infinite ratio)
  configurations. Their mean gaps, as a fraction of the real +0.278-bit gap, were **monotonic in the
  ratio**: -6.17%, -4.64%, -3.64%, -1.69%, +1.51%, +4.83% — crossing from negative to positive
  somewhere between ratio 50 and the B=0 configurations, and only the two positive-but-still-far-short
  results (ratio "infinite") failed the six-criterion check outright.
- **Both natural corpus-derived ratios (1.15 and 1.36) are far below the mildest ratio already tested
  (4.00), which itself only reached -4.64% of the real gap** (still wrong-signed). Given the grid's own
  monotonic trend, a ratio this close to 1.0 should land very close to the ratio=1.00 anchor's own
  result (-6.17%) — small, negative, wrong-signed.

## What has NOT been done before this design (result-blinding)

No coupling-v2 stream has been generated at either of these two specific corpus-derived ratios. The
above is a *prediction* extrapolated from the existing grid's own monotonic trend, not a result. This
design exists to check that prediction against an actual run, not to assume it.

## The design

Reuse `coupling-v2`'s exact mechanism (beta=0.5, `apply_section_varying_substitution_topup`), identical
to the already-executed pilot/primary scripts. **Two dosage pairs, both derived directly from the real
corpus statistics above, anchored at this family's own already-frozen primary value (`nu_sub`=0.01) for
whichever section the ratio assigns the weaker dose to** — following the already-established finding
(from the `coupling-v3.1` and `coupling-v2` pilot work) that the *stronger* dose must go to Currier A to
have any chance of the correct sign:

- **Design 1 — repetition-rate-derived**: `nu_sub_A = 0.01 × (repetition_rate_B / repetition_rate_A) =
  0.01 × 1.155 = 0.01155`, `nu_sub_B = 0.01` (anchor).
- **Design 2 — mean-length-derived**: `nu_sub_A = 0.01 × (mean_length_B / mean_length_A) = 0.01 × 1.364
  = 0.01364`, `nu_sub_B = 0.01` (anchor).

Both values are derived arithmetically from statistics already computed for an unrelated purpose
(descriptive grounding, disclosed as such at the time) — neither is picked to hit the target gap, and
neither reuses an existing dosage pair from any prior grid. `nu_sub_default` (unlabeled lines) stays at
0.01, matching every prior design in this family.

Reuse the pilot's own 3 seeds (42, 179, 316) for a quick check before deciding whether a full 20-seed
primary run is warranted — following the same pilot-then-primary discipline as every prior design in
this family, not skipping straight to a full run.

## Honesty precommitment

The predicted outcome (a small, negative, wrong-signed gap close to -6% of the real gap, similar to the
ratio=1.00 anchor) is stated above, in writing, before any of these two specific configurations has been
run. Whatever the actual result is — confirming the prediction, contradicting it, or something in
between — is reported exactly as measured. If both designs confirm the prediction, this closes off
corpus-statistic-derived `nu_sub` scaling as a viable lever for this mechanism family (not just this
specific pair), since it would show that even the best-motivated real values, not just already-frozen
arbitrary ones, land inside the same already-explored failure region. If either design surprises the
prediction, that itself is reported as the more interesting finding.

## Why this is genuinely new work, not a repeat

Every prior section-aware attempt in this project (both `coupling-v3.1` attempts, the `coupling-v2`
grid) used dosage values reused from an existing frozen grid or explicitly disclosed as arbitrary. This
design's two values are, for the first time, derived from actual Currier A/B corpus statistics computed
independently of this dosage-design question — a qualitatively different (if, per the prediction above,
likely still insufficient) source of numbers.
