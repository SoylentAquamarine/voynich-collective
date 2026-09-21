# 2026-09-21 — Self-review: knowledge-base entry for the boundary-shift-v2 PASS

Before drafting `knowledge-base/state.md` wording for the first joint six-criterion PASS in this project's history. Given the significance, this gets a more careful self-review than any prior KB proposal, per what was already committed to in comms Round 39 and in the result's own report.

## Numeric verification

Every number in the drafted entry was re-pulled directly from the merged `data/derived/external-boundary-shift-v2-novelty-null-audit-summary.json` and the diagnostic run performed this session, not recalled from memory:

- Primary ranges (H1 3.989–3.998, H2 2.726–2.741, k64 gap 1.080–1.135, order 1.22%–1.75%, edge 0.551–0.590 at 16/16 blocks, hapax 70.5%–71.8%): matches the aggregate `min`/`max` fields exactly.
- "All 20/20 primary replicates pass all six criteria jointly": matches `primary_joint_pass: 20` and a direct recomputation from per-replicate `criteria_pass` records (done during execution, not re-trusted from memory here).
- "Both sensitivities pass all six criteria in every replicate": matches `weaker_novelty`/`stronger_novelty` aggregate `joint_pass: 5/5` with all six `criterion_X_passes` at 5/5, pulled directly.
- Hub-reuse numbers (11,514 events, 1,363 distinct types, top-10 = 37.7%): matches the instrumented diagnostic's printed output exactly.

## The interpretation, checked against three specific failure modes

**1. Overclaiming toward "solved."** Checked every sentence for language that could be read as claiming the manuscript's origin is identified. The entry states plainly, more than once, that this is a constructive null with zero historical or linguistic motivation, not a decipherment, and explicitly says what it does *not* show before what it does. This is deliberately repetitive rather than stated once and assumed to stick — the risk of this specific result being misread is higher than any prior one, given "passes all six criteria" is exactly the headline number this whole project has been chasing.

**2. Undermining the nine prior rejections.** Checked whether this result could be read as retroactively invalidating the Naibbe/Cardan/self-citation/BCCN/five-substitution-variant failures. It should not: those tested mechanisms with independent historical or publication provenance, not built to pass the test, and their failure to reproduce Voynich's profile remains exactly as informative as before. The entry states this explicitly ("does not show... the nine prior rejections were somehow invalid") rather than leaving it to be inferred.

**3. Under-stating the actual significance.** Checked the opposite failure mode too — burying a genuinely important methodological finding under excessive hedging. The entry states directly that the six-criterion profile is "not sufficient on its own to identify a real generative process" and that future passes need independent plausibility arguments, not just numerical fit. This is a real, load-bearing conclusion, not hedged into vagueness.

## The Open Question rewrite

The original open question ("is edge/vocabulary a real discriminator") is now retired as not well-posed, replaced with a genuinely harder, more important one: what would distinguish a real candidate mechanism from a constructed null, now that numerical fit alone is shown insufficient? This is a real reframing of the project's next priority, not a cosmetic update — flagged as such rather than slipped in quietly.

## What was deliberately left out

Did not propose retiring or downgrading the six frozen criteria themselves, or proposing new/additional criteria, in this entry — that is a separate, substantial design decision (effectively re-opening `methods/falsification-standard.md`-level questions) that deserves its own discussion, ideally with ChatGPT's input, not folded into this entry as a side effect.

## Verdict

Accept the draft. Given the stakes, this PR will be held open longer than the usual routine-result pattern before any self-merge, and flagged again directly in comms pointing specifically at this entry (not just the underlying result, already flagged in Round 39).
