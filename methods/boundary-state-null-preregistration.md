# Preregistered boundary-state constructive null

Status: **frozen before execution; awaiting Claude's adversarial review**  
Registered: 2026-09-20 01:51 UTC  
Machine-readable manifest: `data/external/boundary-state-null-manifest-v1.json`

## Why this test

Naibbe, Cardan-grille, and self-citation now provide three distinct mechanism controls. The self-citation result is especially useful: it has genuine local copy/mutation state and nearly matches Voynich's adjacent edit-similarity excess, yet produces essentially zero held-out last-glyph → next-first-glyph gain. Claude's independent review also corrected the full profile: every faithful self-citation seed fails the joint six-criterion rule, including the real 65% hapax floor and the 0.90–1.20-bit learned-unit-gap magnitude.

That changes the next question. A fourth arbitrary historical mechanism would add little. The sharper test is an explicitly **constructive adversarial null**: begin with a known cipher that already matches the non-discriminating half of the profile, then add the two properties repeatedly named as missing—boundary-specific state and continuing rare-form generation—using transparent rules frozen before output inspection.

This test is intentionally target-aware at the level of accepted criteria. It is not evidence for a historical Voynich mechanism. Its purpose is to ask whether the six-number joint profile can be manufactured by a small, inspectable extension without estimating any Voynich transition table or copying any Voynich token.

## Result blinding

Before this document and manifest were committed:

- the accepted Naibbe and Voynich reference values were already known;
- the proposed transformation was specified from those known failures;
- no boundary-state/novelty output was generated;
- no transformed stream was passed to entropy, BPE, token-order, edge, or vocabulary scoring;
- no parameter was selected from a transformed outcome.

The external Naibbe code and sources were inspected and checksum-pinned in the earlier accepted audit. `data/scripts/audit_boundary_state_null.py` verifies the frozen source, thresholds, alphabet, inverse serialization, seeds, and manipulation rules without generating a transformed stream or calculating a project outcome.

## Hypothesis card

### Claim

A fixed two-operation postprocessor applied to a published Naibbe ciphertext can jointly reproduce the six frozen Voynich-profile criteria in at least 16 of 20 preregistered replicates, without using Voynich transition probabilities, Voynich tokens, or per-replicate parameter fitting.

### Alternatives

- **Meaningful-language structure:** the joint profile may require morphology, syntax, or discourse continuity not reproduced by a boundary rule plus novelty.
- **Richer cipher state:** a cipher may need homophonic, nomenclator, null, or multi-token state beyond the transparent postprocessor tested here.
- **Structured pseudo-text:** a copying or combinatorial generator may require positional and page-level constraints not represented here.
- **Metric construction:** if the primary passes, the six-number profile is constructible and cannot by itself discriminate meaningful language, cipher, or pseudo-text.

### Discriminating prediction

The primary transformation must pass all six accepted bands on the same replicate. Boundary coupling and novelty must also pass their separate manipulation checks against matched-seed controls. A pass would demonstrate that a simple mechanical extension can construct the profile. A valid failure after both manipulations work would show that adding the two missing axes is still insufficient because one or more other criteria move out of range.

### Failure condition

Version 1 fails if fewer than **16 of 20** primary replicates pass all six criteria, provided both manipulation checks succeed. Sensitivity configurations cannot rescue a primary failure. If a manipulation check itself fails, the version-1 construction is **invalid/inconclusive**, not evidence that boundary-state or novelty mechanisms generally fail.

## Frozen source

- External repository: `lrozanova/voynich-units`, commit `956a7c4fc39981f4d116fa3f4edfccce6d065571`.
- Naibbe driver: `analysis/reproduce_naibbe_control.py`, SHA-256 `df9f01ed8f5eefa03830e4e31904d7163e902119988e9138074ac5cb1e9ecd8e`.
- Cipher tables: `data/controls/naibbe/naibbe_tables.json`, SHA-256 `46c1235ad1dfdcaabd7866895c0557bb0e98c465f3e324fdb10dca150933826a`.
- Plaintext carrier: `voynich_decipherment_repro_bundle/decipherment_attack_v6/lm_corpora/caesar_la.txt`, SHA-256 `84ac8411841a4d8f5f4a49b6a2cd1f466917c6a5af72916d5e0b2b1ecb2f659c`; the same Caesar preparation already used by the accepted Naibbe audit.
- No upstream file will be changed or redistributed.

Each replicate encrypts the complete frozen Caesar stream with Naibbe cipher seed `42 + 137*i`, for `i=0..19`. The postprocessor uses a separate RNG seed `1000042 + 137*i`. If any generated stream is too short for the already accepted entropy, BPE, or 3,950-line targets, execution stops before scoring.

## Atomic representation

The transformation operates on the collapsed-EVA atomic view already used for the accepted Naibbe comparison. Raw Naibbe tokens are collapsed with the external bundle's exact nine substitutions. The frozen atomic alphabet is:

```text
CEIKNPSTadefgiklmnopqrstxy
```

After transformation, atomic strings are serialized back to raw EVA through the exact inverse map `C→ch`, `E→ee`, `I→in`, `K→ckh`, `N→iin`, `P→cph`, `S→sh`, `T→cth`; lowercase atoms serialize as themselves. The audit must verify `collapse(expand(atom)) == atom` for every frozen atom. Metrics then run through the unchanged accepted external code path.

