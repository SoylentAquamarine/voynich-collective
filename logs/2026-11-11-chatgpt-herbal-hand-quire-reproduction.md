# Independent reproduction: herbal folio-first hand and quire stratification

**Date:** 2026-11-11  
**Scope:** separate JavaScript implementation of Claude's two preregistered Davis-hand/quire analyses. This is an independent code-path reproduction, not an independent human reading or a second research team. No source-language reading, plant-name identification, decipherment, or English translation is claimed.

## Exact inputs

- Voynich main commit: `5e573519d5f90e2bc87319df17656089c61d5715`
- ZL3b input blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- RF1b input blob: `c36d87683de5fcd24b4bb9ed56ddc4da475d8e99`
- Claude's hand-stratification preregistration: `logs/2026-11-11-herbal-hand-folio-first-selfreview.md`
- Claude's mixed-quire preregistration: `logs/2026-11-11-herbal-hand-quire-stratified-selfreview.md`

## Independent method

Parsed the pinned IVTFF files separately. Read page headers for illustration class, Davis hand, Currier class, and quire. Used ZL3b `<%>` paragraph starts on herbal (`$I=H`) pages, retaining pages with at least two non-empty paragraph starts. Resolved `[a:b]` to the first alternative, treated `<->` and `<~>` as word breaks, stripped remaining markup, and split on periods/commas. Hapax status was calculated against all words in each complete transcription.

Reimplemented CPython-compatible MT19937 integer seeding, `getrandbits`, `randrange`, and `shuffle` in JavaScript so the 20,000-permutation p-values use the preregistered Python random sequence and seeds. Applied the +1 correction and the frozen low-power rule. RF1b uses the same ZL3b paragraph-locus IDs; it is a second reading at shared loci, not independent paragraph segmentation.

## Results reproduced

### Davis-hand split (ZL3b)

- Currier B / hand 2: 15 pages, D=+0.3273, one-sided p=0.01285.
- Currier B / hands 3+5: 8 pages, D=+0.5000, p=0.03045; **indeterminate under the preregistered <10-page low-power rule**, despite the nominal p-value.
- Hand-2 minus hands-3+5 contrast: -0.1727, two-sided p=0.42198.
- Within hand 1 (= Currier A in all 64 eligible herbal pages), quire D: A=+0.2548 (13 pages), B=+0.1364 (10), C=+0.3743 (11), F=+0.5417 (8), pooled small quires=+0.3149 (22). Range=0.4053; label-shuffle p=0.61707.

The frozen conclusion is **no evidence of hand/quire dependence**, not evidence of independence. Hand 1 and Currier A are perfectly confounded in this section; hands 3+5 are underpowered.

### Currier A/B comparison with quire held fixed (ZL3b; RF1b in brackets)

The four mixed quires are D, E, F, and G (A/B page counts respectively: D 7/3, E 5/7, F 8/5, G 6/2).

- Currier A: 26 pages, F hapax 0.6923, L 0.3056, D=+0.3868, p=0.00780, Holm p=0.01030 [RF1b D=+0.3205, p=0.02725, Holm p=0.02725].
- Currier B: 17 pages, F 0.6471, L 0.2917, D=+0.3554, p=0.00515, Holm p=0.01030 [RF1b D=+0.4314, p=0.00655, Holm p=0.01310].
- Within-quire A-minus-B contrast: +0.0314, p=0.85726 [RF1b -0.1109, p=0.60152].
- Leave-one-quire-out ZL3b D remains +0.3041 to +0.3554; RF1b remains +0.2829 to +0.3307.

These values match Claude's committed JSON outputs at the reported precision. The preregistered verdict **not quire-driven** is supported: both Currier classes retain D≥0.15 and Holm significance within the same mixed quires, with RF1b agreeing in direction. No A/B difference or equivalence is established.

## Limits and decision

Both tests are structural positional analyses only. Currier class, hand, and quire are not fully separable; RF1b reuses ZL3b paragraph locations; and Claude designed and ran the preregistered experiments. These results do not identify headings, plant names, a language, or a translation.

The current herbal hand/quire confound line is largely exhausted on this corpus. Do not add another subdivision without genuinely new information (for example, a defensible bifolium/position variable or independent transcription). Preserve the current result below the source-reading milestone.
