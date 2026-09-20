# Preregistered boundary-coupled constructive null

Status: **frozen design, self-reviewed, cleared for execution**
Registered: 2026-09-20, drafted by Claude (Statistician) per Steering Committee Meeting #4's action item
Owner of the run: Claude, proceeding solo per explicit user authorization after ChatGPT went unresponsive for an extended period (see `logs/2026-09-20-claude-solo-boundary-null-selfreview.md`)

**Note on review process:** this design was intended for ChatGPT's independent design review before execution, exactly as Cardan's preregistration required Claude's review before ChatGPT executed it. ChatGPT did not respond after this document was opened for review. Per the user's explicit instruction to make progress rather than block indefinitely on an unresponsive collaborator, Claude performed its own adversarial self-review instead (documented in the log above) — this is weaker than genuine cross-party review and is disclosed as such. The self-review found and fixed two real defects (see the log): a circularity leak in the internal model's character mapping, and a missing sweep value. Both are corrected below.

## Why this design

Three named mechanisms (Naibbe, Cardan-grille, self-citation) have now been tested against the project's six-criterion joint profile and all three fail the same two criteria — held-out cross-token edge prediction and open vocabulary — while passing a mix of the others. Meeting #4 concluded that the missing ingredient is not generic "state" or "novelty" (self-citation has real local copy/mutation state and still fails edge prediction by roughly the same margin as Naibbe and Cardan). The open question this project has repeatedly deferred is whether the edge/vocabulary axis is becoming a real discriminator between "meaningful/structured text" and "the mechanisms tried so far," or whether it is simply a property of three mechanisms that were each chosen for historical or literature relevance rather than designed to pass it.

This preregistration answers a narrower, cleaner question first: **is it even mechanically possible to construct a generator that satisfies all six criteria simultaneously, without copying Voynich's own statistics?** If a deliberately-built, non-circular generator can pass, that shows the joint profile is achievable by construction and narrows what "explains Voynich" would require. If even a generator purpose-built for exactly the two failing properties still cannot pass, that is a materially stronger and more surprising result than any of the three prior mechanism tests — it would suggest the six-criterion joint profile resists simple constructive explanation generally, not just the three specific historical mechanisms tried.

This is a constructive null, not a historical claim. No argument is made that Voynichese resembles this generator's construction; the point is solely whether the joint statistical profile is achievable at all by a process built for the purpose.

## Design principle: coupling by construction, not by fitting

Every design choice below is fixed **before** any code is written or any output is generated, and none of the frozen parameters are derived from Voynich's own observed transition statistics, entropy, or vocabulary growth curve. Two specific things are disclosed as deliberately favorable to the hypothesis, exactly as the self-citation audit disclosed its own favorable calibration:

1. The token-length distribution is drawn from Voynich's own observed length distribution (not fit to make edge prediction easier — length alone does not affect edge coupling).
2. The character alphabet reused is the EVA glyph inventory itself (an alphabet choice, not a statistic — every prior mechanism test also drew from this alphabet).

Everything that could affect the two failing criteria specifically — the class partition, the coupling rule, and the reuse rate that controls vocabulary growth — is fixed by an arbitrary, mechanical rule with no reference to Voynich's actual glyph adjacency or vocabulary statistics. This is the same non-circularity bar the Cardan preregistration held: parameters may be favorable in ways that do not touch the property under test, never in ways that do.

## The generator ("boundary-coupled constructive null", BCCN)

### 1. Alphabet and glyph classes

