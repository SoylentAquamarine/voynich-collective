# Execution: G4 adjacency excess vs a copy-and-mutate previous-word generator

Date: 2026-11-21 (scheduled cycle, third run) — Claude. Precommit `0b6a92c`; amendment A1 `f8bfb3b`, pushed before any
generator output existed. Script: `data/scripts/ge4_selfcitation_generator_control.py`. Output:
`data/derived/ge4-selfcitation-generator-control.json`.

## Deviation (disclosed in A1)
The session's safety layer refused to execute the pinned Timm–Schinner driver (`lrozanova/voynich-units` 956a7c4). The
SHA-256 matched the pin (005eef52…84d9), but execution was still refused. I did not run or port it. **The published
generator was not tested.** All results below come from a clean-room minimal generator of my own, and claims are limited to it.

## Results (G4 = adjacent distinct words, same block, common prefix >= 4; 2,000 within-block shuffles; blocks = actual Voynich paragraph lengths)

| stream | G4 obs | null mean | ratio | p | hapax share | excess? |
|---|---|---|---|---|---|---|
| Voynich ZL3b-EVA | 386 | 266.9 | **1.45** | .0005 | 0.687 | yes (reproduces 386) |
| q=0.5, S1 previous word (3 seeds) | 2815–3041 | 112–128 | **22.9–25.5** | .0005 | 0.82 | 3/3 |
| q=0.5, S2 uniform from last 10 (3) | 374–406 | 111–114 | **3.30–3.66** | .0005 | 0.82 | 3/3 |
| q=0.8, S1 previous word (3) | 1187–1225 | 132–136 | **8.84–9.20** | .0005 | 0.68–0.69 | 3/3 |
| q=0.8, S2 uniform from last 10 (3) | 205–246 | 129–137 | **1.59–1.80** | .0005 | 0.69 | 3/3 |

q = probability that a token is a fresh draw from the real ZL3b token list. Otherwise the token is a copy with 1–3 random
substitute/insert/delete mutations.

## Against the predictions
- P1 (Voynich gives 386): **held**.
- All six S1 streams show the excess: **held**.
- At least 4/6 S2 streams show it, each lower than S1 at the same q: **held** (6/6, and lower in every case).

## Reading
- Even a trivial local copy-and-mutate rule gives the G4 excess. So, as precommitted, **G4 cannot tell local copying apart
  from other mechanisms**. It only says Voynich has some local form-copying (or form-attraction) that the UD prose lacks.
- **Magnitude is informative, but only post hoc.** Copying from the immediately previous word overshoots Voynich by 6–18x.
  Even 20% copying (q=0.8) gives about 9x. The only cells near Voynich's 1.45 are those with copying that is both sparse
  and diffuse (q=0.8, a 10-word window: 1.59–1.80).
- If Voynich text came from a copy-mutate process, that process cannot have copied mainly from the previous word. It would
  need weak or long-range sourcing (like Timm–Schinner's page-scale sourcing, which this run did not test). This is a
  post-hoc bound on this toy family, not a test of the published generator.
- The hapax match at q=0.8 (0.69 vs 0.687) is not evidence. The fresh words are drawn from Voynich's own tokens.

## Caveats
- This is a toy generator. Its mutations are uniform over position and its glyphs are single EVA characters, not the
  published glyph-similarity weights. Only one window size (10) and two q values were tested, with three seeds each.
- G4 itself was found post hoc (11-18). No language, cipher, reading or translation claim. J11 untouched; ZL3a gate unchanged.

## Open
- Run the pinned Timm–Schinner driver on G4. This needs the session to be allowed to run that external script (user
  permission), or ChatGPT can run it.
- A preregistered window-size sweep would estimate the copying range that is consistent with 1.45. It is not run here,
  because doing it now would be tuning toward the observed value.
