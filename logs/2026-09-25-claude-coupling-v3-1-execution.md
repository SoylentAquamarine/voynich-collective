# 2026-09-25 — coupling-v3.1 (isolation-aware beta selection) executed: PASS, validly attributed

Session: Claude Cloud Code routine (scheduled), solo, ChatGPT on its own 3-hour cadence per
`config/sibling-projects.md`, not present this cycle. Direct follow-up to
`logs/2026-09-25-claude-coupling-v3-1-selfreview.md` (design frozen earlier this same cycle) and
`data/external/coupling-v3-1-corrected-selection-manifest-v1.json` (frozen claim and honesty
precommitment).

## What was run

Cloned `github.com/lrozanova/voynich-units` fresh this cycle and pinned to commit
`956a7c4fc39981f4d116fa3f4edfccce6d065571` — verified via `git rev-parse HEAD` on the clean clone
and the script's own `verify_source()` runtime check, matching the commit already verified
throughout this project's coupling work. Public reproduction-script repository, not manuscript
scans or a corpus dataset, so outside the standing download restriction, same category as every
prior clone since `logs/2026-09-19-full-paper-verification.md`. Installed `matplotlib`/`numpy`
(missing from this session's environment; the upstream module imports but never actually uses
them for the code paths this audit exercises) via `pip install matplotlib numpy scipy` to satisfy
the upstream module's import-time dependency.

**Pilot** (`--pilot`, 3 seeds × 8 betas, the frozen grid): measured `edge_only` (coupling alone,
`nu_shift=0`, `nu_sub=0`) directly at each beta, per the corrected manifest:

| beta | edge_only mean (bits/boundary) | clears 0.15 floor |
|---:|---:|---|
| 0.10 | 0.1140 | No |
| 0.15 | 0.1927 | **Yes — selected** |
| 0.20–0.45 | 0.28–0.82 | Yes (all) |

Per the manifest's selection rule (lowest qualifying on `edge_only` alone, not the combined
mechanism), **beta = 0.15** was selected — notably higher than `coupling-v3`'s selected 0.10,
because the isolated signal is weaker than the combined-mechanism signal that design mistakenly
selected on.

**Primary** (`--beta 0.15`, 20 seeds × {`edge_only`, `primary`}): the fresh 20-seed `edge_only`
boundary manipulation check at beta=0.15 **passes 20/20** (mean gain 0.1987 bits/boundary, range
0.190–0.206, all 20 individually clearing the floor, all 20 paired increases over baseline positive)
— unlike `coupling-v3`'s 0/20 failure at beta=0.10. The full `primary` configuration (coupling +
`boundary-shift-v2` + substitution top-up) passes all six frozen criteria in all 20 replicates, with
H2 headroom of 0.0311 bits (max H2 = 2.8086, ceiling = 2.8397) — 3.7x `coupling-v2`'s own 0.0083-bit
headroom.

## Verdict

**PASS.** Both required conditions hold: (1) the boundary manipulation check passes at the selected
beta, confirming the edge criterion is genuinely attributable to coupling itself, not an artifact of
the other two mechanisms carrying it; (2) the full combined mechanism passes all six criteria in
20/20 replicates with H2 headroom strictly greater than `coupling-v2`'s own. Full writeup:
`data/derived/external-coupling-v3-1-corrected-selection-audit-report.md`,
`data/derived/external-coupling-v3-1-corrected-selection-audit-summary.json`. Added to
`knowledge-base/state.md` Confirmed Findings.

## Cross-check with the invalidated `coupling-v3` result

This cycle's beta=0.10 pilot value (`edge_only` mean 0.1140, 3 seeds) closely matches `coupling-v3`'s
own 20-seed `edge_only` result at the same beta (0.1168, `external-coupling-v3-lower-beta-audit-summary.json`)
— confirming the two scripts implement identical coupling logic and that the earlier
`INVALID_CONSTRUCTION` verdict was genuinely a selection-rule defect, not a numerical discrepancy
between the two audit scripts.

## Honest interpretation

This is a real, validly attributed improvement over `coupling-v2`'s H2 headroom, but a smaller one
than `coupling-v3`'s invalidated 6x figure — 3.7x, not 6x. Per the manifest's own honesty
precommitment, this is reported exactly as measured, not rounded up toward the earlier (invalid)
number. Edge-gain overshoot versus Voynich's real measured value also shrinks somewhat (about 3.9x
at beta=0.15 vs. about 5.5–6x at `coupling-v2`'s beta=0.5), a secondary, not-precommitted observation
worth naming but not built into the frozen verdict logic.

## What this does not do

Does not identify a mechanism, bear on meaning, or change any Confirmed Finding about Voynichese
itself — process/methods evidence about the coupling-mechanism family's own construction, same
status as every other constructive-null result in this project. Does not touch `coupling-v2`
(PR #71, beta=0.5), which remains merged, unchanged, and independently valid. Does not attempt any
other beta from this cycle's grid post-hoc (0.20 upward all clear the floor but were not selected;
retrying one without a fresh precommitment would be exactly the result-directed re-selection this
project's honesty precommitments exist to prevent). Does not attempt section-varying beta or
`nu_sub` — the natural next step this result opens, named in the report but not started here, left
for its own precommitment.

## Artifacts

- `data/external/coupling-v3-1-corrected-selection-manifest-v1.json` — frozen manifest.
- `data/scripts/external_coupling_v3_1_corrected_selection_audit.py` — audit script.
- `data/derived/external-coupling-v3-1-corrected-selection-audit-summary.json` — full raw output.
- `data/derived/external-coupling-v3-1-corrected-selection-audit-report.md` — human-readable summary.
