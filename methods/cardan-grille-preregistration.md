# Preregistered Cardan-grille mechanism control

Status: **frozen before execution; awaiting Claude's adversarial review**  
Registered: 2026-09-19 21:54 UTC  
Machine-readable source manifest: `data/external/cardan-grille-source-manifest-v1.json`

## Why this mechanism

Steering Committee Meeting #3 chose mechanism controls over further mining of confounded manuscript labels. The next candidate is the Rugg/Cardan table-and-grille family: a prominent, named Voynich pseudo-text proposal, now supplied as an executable generator in Christophe Parisel's 2026 preprint and public repository.

This choice does **not** make the literal Cardan device contemporaneous with the manuscript. Cardano's published grille dates to the sixteenth century, while the Voynich parchment is fifteenth-century. The test therefore addresses a concrete production mechanism and a long-standing Voynich claim, not manuscript dating or authorship. A pass would show that the frozen mechanism can reproduce the statistical joint profile; it would not show that a Cardan grille was historically used.

Primary sources:

- Parisel, *Evidence of Layered Positional and Directional Constraints in the Voynich Manuscript* (arXiv:2604.19762v2, 16 June 2026): <https://arxiv.org/abs/2604.19762v2>
- Frozen implementation, commit `5d50101b57957bc7feaa002cec01d1ce5b2b11d9`: <https://github.com/labyrinthinesecurity/currier-signatures/tree/5d50101b57957bc7feaa002cec01d1ce5b2b11d9>
- Rugg and Taylor, *Hoaxing statistical features of the Voynich Manuscript* (2016): <https://doi.org/10.1080/01611194.2016.1206753>
- Zandbergen, *The Cardan grille approach to the Voynich MS taken to the next level* (2021): <https://arxiv.org/abs/2104.12548>

## Result blinding and source audit

No generator was executed and no project joint-profile value was calculated before this document and its manifest were committed. The preprint's published conclusions and its shipped text logs are necessarily known; the new outcome is whether the frozen outputs survive the project's independently developed profile and held-out tests.

The seven-file repository was inspected statically before execution. It contains Python plus text data, uses only the standard library and NumPy, and contains no subprocess, network, `eval`, `exec`, pickle, or shell calls. Two reproducibility defects were found and are frozen rather than silently repaired:

1. `grille.py` imports `signatures_v26`, which is absent; the repository ships only `signatures_v27.py`. The published Cardan command therefore fails from a clean checkout.
2. The repository has no `LICENSE` file or other explicit software/data license, despite the paper saying the code is freely available. We may inspect and run a local audit, but we will not copy upstream code or data into this repository.

After Claude approves the design, execution may use exactly one documented repair: change the missing module import from `signatures_v26` to the shipped `signatures_v27`. The repaired file's before/after SHA-256 and one-line diff must be recorded. No other upstream change is allowed under version 1 of this preregistration. NumPy's bootstrap RNG must be seeded to `20260919` by a project wrapper so confidence intervals are repeatable; point estimates must remain unchanged.

## Hypothesis card

### Claim

At least one **honest, non-target-informed configuration** in the frozen Parisel Cardan implementation can generate a corpus that jointly matches the Voynich profile: character entropy, learned multi-symbol-unit scale, weak whole-token order, strong cross-token edge prediction, and open vocabulary.

### Alternatives

- **Natural language or constructed language:** positional morphology and discourse continuity may generate the joint profile without a grille.
- **Cipher:** a stateful or nomenclator-like cipher may preserve or introduce cross-token dependencies that a random grille lacks.
- **Other pseudo-text:** self-citation, copying-with-mutation, or another structured generator may produce the profile even if this Cardan family fails.
- **Target-informed table design:** pre-separating pools with Voynich-derived prefix/suffix classes may fit positional statistics circularly. Such configurations are diagnostic sensitivities, not evidence for the primary claim.

### Discriminating prediction

An honest grille configuration must reproduce all six frozen criteria below on the same generated replicate, not merely match one marginal statistic. Random and target-informed controls must behave as labelled. The central prediction is especially demanding at token boundaries: a mechanism that generates words independently should not reproduce Voynich's held-out last-glyph to next-first-glyph gain unless its traversal supplies real cross-token state.

### Failure condition

The claim fails if none of the four English-source configurations below passes all six criteria in at least **16 of 20** frozen-seed replicates. Passing only after looking at results, only in a target-informed configuration, or only after changing a source, threshold, table, traversal rule, tokenizer, or seed is a failure of version 1 and requires a new preregistration.

## Frozen configurations

The four primary configurations are the upstream `G_seq English` sequential traversals at jump probabilities `0.00`, `0.05`, `0.10`, and `0.30`. They are the only shipped non-target-informed variants with explicit cross-token state. Each uses four holes and the upstream defaults otherwise.

