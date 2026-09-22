# Coupling causal concentration diagnostic: the real mechanism, found by fixing a flawed proxy

Direct follow-up to `external_coupling_order_concentration_diagnostic.py` (PR #42), whose leading hypothesis — order-share excess concentrates in pairs where the next token's first character is one of the 4 coupling-target initials (`o`, `q`, `C`, `S`) — was reported not confirmed. That report's own caveats named the likely flaw: grouping by which *letter* a token happens to start with conflates two different things, since ordinary Naibbe output can start with any of those 4 letters by chance, with or without coupling ever touching it. This diagnostic fixes that by conditioning on the real causal event instead: did `apply_coupling`'s `rng.random() < beta` check actually fire for that token?

## Method

Modified `apply_coupling` to also return, per token, whether coupling fired (not just the resulting string). Measured collapsed-vocabulary mutual information between adjacent tokens at the coupling-output stage itself (before boundary-shift or substitution touch anything, since a shift merges and re-splits tokens, destroying which output token traces back to which coupling event) — split into pairs where the *next* token's coupling fired, versus pairs where it didn't.

## Result

| | MI (bits) | n pairs |
|---|---:|---:|
| All pairs, coupling-output stage | ~2.43 (mean) | ~80,700 |
| **Coupling fired** for next token | **2.692** (mean) | ~40,400 (≈50.1% of pairs, as expected at β=0.5) |
| Coupling **did not fire** | **2.223** (mean) | ~40,350 |
| Full pipeline (post shift+substitution) | 0.960 (mean) | ~80,700 |

Every one of 5 seeds shows the same pattern, consistently: MI is substantially and reliably higher (~0.47 bits) when coupling fired than when it didn't. This is the confirmation PR #42's flawed proxy failed to find — checked directly rather than inferred from the wrong signal.

## Interpretation

**This resolves the mechanism, and explains PR #42's null result as a measurement artifact, not a real absence of effect.** When coupling fires, a token's first character becomes a deterministic function of the previous token's last character, collapsed onto one of only 4 possible values — this genuinely raises that token's predictability from its predecessor, exactly as coupling was designed to do (it is, after all, the mechanism responsible for this project's edge-prediction criterion passing so robustly). PR #42's proxy — grouping by the resulting letter rather than the triggering event — mixed in a large population of tokens that happened to start with one of those letters through ordinary chance, diluting and even inverting the apparent effect.

**This also clarifies the earlier interaction-vs-main-effect correction** (the addendum to PR #40's report): coupling's raw, causal contribution to token-to-token predictability is large at its own output stage (~0.47 bits between fired and not-fired pairs) but the full pipeline's final order-share only moves by a small amount (~0.003, from the earlier decomposition) once boundary-shift and substitution have run. The shift/substitution process itself contributes substantial MI on its own (full-pipeline MI ≈0.96 bits, versus baseline coupling-stage MI ≈2.43 — note these aren't directly comparable in scale since the token population and cap-2000 collapse differ substantially post-transformation, but the qualitative point holds: a great deal of raw predictability is scrambled away by the shift/substitution process, and only a fraction of coupling's own contribution survives to the final measured statistic).

## What this does not resolve

This still doesn't fully explain why hybrid-shift-v2-substitution's order-share sits right at the 0.02 ceiling even *without* coupling (`hybrid_novelty_only`, 7/20 pass) — that remaining baseline predictability comes entirely from the shift/substitution mechanism's own combinatorics, a separate question from coupling's contribution, and not addressed here.

## Provenance

- Implementation: `data/scripts/external_coupling_causal_concentration_diagnostic.py`, reusing `apply_boundary_shift_v2`, `apply_substitution_topup`, and `expand` directly from the merged hybrid-shift-v2-substitution script; only `apply_coupling` was extended (not modified in behavior, only in what it returns) to track the firing event.
- Full replicate data: `data/derived/external-coupling-causal-concentration-diagnostic-summary.json`.
