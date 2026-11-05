# 2026-11-05 — Execution: design A1 on a fresh, seeded random folio set

Precommitment: `logs/2026-11-05-showthrough-a1-fresh-heldout-selfreview.md` (pushed in a27bca6,
~12:45 UTC, before the draw, any code, or any fetch; the "~10:30 UTC" in that file is wrong, and
nothing ran before it was pushed). Script + workflow: 2dc8322. Run: Actions run 42030849755
(results commit b926478). 30 Yale 1,200-px canvases fetched on the runner; **all 30 hashes equal
the manifest**; no images committed. Output: `research/2026-11-05-showthrough-a1-fresh-heldout.csv`.

## Pre-run synthetic self-test (disclosed; design unchanged)

Offline only, on the drawn page names with synthetic images: planted mirrored same-leaf image at
alpha 0.08 → P1 10/10, P2 10/10; alpha 0 → P1 5/10, P2 0/10. A denser synthetic (own "paint"
covering most of the page) at alpha 0.06 gave P2 4/10. A1's dilated own-paint mask leaves little
vellum on crowded pages, so the test loses power there. Nothing was changed.

## Draw (seed 20261105; 119 eligible; leaf-disjoint)

f32v, f26v, f106v, f47v, f114r, f7r, f9r, f82v, f55v, f103v. These are herbal, biological
(f82v) and recipe-section (f103v, f106v, f114r) pages. 27 controls each.

## Result (darkness, mirrored)

| target | same | facing | max ctl | z same | P1 | P2 |
|---|---:|---:|---:|---:|:-:|:-:|
| f32v | 0.3677 | 0.0956 | 0.1287 | +14.4 | y | y |
| f26v | 0.1628 | 0.1093 | 0.0992 | +6.2 | y | y |
| f106v | 0.0823 | 0.0784 | 0.0674 | +3.3 | y | y |
| f47v | 0.1874 | 0.1137 | 0.1058 | +6.4 | y | y |
| f114r | 0.0766 | 0.0873 | 0.1149 | +0.4 | n | n |
| f7r | 0.2409 | 0.1242 | 0.0964 | +13.2 | y | y |
| f9r | 0.2161 | 0.0764 | 0.1524 | +4.5 | y | y |
| f82v | 0.0772 | 0.0647 | 0.0737 | +3.2 | y | y |
| f55v | 0.1091 | 0.0420 | 0.0909 | +3.9 | y | y |
| f103v | 0.1764 | 0.2064 | 0.2456 | +0.3 | n | n |

**P1 8/10 (need ≥ 8), P2 8/10 (need ≥ 6). Decision: "A1 same-leaf dominance replicates on a
fresh random folio set."** P1 is exactly at threshold. P2 clears it by two.

Predictions: P1 held (at threshold). P2 was predicted 6–7/10 and came in at 8/10, better than
predicted.

## Reading it honestly

- Both failures are text-dense recipe pages (f114r, f103v). On f103v the controls themselves
  run high (mean 0.16), so dense regular text layout correlates with any page there. f106v
  passes by small margins (0.0823 vs facing 0.0784, vs control max 0.0674).
- Facing pages also sit above their controls on several targets (z +2.5 to +4.0 on f26v, f47v,
  f7r, f106v). That is descriptive only. It may be weak contact offset or shared neighbouring
  layout, and it was not tested.
- Chroma (secondary, descriptive): same > facing 8/10, same > max control 4/10. This fits the
  synthetic finding that chroma has low power.
- Scope: A1 detects a through-the-leaf (mirrored same-leaf) image on most randomly drawn Yale
  pages. That supports the A1 method as a detector beyond the 30 pages it was adopted on, and it
  weakens the "only under a same-run amendment" caveat. It does **not** change the 2026-11-05
  ten-folio held-out result. That still passes only under A1, at threshold, and the original
  097cba5 design still does not replicate. Cite all three together. No cell is scored, and no
  chronology, language, reading or translation claim follows.
