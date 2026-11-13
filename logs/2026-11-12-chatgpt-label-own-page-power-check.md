# Independent reduced-budget sensitivity check for the label own-page test

**Date:** 2026-11-12 (ChatGPT V8 run; append-only research record).  
**Status:** independent reduced-budget reproduction of Claude's post-hoc power analysis, not a new confirmatory test.

## Pinned inputs and parser check

- \`data/ZL3b-n.txt\` — Git blob \`2a4533ab9bdfa85db9bad602d590978953055df1\`; 53 eligible pages / 1,054 label tokens.
- \`data/RF1b-er.txt\` — Git blob \`85e5d4bcfe270dd4fb54cc477b1b5900020fa3f2\`; 52 eligible pages / 1,049 label tokens.

The separate V8 parser reproduced the eligible-page and label-token counts. At q=0 it also reproduced the observed exact-hit totals (ZL3b 114; RF1b-er 100) and analytic within-stratum null means (primary I: 88.347 / 78.164; secondary I×L: 104.647 / 94.364).

## Independent sensitivity design

- Same planted-anchor model and SHA-256 key as \`data/scripts/label_own_page_power.py\`: \`20261113|q|rep|page|label-token-index\`; only label tokens absent from their own page's text are eligible for planting.
- Same frozen pass rule: primary within-I p<0.01 in both inputs AND secondary within-I×L p<0.05 in both.
- Independent implementation: JavaScript/V8 parser and score matrix; Node-compatible SHA-256 planting; xorshift32 Fisher–Yates within-stratum permutations, not NumPy PCG64.
- Reduced budget: 50 replicates and 500 permutations per null (rather than Claude's 200 replicates and 2,000 permutations); seed 20261113; q = 0, 0.01, 0.0125, 0.02.
- Executable check: \`node data/scripts/chatgpt_label_own_page_power_check.js\`. The script refuses inputs whose Git blob IDs differ from the two pins above.

## Results

| Uniform anchor q | Passes | Estimated power | Mean planted tokens ZL3b / RF1b-er |
|---:|---:|---:|---:|
| 0 | 0/50 | 0% | 0 / 0 |
| 0.01 | 33/50 | 66% | 9.38 / 9.62 |
| 0.0125 | 47/50 | 94% | 12.28 / 12.50 |
| 0.02 | 50/50 | 100% | 19.82 / 19.84 |

At q=0.0125, mean primary p-values were 0.0028 (ZL3b) and 0.0041 (RF1b-er); mean secondary p-values were 0.0055 and 0.0137. At q=0.02 they were 0.0021 / 0.0026 and 0.0028 / 0.0051 respectively.

Claude's higher-budget run reported 184/200 (92%) at q=0.0125 and 200/200 at q=0.02. The reduced-budget independent run is concordant within Monte Carlo variation; it does not claim byte-identical RNG output.

## Interpretation and limits

The q=0 run passes 0/50, as required by the observed data's failure of the frozen rule. Under this *uniformly spread, planted-on-top-of-real-data* model, the threshold is around 1–1.25% of eligible label tokens (roughly 11–13 extra own-page hits). This qualifies the negative result; it does not reverse it.

The simulation does not model anchors concentrated on a few pages or illustration classes. Its fine-grid threshold is post hoc. The preregistered label test still fails under both RF input variants; the RF1b-e versus preregistered RF1b-er mismatch remains a separate Director decision. No label referent, plant identity, source-language reading, or English translation is established.

No Yale images or restricted corpus material were accessed. This is a text-only statistical sensitivity check.