## Frozen transformation

Process Naibbe tokens in their original order. Maintain the previous emitted atomic token and a set of emitted atomic token types.

### Operation 1: boundary coupling

For every token after the first, draw once from the postprocessor RNG. With probability `beta`, replace the current token's first atomic glyph with:

```text
target(last) = [o, q, C, S][index(last in frozen_alphabet) mod 4]
```

The four target initials are the four common initial classes in the already published Naibbe control, chosen to make the manipulation operational without using any Voynich transition matrix. The mapping is fixed globally and never re-estimated by replicate, block, or result.

### Operation 2: novelty injection

After boundary coupling, if the candidate atomic token has already been emitted and contains at least two atoms, draw once from the same RNG. With probability `nu`, search deterministically for an unseen one-substitution variant while protecting the boundary-linked first atom:

1. Draw a starting noninitial position uniformly from positions `1..len(token)-1`.
2. Draw a starting alphabet step uniformly from `1..25`.
3. Visit noninitial positions cyclically from that start. At each position, try all 25 alternative frozen atoms cyclically from the starting alphabet step.
4. Accept the first candidate not already in the emitted-type set.
5. If all `25 × (len(token)-1)` candidates have already appeared, retain the unmodified candidate.

Token length in atomic units never changes. The first atom is never changed by novelty injection, so the boundary manipulation remains intact. The final emitted atom—whether mutated or not—becomes the state for the next token.

## Configurations and seeds

### Primary

- `beta=0.50`, `nu=0.75`
- 20 replicates with the frozen paired cipher/postprocessor seeds.
- This is the only configuration that can determine the primary PASS/FAIL verdict.

### Matched-seed controls

- Baseline: `beta=0.00`, `nu=0.00`.
- Edge-only: `beta=0.50`, `nu=0.00`.
- Novelty-only: `beta=0.00`, `nu=0.75`.
- Each control uses all 20 matched seeds.

### Reduced-N sensitivities

Using the first five frozen seeds only:

- weaker edge: `beta=0.25`, `nu=0.75`;
- stronger edge: `beta=0.75`, `nu=0.75`;
- weaker novelty: `beta=0.50`, `nu=0.50`;
- maximal novelty: `beta=0.50`, `nu=1.00`;
- ceiling construction: `beta=1.00`, `nu=1.00`.

Sensitivities describe parameter behavior and cannot rescue primary failure.

## Manipulation checks

Before interpreting the joint verdict:

1. **Boundary check:** edge-only must exceed its matched baseline edge gain in at least 16/20 seeds, pass the frozen edge threshold in at least 16/20 seeds, and have at least 15/16 positive blocks in each counted pass.
2. **Novelty check:** novelty-only must exceed its matched baseline hapax share in at least 16/20 seeds and pass the frozen 65% hapax floor in at least 16/20 seeds.

If either check fails, report `INVALID_CONSTRUCTION` and do not interpret the primary joint failure as evidence against a mechanism family. Still publish every replicate and explain which intended operation failed.

## Evaluation units and six criteria

- Preserve the full transformed token stream for entropy and BPE targets.
- Rewrap the first required tokens to the exact accepted 3,950-line collapsed-EVA line-length template before held-out edge scoring; all replicates therefore have identical line boundaries.
- Use the unchanged `voynich-units` `battery()` path and the accepted 16-block alpha-1 edge evaluator.
- Preserve every replicate; do not select a best seed.
- A replicate passes only if all six frozen Cardan-protocol bands are true:
  1. `H1 = 3.9763 ± 0.15` bits;
  2. `H2 = 2.6897 ± 0.15` bits;
  3. BPE minimum at 32 or 64 merges **and** k64 gap `0.90–1.20` bits;
  4. whole-token-order share `0–2.0%`;
  5. held-out edge gain `≥0.15` bits/boundary and `≥15/16` positive blocks;
  6. hapax share `≥65%`.

The primary verdict is `PASS` only if both manipulation checks succeed and at least 16/20 primary replicates pass all six. Otherwise it is `FAIL` or `INVALID_CONSTRUCTION` as defined above.

## Stop conditions

Stop before interpreting results if:

- any pinned commit or checksum differs;
- the alphabet or collapse/expand round trip differs;
- the external driver cannot reproduce its already accepted baseline path;
- a stream is shorter than any accepted target;
- the exact line template cannot be reproduced;
- any transformation rule, parameter, seed, threshold, or verdict rule changes after output inspection;
- evaluation code differs from the accepted Naibbe/Cardan implementations.

Any change requires a version-2 preregistration and a fresh execution embargo.

## Interpretation limits

A PASS would show only that the six summary criteria are mechanically constructible from a known ciphertext plus two explicit postprocessing rules. It would not show that the Voynich manuscript used Naibbe, this mapping, this novelty rule, or any historically plausible equivalent.

A valid FAIL would narrow only this frozen construction. It would not prove language, reject ciphers or pseudo-text, or validate edge/vocabulary as a universal discriminator. An `INVALID_CONSTRUCTION` result would say only that version 1 failed to instantiate its intended controls.

No outcome will enter the knowledge base until Claude has reviewed this design and independently reproduced or audited the decisive output.
