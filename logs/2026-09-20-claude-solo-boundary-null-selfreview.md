# 2026-09-20 — Solo adversarial self-review of the boundary-coupled null design

Session: by Claude, acting as both Statistician (who drafted PR #24's design) and Skeptic (reviewing it), because ChatGPT did not respond after the design was opened for review — many hours and roughly a dozen check cycles with no comms activity or PR review from their side.

## Why this happened

The user explicitly authorized proceeding solo when ChatGPT is unresponsive: "i want you to do it by yourself if chatgpt does not answer. i don't need both of my employees calling in sick, you have to make progress." This overrides the earlier caution (stated in comms Round 27 and several loop ticks) that PR #24 specifically needed genuine cross-party review, not a self-review, because the whole point of outcome-blind preregistration is adversarial distance between the designer and the reviewer.

Given that constraint can no longer be met, the next best thing is to review the design as skeptically as possible myself, in a separate pass from when it was written, and disclose plainly that this is a weaker substitute for real cross-party review — not to quietly treat a self-review as equivalent to one.

## What the self-review found

Rereading `methods/boundary-coupled-null-preregistration.md` from scratch with an adversarial mindset (assuming the design is trying to smuggle in something that would make a pass easier, exactly the posture used when reviewing ChatGPT's Cardan and self-citation designs) surfaced two real defects:

1. **A genuine circularity leak.** Step 3.2 specified mapping the Latin-trained order-2 internal model's characters onto the EVA alphabet "by frequency rank" — the Latin model's most frequent character maps to the EVA alphabet's most frequent glyph. The problem: the only available source of "the EVA alphabet's most frequent glyph" is Voynich's own corpus. This would have silently imported Voynich's real unigram frequency ordering into a component the document explicitly claimed was "trained on a non-Voynich reference text" and non-circular — exactly the kind of one-line design mistake that makes a constructive null's eventual "pass" uninterpretable, because a pass could then be attributed to the borrowed frequency information rather than the coupling rule under test. **Fixed**: the internal model's Latin-to-EVA character mapping now reuses the same arbitrary, mechanical, alphabetical-by-EVA-string ordering already established for the glyph-class partition in step 1, which has no dependency on Voynich's own statistics.
2. **An incomplete sweep.** The `p_couple` sweep stopped at 0.9, leaving out the cleanest possible test of the mechanism's maximum potential (`p_couple = 1.0`, fully deterministic class coupling). Added at negligible cost; the failure condition and hypothesis card were updated to match.

Both corrections are recorded inline in the design document itself (not silently) with an explicit "self-review correction" note at each site, so the document's own history shows what changed and why, matching the project's discipline of never silently overwriting method decisions.

## What did not need changing

- The core coupling-rule design (directly targeting criterion 5 by construction, with a `p_couple=0` negative control) held up under scrutiny — I could not find a way it leaks the coupling signal anywhere else, and the ablation control (checking whether the internal model alone, independent of coupling, could produce edge signal) is correctly designed to catch exactly the failure mode described above if it had survived into the internal-model itself.
- The glyph-class partition (alphabetical round-robin) is about as mechanically arbitrary a partition as is achievable and does not plausibly encode real Voynich adjacency structure.
- The six-criterion bands, reused verbatim from Cardan's already-reviewed preregistration, needed no changes.
- The disclosed-favorable-choice list (token length, alphabet reuse) is accurate and complete once the frequency-rank leak above is closed — no other undisclosed favorable choice was found.

## Assessment

Given the two defects found and fixed, and that no other issues survived a genuinely adversarial pass, the design is now cleared for solo execution. This is explicitly weaker evidence of design soundness than genuine two-party review would have produced — a second reviewer with independent judgment might catch something this pass missed, and if ChatGPT does return and finds an issue, that would be recorded the normal way (a new log entry, not a silent edit) and treated seriously rather than defended.

## Next step

Implement the generator, run the `p_novel` pilot calibration (self-consistency only, no Voynich comparison, per the design's own stop condition), then execute the full sweep and score it against the frozen six criteria.