Controls and sensitivities:

- `G_seq Random p=0.00` and `p=1.00`: structureless negative controls. Neither may satisfy the full profile.
- `G8 LEARNED-ENGLISH+RANDOM`: honest independent-word grille; expected to fail the edge criterion.
- `G10 LEARNED-RANDOM+RANDOM`: second structureless negative control.
- `G0 SPLIT+RANDOM`, `G1 SPLIT+SHIFT`, `G2 SPLIT+ROTATE`, and `G4 GRADIENT+RANDOM`: target-informed upper bounds. A pass is reported but cannot support the primary claim because Voynich positional structure is built into their pools.
- `G9 LEARNED-VMS+RANDOM`: explicitly circular positive-control sensitivity; excluded from the primary verdict.

The upstream English fallback is a tiled short excerpt and is not acceptable for the primary run. The primary source will instead be the already pinned English EWT surface-token corpus from `data/baselines/document-panel-v1.json` (UD English-EWT commit `4a4d77f599ea53cc405f85d0cec4b2f14f81d42b`, CC BY-SA 4.0), concatenated in frozen train/dev/test file order while preserving explicit document and sentence order. This changes source content, not the Cardan mechanism; both the EWT run and the upstream fallback must be reported so the extension is distinguishable from reproduction.

## Units, sampling, and controls

- Generate 20 replicates per configuration using upstream seeds `42 + 137*i`, `i=0..19`.
- Generate at least 39,026 tokens per replicate. For the project profile, rewrap each token stream to the exact 3,950-line collapsed-EVA line-length template already used by `external_naibbe_audit.py`; truncate only after the final required token. This fixes boundary locations across Voynich and all controls.
- Treat upstream multi-character elements as atomic for the upstream four-signature reproduction and also serialize them without separators for the project's collapsed-EVA view. Report raw-element and serialized-character sensitivity views.
- Run the two random controls through the identical pipeline.
- Preserve every individual replicate. Do not select the best seed.
- Use the project's existing code paths for entropy/BPE/token-order (`voynich-units` commit `956a7c4...`), held-out edge prediction (`external_edge_crossfit.py` / the line-block adapter in `external_naibbe_audit.py`), and vocabulary summaries.

## Six-criterion project profile

A replicate passes only if all are true:

1. Character entropy `H1` is within `3.9763 ± 0.15` bits.
2. Conditional character entropy `H2` is within `2.6897 ± 0.15` bits.
3. The learned-unit dependence-gap minimum occurs at 32 or 64 merges, and the 64-merge gap is between `0.90` and `1.20` bits.
4. Excess whole-token-order share is between `0%` and `2.0%` (weak but non-negative).
5. Held-out last-glyph to next-first-glyph prediction gains at least `0.15` bits per boundary overall and is positive in at least `15/16` fixed line blocks at alpha 1.
6. At least `65%` of word types are singletons.

These are equivalence bands, not claims of universal natural-language ranges. They were fixed from the accepted Voynich profile (`H1=3.9763`, `H2=2.6897`, 64-merge gap `1.0448`, token-order share `0.79%`, edge gain approximately `0.18`, singleton share `69.7%`) before any Cardan output was produced. Exact distances and all failures must be reported; the binary verdict cannot replace the continuous values.

## Upstream four-signature reproduction

Before applying the project profile, reproduce Parisel's Currier A and B calibration and the shipped honest/configuration results using the corrected import. Differences from `signatures_A.txt` and `signatures_B.txt` must be classified as point-estimate, confidence-interval, line-ending, or presentation differences. The paper's four-signature thresholds are reported as an upstream reproduction only; they do not replace the six frozen project criteria.

## Stop conditions

Stop and return to review, without interpreting a mechanism result, if:

- any pinned checksum or commit differs;
- the one-line import repair is insufficient to run the frozen code;
- the EWT checksums or token order cannot be reproduced from the existing manifest;
- a primary output contains fewer tokens than the fixed line template requires;
- a metric implementation differs from the previously accepted project version;
- the missing upstream license would require redistribution rather than local inspection/execution;
- any configuration, band, seed, tokenization, or verdict rule is changed after output inspection.

## Interpretation limits

A pass would establish only that this frozen table-and-grille implementation can reproduce the statistical profile. It would not date the manuscript, identify an author, prove meaningless text, exclude hidden plaintext, or establish use of a physical grille. A failure would narrow these frozen configurations, not all table methods, all hand generators, all hoaxes, or all ciphers. Because the primary configurations use a modern English source as a reproducible structural carrier, historical claims require a separate Latin/Italian source preregistration rather than a post-hoc substitution.

No knowledge-base change will be proposed until Claude has reviewed this design and independently audited either the source repair or the resulting headline values.
