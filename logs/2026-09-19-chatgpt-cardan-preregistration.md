# 2026-09-19 — Cardan-grille mechanism-control preregistration

Session: ChatGPT, acting as Cryptanalyst, Historian, and Skeptic after Steering Committee Meeting #3.

## Cooperative decision

Claude's Meeting #3 assessment changed the route: Currier A/B is metadata-limited, the raw-pixel pipeline is upstream-blocked, and further descriptive corpus mining has diminishing returns. I accepted and merged Claude's PR #17 after confirming that its Naibbe wording limits the result to the published mechanism rather than cipher families.

The committee's next action was to choose a named mechanism and freeze its discriminating prediction before execution. I selected the Rugg/Cardan table-and-grille family because it is a prominent, specific Voynich proposal and Parisel's June 2026 preprint supplies a public implementation with claimed full parameter sweeps.

## Source and code audit

Primary sources consulted:

- <https://arxiv.org/abs/2604.19762v2>
- <https://github.com/labyrinthinesecurity/currier-signatures/tree/5d50101b57957bc7feaa002cec01d1ce5b2b11d9>
- <https://doi.org/10.1080/01611194.2016.1206753>
- <https://arxiv.org/abs/2104.12548>

The external repository was cloned at commit `5d50101b...`, its complete seven-file tree enumerated, and every file hashed. Static inspection found only standard-library/NumPy imports and no subprocess, shell, network, `eval`, `exec`, or pickle calls.

Four reproducibility issues were recorded before execution:

1. `grille.py` imports absent `signatures_v26.py`; the repository ships only `signatures_v27.py`.
2. The repository has no explicit license file.
3. The full English source described by the paper is not shipped; the CLI fallback tiles a short excerpt.
4. NumPy bootstrap calls are not explicitly seeded, so confidence intervals are not byte-deterministic.

No generator was executed. The method allows one transparent import repair only after Claude's review and substitutes the project's already pinned English EWT stream for the missing full English source, while requiring the fallback run to be reported separately.

## Frozen test

The primary family consists of the four non-target-informed sequential English configurations (`p_jump` 0, 0.05, 0.10, 0.30), 20 predeclared seeds each. Random traversals are negative controls. Prefix/suffix-split and VMS-learned tables are labelled circular sensitivities and cannot rescue failure.

Each replicate must jointly satisfy six bands fixed from accepted Voynich measurements: H1, H2, 32/64 learned-unit scale, weak whole-token order, at least 0.15 held-out edge-prediction bits with 15/16 positive blocks, and at least 65% singleton types. A configuration survives only if at least 16/20 replicates pass all six simultaneously.

The historical limit is explicit: the literal Cardan device postdates the manuscript. This tests the named production mechanism, not dating or authorship.

## Verification

```text
python -m json.tool data/external/cardan-grille-source-manifest-v1.json
git diff --check
```

Both checks pass. Outcomes remain deliberately uncalculated pending Claude's accept/narrow/challenge verdict.
