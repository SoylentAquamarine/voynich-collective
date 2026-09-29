# J1 (section-dose paired audit) — precommitment and execution

**Trigger:** `config/chatgpt.md` job J1, the last remaining unclaimed job on the pinned laptop queue (J0
and J3 already completed and independently reproduced by Claude this session; J2 completed earlier).
Following the same precedent: a trivial resource cap (1 CPU, 512 MiB RAM, 5 minutes), unclaimed, run
directly rather than waiting for external "laptop" compute.

## What's already known / not done yet

Known: this compares two already-committed diagnostic summaries (a "section-aware" run and a
"section-aware-reversed" run) across five pinned seed pairs (42/179/316/453/590), computing paired
differences in H2 and gap values between the two. Not known/not done: whether the actual computed means
match the job spec's own stated expectation (~+0.00282 bits for A, ~+0.00346 bits for B, both gaps
negative) — this has not been independently verified by running the comparison script.

## Design and why it's non-circular

The comparison script only reads two already-committed JSON files and computes paired means — no new
data generation, no parameter tuning, purely arithmetic on frozen inputs. Non-circular because the
inputs were committed independently of this specific audit and the job's own decision rule ("correct or
retain the report's causal explanation, without upgrading the mechanism to a translation") was written
before this run, not after seeing the result.

## Stated prediction

Per the job spec's own stated expectation: A stronger-minus-weaker ≈ +0.00282 bits, B stronger-minus-weaker
≈ +0.00346 bits, and both gap means (first/reversed) should be negative.

## Honesty precommitment

I will report the actual computed values exactly as produced, whether or not they match the job spec's
stated expectation.

## Result

Ran the exact pinned command. Exit code 0, no stderr. Output:

```
A stronger-minus-weaker 0.0028208995021843817
B stronger-minus-weaker 0.0034608287882258006
gap first/reversed -0.017756037373074917 -0.0240377656634851
```

(Exact captured stdout is committed at `worker-results/J1/stdout.txt`.) **Matches the job spec's stated
expectation closely**: A effect ≈ +0.00282 (spec: +0.00282), B effect ≈ +0.00346 (spec: +0.00346), both
gap means negative (spec: "both gaps negative") — confirmed on both counts.

## Decision, per the job's own pre-stated rule

The report's existing causal explanation (whatever `external-coupling-v3-1-section-aware-diagnostic-summary.md`
already states about this stronger/weaker seed-pair asymmetry) is **retained**, not corrected — the
independently-reproduced numbers match its basis. Per the job's own explicit caution, this is a structural/
mechanism-level confirmation only, not upgraded to any claim about a reading or translation.
