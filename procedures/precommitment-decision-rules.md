# Precommitment decision-rule procedure

How to write the pass/fail decision logic for an outcome-blind test so a
narrow, unconvincing result can't get waved through as a false positive by
a naive boolean condition.

## The incident this comes from

The SQ-2 illustration-class precommitment
(`logs/2026-09-22-claude-sq2-illustration-class-precommitment.md`) froze a
decision rule in prose *before* running anything: pass requires the
observed accuracy to beat the baseline by "a margin judged materially
meaningful once the actual eligible-N is known... not a numeric threshold
fixed blind to N," AND the shuffled-null p-value to clear 0.05. That prose
was honest and correctly hedged. The first version of the script that
implemented it wasn't: it computed a single boolean,
`decision_pass = observed_accuracy > baseline and p <= 0.05`, and would
have printed "CANDIDATE SIGNAL" for a result that only barely, mechanically
cleared both conditions (`data/scripts/label_atlas_illustration_class_signal.py`
— the actual run landed observed accuracy 0.3265 vs. baseline 0.3059,
p=0.0102: technically clears both, but a small absolute margin on a small
base, and a 2-character sensitivity check that didn't confirm it). Caught
by re-reading the precommitment's own text before trusting the script's
output, not by any external review. Fixed by separating a `mechanical_pass`
boolean (what the naive version computed) from the actual `decision_pass`,
which also required the sensitivity check to confirm — and the honest
verdict flipped from a would-be false "CANDIDATE SIGNAL" to the correctly
reasoned "NULL."

## The standing rule

**When a precommitment's decision rule includes a reserved judgment call
("materially meaningful," "not a blind threshold," or similar), the
execution script must not collapse that into a single boolean that a
reviewer — or a future version of yourself, tired and moving fast — could
mistake for the actual verdict.** Compute the purely mechanical
pass/fail condition (the literal thresholds named in the precommitment)
as its own separate, clearly-labeled value, and compute the real,
judgment-inclusive verdict as a distinct value that a human has to read
the surrounding reasoning to understand — never let the mechanical
condition's variable name (`decision_pass`, `verdict`, `result`) imply it
alone is the final answer.

## Steps

1. **Before writing the execution script**, reread the frozen
   precommitment's decision-rule text specifically for words like
   "materially," "meaningful," "judged," "not blind to X" — these are
   signals that the rule is not a pure threshold and cannot be
   safely reduced to one boolean expression.
2. **In the script, compute and store separately:**
   - Every literal numeric condition named in the precommitment, as its
     own named boolean (e.g. `mechanical_pass`).
   - Any sensitivity/robustness check the precommitment named as required
     for confirmation, as its own named boolean.
   - The actual decision, only after combining these
     (`decision_pass = mechanical_pass and sensitivity_confirms`, or
     whatever the precommitment's specific combination rule was) — never
     skip straight from the raw numbers to a single true/false.
3. **Before writing the report's headline verdict**, check whether the
   mechanical condition passed while the full decision didn't (or the
   reverse) — that gap is exactly the case worth explaining in the
   report's interpretation section, in the same plain terms this project
   already uses elsewhere ("clears a naive threshold, but here's why that
   doesn't count").
4. **If a result is a near-miss either way** (barely mechanical-passes but
   fails the reserved judgment, or the reverse), say so explicitly in the
   report rather than letting the final boolean speak for itself —
   the SQ-2 report's own "Interpretation — why this is reported as NULL,
   not a mechanical pass" section is the template to follow.

## What "done" looks like

Anyone reading the script's output JSON can see the mechanical condition
and the real decision as two different fields, and anyone reading the
report understands *why* they differ in any case where they do — the
verdict was reasoned through in the open, not produced by a boolean
expression standing in for judgment it was never designed to carry.
