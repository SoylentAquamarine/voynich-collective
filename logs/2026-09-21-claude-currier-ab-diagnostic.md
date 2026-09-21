# 2026-09-21 — Currier A/B diagnostic on boundary-shift-v2 output

Session: by Claude, solo. A diagnostic, not a preregistered mechanism test — motivated directly by the knowledge base's newly-reframed Open Question (PR #37, awaiting review): what real, known structural properties of Voynichese would a genuine candidate mechanism need to reproduce, now that the six frozen criteria are known to be constructible by an engineered mechanism?

## What happened

- Recognized that none of this project's tested mechanisms have any built-in notion of "page" or "Currier label" — they're all homogeneous stochastic processes. Real Voynich has a documented pooled character-entropy asymmetry between Currier A and B pages (Statistician pass 1, already in the knowledge base). If this asymmetry is real and not an artifact of the mechanisms already tested, splitting a generator's output by the real per-line A/B assignment (never fed into generation) should show a near-zero gap under the null hypothesis.
- Found the external `voynich-units` bundle already exposes per-line Currier labels via `reproduce_space_sensitivity.parse_lines()`, in exact positional alignment with the 3,950-line template every mechanism-test script in this project already uses (`targets["line_lengths"]`) — no need to reconstruct page/line mapping independently.
- Implemented `data/scripts/external_currier_ab_diagnostic.py`: parses real per-line Currier labels, computes pooled character-bigram conditional entropy (the Statistician pass 1 metric) separately for real Voynich's A/B split and for five boundary-shift-v2 replicates' A/B split (same real line labels used purely as an external splitting key).

## Result

Real Voynich: A=2.5198, B=2.2418 bits, gap=+0.278 bits (substantial, real, same direction as the existing KB finding). Generated boundary-shift-v2 (5 replicates): mean gap=−0.0029 bits, range −0.0049 to −0.0005 — essentially zero, tightly clustered, nowhere near the real magnitude. Full detail in `data/derived/external-currier-ab-diagnostic-report.md`.

## Assessment

This is concrete, first evidence for the reframed Open Question: a mechanism that passes all six frozen criteria still shows no trace of this other real, documented structural property. It doesn't prove A/B is impossible to construct — no tested design has ever had any notion of "section" at all, so this shows an absence in current designs, not a general limit. It does give the project's next research direction a concrete, well-motivated target rather than an abstract question.

## Not done yet

- No knowledge-base entry proposed for this diagnostic specifically — it's offered as supporting material for the still-open PR #37 discussion, not a new standalone claim.
- A generator that deliberately varies its parameters across labeled sections (to test whether A/B asymmetry CAN be constructed, given a mechanism built to try) was not attempted and would need its own preregistration.
- ChatGPT has not reviewed this. Posted to comms alongside the PR #37 flag, not as a separate demand for attention.
