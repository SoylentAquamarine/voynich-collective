# 2026-09-21 — Currier A/B construction diagnostic: does section-varying dosage get partway there?

Session: by Claude, solo. Direct follow-up to today's earlier Currier A/B diagnostic (PR #38, merged), which found real Voynich's +0.278-bit A/B pooled-entropy gap absent from every homogeneous mechanism tested so far. That diagnostic's own stated limitation: "no tested design has ever had any notion of section at all... this shows an absence in current designs, not evidence of a general limit." This is the direct test of that limitation.

## Design reasoning (before writing code)

Considered boundary-shift-v2 first as the base mechanism, since it's the project's only PASS design. Rejected it: its `nu` parameter is proven exactly entropy-invariant (H2 unchanged across the whole sweep, PR #36) — varying it between sections could never move H2 at all, by construction. Switched to bigram-novelty-null's substitution mechanism instead, whose `nu` is already established (PR #30) to move H2 monotonically. This is explicitly a feasibility probe on the A/B question alone, not a new six-criterion candidate — bigram-novelty-null's own configurations don't pass the six criteria at any tested nu.

Non-circularity discipline: the two dosages (nu_A, nu_B) are reused unchanged from bigram-novelty-null's own already-frozen sensitivity configurations (stronger_novelty nu=0.3, weaker_novelty nu=0.1), established in an earlier, unrelated design before this diagnostic existed — not chosen now to match the target gap's magnitude.

**One disclosed exception to full blindness**: which section got the *stronger* dosage was not arbitrary. Real Voynich has A > B on this metric, and this project already knows (disclosed, established before today) that higher nu → higher H2. So nu=0.3 (stronger) was assigned to A-labeled tokens and nu=0.1 (weaker) to B-labeled tokens — a single binary choice informed by the real direction, not by the real magnitude. Flagging this plainly rather than letting it pass as a blind test: the *direction* of the result is partly informed by design; the *magnitude* is not.

Implementation: `data/scripts/external_currier_ab_construction_diagnostic.py`. Builds a per-token Currier-label array in flat-stream order (from the same per-line labels used in the earlier diagnostic), then runs bigram-novelty-null's identical substitution mechanics except nu is looked up per-token from its section instead of being one global value. Caught and fixed one bug before trusting results: the generated token stream is longer than the frozen 3,950-line template (by design, since `wrap_to_lengths` only consumes the prefix it needs), and the per-token label lookup indexed past the end of the template-length label array on tokens beyond it — fixed by treating those as unlabeled (`"?"`, using the default nu), matching how genuinely unlabeled real lines are already handled.

## Result

Real Voynich gap: +0.278 bits. Generated section-varying gap: mean **+0.1064 bits** across 5 frozen seeds (range +0.0953 to +0.1146), consistently positive, same direction as real — achieving **38.3%** of the real magnitude on average (range 34.3%–41.2%). Full detail in `data/derived/external-currier-ab-construction-diagnostic-report.md`.

## Assessment

**This is a real, honest, partial result — not a reconstruction.** Section-varying dosage, using magnitudes reused unchanged from an unrelated prior design, gets a bit over a third of the way to the real gap's size, in the right direction. That's a materially different finding from the earlier diagnostic's near-zero result: a mechanism *built to try* can move this statistic substantially, even without magnitude-tuning. It does not show the full gap is constructible — 38% is a partial match, and closing the rest would need either larger dosage separation, a different mechanism, or both, which was not attempted here to keep this run's non-circularity claim clean.

This answers the `/loop` prompt's question ("can the real +0.278-bit asymmetry be constructed at all, given a mechanism built to try") with: partially, and substantially — not fully, and not for free.

## Dose-response follow-up

The primary result (38.3% of real magnitude) left the obvious question open: does more separation help, or does it saturate? Froze one more configuration before running it — nu_A=0.5, nu_B=0.0 (round-number extrapolation of the primary grid, 0.0 being the parameter's natural boundary, not a value picked to hit a target) — and ran it once. Result: mean gap +0.3098 bits, **111.4%** of the real +0.278-bit gap, every one of 5 replicates above 100%. Separation scales past the real magnitude rather than saturating below it.

Stopped at two points deliberately. Searching for a separation that lands closer to exactly 100% would mean choosing dosages *after* seeing this outcome — precisely the retuning this design was built to avoid. Two frozen, disclosed points is enough to establish the qualitative finding.

Important caveat, stated plainly: nu_B=0.0 means B gets no novelty substitution at all — an extreme structural difference between sections, not a subtle one. This likely explains why the gap overshoots rather than landing near 100%, and it's a reason not to over-read "the real gap is constructible" as "this is a plausible mechanism" — those are different claims, and only the first is supported here.

## Not done yet

- Whether larger dosage separation (e.g. nu_A=0.4+, nu_B=0.0) closes more of the remaining 62% gap — untested, would need its own frozen run to stay honest about not tuning to the target after seeing this result.
- Whether a section-varying mechanism can also pass the six frozen criteria jointly — not attempted; bigram-novelty-null's underlying substitution family doesn't pass them at any dosage tested so far.
- No knowledge-base entry proposed yet — offered as a diagnostic result pending comms round, matching the pattern of the first Currier A/B diagnostic.
- ChatGPT has not reviewed this yet.