Use the set of raw single EVA letter-characters that actually appear in the Voynich token stream used by the project's scoring pipeline (25 characters, `a`–`z` minus `w`; an alphabet-membership fact, not a frequency or adjacency statistic — pulling the *inventory* from Voynich is the same kind of disclosed choice as reusing its glyph alphabet in every prior mechanism test). **Self-review correction, replacing the original draft's choice of `grille.ALL_GRAPHEMES`** (the multi-character EVA fragment pool Cardan's generator uses, e.g. `"aiin"`, `"d2"`, `"ch2"`): the project's held-out edge-prediction metric (`edge_crossfit`) reads only the trailing and leading **character** of each raw token string (`left[-1]`, `right[0]`), not a semantic "glyph unit." A class-coupling rule built over multi-character fragments does not reliably control what that metric observes — different fragments assigned to the same class can have different trailing/leading characters, diluting or destroying the intended signal, which would have made the "targets criterion 5 by construction" claim below false in practice even though true in intent. Using single characters as the atomic unit makes "first glyph of token" and "first character of the token string" identical by construction, so the coupling rule controls exactly what the scoring metric measures, with no gap between intent and implementation.

Partition the 25-character alphabet into `K = 6` classes by a purely mechanical rule fixed before design: sort it alphabetically and assign characters to classes round-robin (character `i` → class `i mod K`). This partition carries no linguistic or Voynich-adjacency meaning — it is an arbitrary but fixed labeling, chosen this way specifically so it cannot be accused of encoding real Voynich structure.

### 2. The coupling rule (targets criterion 5 directly, by construction)

For a token ending in a glyph of class `c`, the next token's **first glyph's class** is drawn from a fixed distribution `f(c)`:

- With probability `p_couple`, the next token's first-glyph class is `(c + 1) mod K` (a fixed, arbitrary successor rule).
- With probability `1 − p_couple`, the next token's first-glyph class is drawn uniformly from all `K` classes.

Once the class is chosen, the actual first glyph is drawn uniformly from the glyphs in that class. This is the only place in the generator where the previous token's identity influences the next token — it directly targets the last-glyph → next-first-glyph criterion, and nothing else in the design is allowed to also encode this coupling (no other hidden channel of adjacency is permitted; this must be checked in code review before execution).

`p_couple` is swept over `{0.3, 0.5, 0.7, 0.9, 1.0}` — the same style of parameter sweep used for Cardan's jump probability — so the test asks whether *any* coupling strength in this family passes, not just one arbitrary value. **Self-review correction**: the original draft stopped at 0.9; added 1.0 (fully deterministic class coupling) as the cleanest possible test of the mechanism's maximum potential, at negligible extra cost.

### 3. Token-internal structure (does not target any criterion by construction)

After the first glyph is fixed by the coupling rule:

1. Draw a token length from Voynich's own observed word-length distribution (disclosed favorable choice, per above — affects entropy/BPE scale only, not edge coupling or vocabulary growth mechanics).
2. Fill the remaining positions one at a time using an order-2 character Markov model **trained on a non-Voynich reference text** (the already-pinned Latin baseline corpus from `data/derived/language-baselines-report.md`), mapped onto the EVA alphabet **using the same arbitrary alphabetical-by-EVA-string ordering established in step 1** (Latin model's 1st character in that model's own frequency order → EVA alphabet's 1st glyph in alphabetical order, 2nd → 2nd, and so on). **Self-review correction**: the original draft of this document specified mapping "by frequency rank," meaning the Latin model's most frequent character would map to the EVA alphabet's *most frequent* glyph — but the only source of "EVA alphabet's most frequent glyph" is Voynich's own corpus, so that mapping would have silently imported Voynich's real unigram frequency ordering into a step meant to be non-circular. Fixed to use the same Voynich-independent alphabetical ordering already used for the class partition, closing that leak.
3. **Implementation-pilot correction, replacing the original `p_novel` novelty-splice design**: building and pilot-testing the order-2 Latin-trained internal model (step 2) revealed that it is already far *too* open on its own — even with zero deliberate novelty injection, a 25-letter alphabet with word lengths up to 22 and order-2 branching produces ~83% singleton types, already above Voynich's ~70% point estimate before any "novelty" mechanism is added. The originally-designed lever (splice in random characters to *increase* openness) therefore pushes the wrong direction; the real need is a lever that *increases* repetition. Replaced with a **reuse mechanism**: maintain a memory of previously-generated internal parts (everything after the coupled first glyph), bucketed by length; with probability `p_reuse`, instead of generating a fresh internal part via the order-2 model, resample verbatim from memory (matched by length) — otherwise generate fresh and add it to memory. This still touches only vocabulary growth, not edge coupling (the first glyph is always set by the coupling rule regardless of reuse) or entropy/BPE scale (reused text has the same character-level statistical profile as freshly-generated text, just repeated).

`p_reuse` is calibrated once via a small pilot **before freezing this document** to target roughly Voynich's aggregate hapax share (~70%) at the corpus's final size — this calibration is disclosed exactly like the self-citation audit's disclosed favorable calibration, and only affects the vocabulary-growth criterion, not edge coupling, entropy, or BPE scale. **Pilot result**: `p_reuse = 0.87` produces 69.9–70.3% hapax share across three pilot seeds (self-consistency check only — generated text was never scored against Voynich's actual joint profile at pilot time, per the stop conditions below). This value is frozen for all subsequent execution.

### 4. Sequence assembly

Tokens are generated one at a time, in order, using the coupling rule (step 2) chained to the previous token's actual last glyph, until at least 39,026 tokens exist (the same conservative generation-floor figure Cardan's preregistration used; the line-length template's actual requirement is 32,747 tokens, so this floor is a safety margin, not a hard minimum — `scale.wrap_to_lengths` truncates any excess). The stream is then wrapped onto Voynich's exact line-length template (`scale.wrap_to_lengths`, the same forced-template approach used by Naibbe and Cardan — not the self-citation audit's looser "first N lines," which this preregistration explicitly avoids repeating after the fairness caveat raised in that audit's review).

## Hypothesis card

### Claim

At least one `p_couple` setting of the frozen BCCN generator can produce a corpus that jointly matches all six of the project's frozen criteria (the same bands used in the Cardan preregistration) on the same generated replicate.

### Alternatives

- **The joint profile is not mechanically hard**: some coupling strength passes, showing six-criterion joint satisfaction is achievable by simple construction and does not by itself indicate anything unusual about Voynichese.
- **The joint profile resists even purpose-built construction**: no coupling strength passes, meaning the specific *combination* of properties is harder to jointly satisfy than any single criterion in isolation suggests — a positive result for the project's discriminating-test program, though still not evidence of language, cipher, or meaning.
- **A confound in the construction, not the mechanism family, explains failure**: e.g., the order-2 Latin-mapped internal model or the novelty-splice mechanism interact with the coupling rule in a way that suppresses edge signal or distorts entropy — this would need to be ruled out by the sensitivity checks below before treating a failure as informative.

### Discriminating prediction

If passed, at least one `p_couple` value produces joint criteria satisfaction on the frozen bands, in at least 16 of 20 seeded replicates (same threshold convention as Cardan), with edge gain ≥0.15 bits/boundary at ≥15/16 line blocks specifically arising from the class-coupling rule (verified by an ablation: set `p_couple = 0` and confirm edge gain collapses to ≈0, proving the passing configuration's edge signal is attributable to the coupling rule and not an artifact of the internal-structure model).

### Failure condition

The claim fails if no `p_couple` in `{0.3, 0.5, 0.7, 0.9, 1.0}` reaches 16/20 joint passes. As with Cardan, passing only after changing a frozen parameter, band, seed, or the coupling rule itself after seeing output is a failure of version 1 and requires a new preregistration, not a patch.

### Units, controls, and sensitivity checks

- 20 seeds per `p_couple` value (`42 + 137*i`, `i = 0..19`, same convention as Cardan and self-citation).
- Negative control: `p_couple = 0.0` (coupling rule reduces to uniform — should fail edge decisively, confirming the rule is what carries any passing signal).
- Ablation control: for whichever `p_couple` value comes closest to passing, rerun with the order-2 internal model replaced by pure uniform-random internal glyphs, to check whether the internal-structure model (not the coupling rule) is doing unacknowledged work on the edge criterion.
- The `p_reuse` pilot calibration (see above) is the only pre-registration-time computation permitted; it may not be tuned against edge gain, entropy, or BPE scale — only against the corpus's own vocabulary growth curve shape, checked internally, with no Voynich comparison at pilot time.

## Six-criterion project profile

Reuse the exact frozen bands from `methods/cardan-grille-preregistration.md` `six_criteria` without modification: H1 3.9763±0.15, H2 2.6897±0.15, learned-unit checkpoint at 32 or 64 merges with k64 gap in [0.90, 1.20], token-order share in [0%, 2.0%], held-out edge gain ≥0.15 bits/boundary with ≥15/16 positive blocks (alpha=1, 16 contiguous Voynich-template line blocks), hapax share of types ≥0.65. No band is altered for this test; reusing the identical, already-reviewed bands is itself part of keeping this comparable to the prior three mechanism data points.

## Stop conditions

Stop and return to review, without interpreting a result, if:

- the `p_reuse` pilot calibration is run against anything other than the generator's own internal vocabulary-growth self-consistency (i.e., if it is ever compared to Voynich's actual hapax curve at pilot time rather than only frozen afterward);
- the class partition, coupling rule, `p_couple` sweep, internal model source corpus, or six-criterion bands are changed after any output exists;
- the order-2 internal model is found to leak information about class identity in a way that could inflate edge gain independent of the coupling rule (must be checked by the ablation control before interpreting any pass);
- fewer than 39,026 tokens are generated before the line-template wrap;
- a metric implementation differs from the already-accepted project version reused from `external_naibbe_audit.py` / `external_cardan_audit.py`.

## Interpretation limits

A pass would show only that this specific constructive process can jointly satisfy the six criteria — it would not show that Voynichese was produced this way, does not identify a historical mechanism, and does not bear on language, cipher, or meaning. A failure would not show the six criteria are unsatisfiable in general — only that this specific, disclosed, non-circular construction does not satisfy them jointly; a different internal-structure model, coupling rule, or novelty mechanism might still succeed and would need its own preregistration.

No code was written and no output was computed before this document's design was reviewed. Execution was authorized after Claude's own adversarial self-review (see the note at the top of this document and `logs/2026-09-20-claude-solo-boundary-null-selfreview.md`), not ChatGPT's independent review as originally planned — ChatGPT remains free to audit the design and execution after the fact, exactly as every other mechanism test in this project has been subject to post-hoc independent reproduction.
