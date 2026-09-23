#!/usr/bin/env python3
"""Execute the preregistered coupling-v3 (lower, fixed beta) pilot and primary audit.

Implements data/external/coupling-v3-lower-beta-hybrid-manifest-v1.json exactly as frozen.
Identical to external_hybrid_shift_coupling_v2_substitution_novelty_null_audit.py (coupling-v2,
PR #71) EXCEPT beta becomes a swept/selected parameter instead of the fixed 0.5 -- see
logs/2026-09-23-claude-coupling-v3-lower-beta-selfreview.md for the full design reasoning.
Everything else (coupling-v2's identity-mapping target rule, boundary-shift-v2, substitution
top-up, six frozen criteria, evaluation code) is unchanged.

Two modes:
  --pilot         run the 3-seed-per-beta calibration grid from the manifest, report mean edge
                   gain / H2 / order-share per beta. No selection or freezing happens here --
                   read the printed table and pick the lowest beta clearing the edge criterion.
  --beta VALUE    run the full 20-seed primary evaluation at the selected beta, plus the same
                   boundary/novelty manipulation checks coupling-v2 used, plus the H2-headroom
                   comparison against coupling-v2's own primary configuration (hardcoded below,
                   from PR #71's committed summary -- not recomputed, since coupling-v2 itself is
                   unchanged and already verified).

Usage:
    python data/scripts/external_coupling_v3_lower_beta_pilot_and_primary_audit.py <units_repo> --pilot
    python data/scripts/external_coupling_v3_lower_beta_pilot_and_primary_audit.py <units_repo> --beta 0.20
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import random
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-coupling-v3-lower-beta-audit-summary.json"
MANIFEST_PATH = ROOT / "data" / "external" / "coupling-v3-lower-beta-hybrid-manifest-v1.json"
REFERENCE_PATH = ROOT / "data" / "external" / "reference" / "boundary-state-null-baseline-edgeonly-reference.json"

ATOMIC_ALPHABET = "CEIKNPSTadefgiklmnopqrstxy"
EXPAND_MAP = {"C": "ch", "E": "ee", "I": "in", "K": "ckh", "N": "iin", "P": "cph", "S": "sh", "T": "cth"}
COLD_START_TOKENS = 5
SPARSE_CONTEXT_MIN = 20

SIX_CRITERIA = {
    "H1_bits": {"center": 3.9763, "tol": 0.15},
    "H2_bits": {"center": 2.6897, "tol": 0.15},
    "learned_units": {"checkpoints": [32, 64], "k64_min": 0.90, "k64_max": 1.20},
    "token_order_share": {"min": 0.0, "max": 0.02},
    "edge": {"gain_min": 0.15, "positive_min": 15, "blocks": 16},
    "hapax": {"min": 0.65},
}

# coupling-v2's own committed primary result (PR #71 summary JSON), for the H2-headroom
# comparison this design's claim depends on. Not recomputed here -- coupling-v2 is unchanged.
COUPLING_V2_PRIMARY_H2_CEILING = SIX_CRITERIA["H2_bits"]["center"] + SIX_CRITERIA["H2_bits"]["tol"]  # 2.8397
COUPLING_V2_PRIMARY_H2_HEADROOM_BITS = 0.0083


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_source(repo: Path) -> dict:
    ref = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if commit != ref["source_commit"]:
        raise RuntimeError(f"external repository at {commit}, expected {ref['source_commit']}")
    return {"commit": commit, "reused_from": "boundary-state-null verified source (identical pin)"}


def expand(atomic_token: str) -> str:
    return "".join(EXPAND_MAP.get(a, a) for a in atomic_token)


def verify_roundtrip(headlines_module) -> None:
    for atom in ATOMIC_ALPHABET:
        if headlines_module.collapse(expand(atom)) != atom:
            raise RuntimeError(f"round-trip failed for atom {atom}")


def apply_coupling_v3(atomic_tokens: list[str], beta: float, rng: random.Random) -> list[str]:
    """coupling-v3: identical target rule to coupling-v2 (target = prev_last, 26 distinct
    possible targets), only beta (trigger probability) differs from coupling-v2's fixed 0.5."""
    output: list[str] = []
    prev_last = None
    for i, token in enumerate(atomic_tokens):
        candidate = list(token)
        if i > 0 and rng.random() < beta:
            candidate[0] = prev_last
        candidate_str = "".join(candidate)
        output.append(candidate_str)
        prev_last = candidate_str[-1]
    return output


def apply_boundary_shift_v2(coupled_tokens: list[str], nu_shift: float, rng: random.Random) -> list[str]:
    """Unchanged from external_hybrid_shift_coupling_v2_substitution_novelty_null_audit.py."""
    result: list[str] = []
    emitted: set[str] = set()
    i = 0
    n = len(coupled_tokens)
    while i < n:
        tok_i = coupled_tokens[i]
        eligible = tok_i in emitted and i + 1 < n
        if eligible and rng.random() < nu_shift:
            tok_j = coupled_tokens[i + 1]
            combined = tok_i + tok_j
            L = len(combined)
            original_split = len(tok_i)
            start_pos = rng.randrange(1, L)
            positions = [(start_pos - 1 + k) % (L - 1) + 1 for k in range(L - 1)]
            positions = [p for p in positions if p != original_split]
            found = False
            for p in positions:
                left, right = combined[:p], combined[p:]
                left_new = left not in emitted
                right_new = right not in emitted
                if left_new != right_new:
                    result.append(left); result.append(right)
                    emitted.add(left); emitted.add(right)
                    found = True
                    break
            if not found:
                for p in positions:
                    left, right = combined[:p], combined[p:]
                    if left not in emitted or right not in emitted:
                        result.append(left); result.append(right)
                        emitted.add(left); emitted.add(right)
                        found = True
                        break
            if not found:
                result.append(tok_i)
                result.append(tok_j)
                emitted.add(tok_i)
                emitted.add(tok_j)
            i += 2
        else:
            result.append(tok_i)
            emitted.add(tok_i)
            i += 1
    return result


def apply_substitution_topup(shifted_tokens: list[str], nu_sub: float, rng: random.Random) -> list[str]:
    """Unchanged from external_hybrid_shift_coupling_v2_substitution_novelty_null_audit.py."""
    output: list[str] = []
    emitted: set[str] = set()
    unigram_freq: Counter = Counter()
    bigram_freq: dict[str, Counter] = defaultdict(Counter)
    bigram_total: Counter = Counter()
    tokens_emitted = 0

    for token in shifted_tokens:
        candidate = list(token)
        candidate_str = "".join(candidate)
        if candidate_str in emitted and len(candidate) >= 2 and rng.random() < nu_sub:
            n = len(candidate)
            start_pos = rng.randrange(1, n)
            positions = [(start_pos - 1 + k) % (n - 1) + 1 for k in range(n - 1)]
            use_cold_start = tokens_emitted < COLD_START_TOKENS
            found = False
            for pos in positions:
                original = candidate[pos]
                alternatives = [a for a in ATOMIC_ALPHABET if a != original]
                if use_cold_start:
                    start_step = rng.randrange(1, 26)
                    order = [alternatives[(start_step - 1 + k) % 25] for k in range(25)]
                else:
                    preceding = candidate[pos - 1]
                    if bigram_total.get(preceding, 0) >= SPARSE_CONTEXT_MIN:
                        context = bigram_freq[preceding]
                        keyed = [(-context.get(a, 0), rng.random(), a) for a in alternatives]
                    else:
                        keyed = [(-unigram_freq.get(a, 0), rng.random(), a) for a in alternatives]
                    keyed.sort()
                    order = [a for _, _, a in keyed]
                for alt in order:
                    trial = candidate.copy()
                    trial[pos] = alt
                    trial_str = "".join(trial)
                    if trial_str not in emitted:
                        candidate_str = trial_str
                        found = True
                        break
                if found:
                    break
        output.append(candidate_str)
        emitted.add(candidate_str)
        prev_char = None
        for ch in candidate_str:
            unigram_freq[ch] += 1
            if prev_char is not None:
                bigram_freq[prev_char][ch] += 1
                bigram_total[prev_char] += 1
            prev_char = ch
        tokens_emitted += 1
    return output


def transform_replicate(atomic_tokens: list[str], beta: float, nu_shift: float, nu_sub: float, seed: int) -> list[str]:
    rng = random.Random(seed)
    coupled = apply_coupling_v3(atomic_tokens, beta, rng)
    shifted = apply_boundary_shift_v2(coupled, nu_shift, rng)
    topped_up = apply_substitution_topup(shifted, nu_sub, rng)
    return topped_up


def edge_rows(lines):
    return [(i, left[-1], right[0]) for i, line in enumerate(lines) for left, right in zip(line, line[1:])]


def edge_crossfit(lines, alpha, blocks=16):
    rows = edge_rows(lines)
    total_gain, total_pairs, positive = 0.0, 0, 0
    for fold in range(blocks):
        lower = fold * len(lines) // blocks
        upper = (fold + 1) * len(lines) // blocks
        training = [r for r in rows if not lower <= r[0] < upper]
        testing = [r for r in rows if lower <= r[0] < upper]
        marginal = Counter(right for _, _, right in training)
        context = Counter((left, right) for _, left, right in training)
        left_count = Counter(left for _, left, _ in training)
        alphabet = set(marginal)
        categories = len(alphabet) + 1
        gain = 0.0
        for _, left, observed in testing:
            right = observed if observed in alphabet else "<unknown>"
            conditional = (context[(left, right)] + alpha) / (left_count[left] + alpha * categories)
            baseline = (marginal[right] + alpha) / (len(training) + alpha * categories)
            gain += math.log2(conditional / baseline)
        value = gain / len(testing)
        if value > 0:
            positive += 1
        total_gain += gain
        total_pairs += len(testing)
    return {"gain_bits_per_boundary": total_gain / total_pairs, "positive_blocks": positive, "blocks": blocks}


def evaluate_replicate(tokens, targets, naibbe_module, scale, args, modules):
    if len(tokens) < sum(targets["line_lengths"]):
        raise RuntimeError(f"{len(tokens)} tokens < {sum(targets['line_lengths'])} required by the line template")
    result = naibbe_module.battery("replicate", tokens, None, set(), targets, args, modules, lambda m: None, [])
    entropy = result["entropy"]["collapsed"]
    bpe = result["bpe"]
    order = result["order"]["order_by_cap"]["2000"]
    vocab = result["order"]["vocabulary"]
    template_lines = scale.wrap_to_lengths(tokens, targets["line_lengths"])
    edge = edge_crossfit(template_lines, alpha=1.0, blocks=16)

    c = SIX_CRITERIA
    passes = {
        "H1": abs(entropy["H1"] - c["H1_bits"]["center"]) <= c["H1_bits"]["tol"],
        "H2": abs(entropy["H2"] - c["H2_bits"]["center"]) <= c["H2_bits"]["tol"],
        "learned_units": (
            bpe["minimum_checkpoint"] in c["learned_units"]["checkpoints"]
            and c["learned_units"]["k64_min"] <= bpe["curve"]["64"]["gap"] <= c["learned_units"]["k64_max"]
        ),
        "token_order_share": c["token_order_share"]["min"] <= order["share"] <= c["token_order_share"]["max"],
        "edge": (
            edge["gain_bits_per_boundary"] >= c["edge"]["gain_min"]
            and edge["positive_blocks"] >= c["edge"]["positive_min"]
        ),
        "hapax": vocab["hapax_share_of_types"] >= c["hapax"]["min"],
    }
    return {
        "n_tokens": len(tokens),
        "H1": entropy["H1"], "H2": entropy["H2"],
        "bpe_minimum_checkpoint": bpe["minimum_checkpoint"], "bpe_k64_gap": bpe["curve"]["64"]["gap"],
        "token_order_share": order["share"], "hapax_share_of_types": vocab["hapax_share_of_types"],
        "vocabulary_types": vocab["types"],
        "edge_gain_bits_per_boundary": edge["gain_bits_per_boundary"], "edge_positive_blocks": edge["positive_blocks"],
        "criteria_pass": passes,
        "all_six_pass": all(passes.values()),
    }


def setup(units_repo: Path, log):
    source = verify_source(units_repo)
    log(f"verified source: commit {source['commit']} (reused pin from boundary-state-null)")

    sys.path.insert(0, str(units_repo / "analysis"))
    naibbe_module = importlib.import_module("reproduce_naibbe_control")
    bundle = units_repo / "voynich_decipherment_repro_bundle"
    modules = naibbe_module.load_modules(bundle)
    _attack_lib, _attack_voynich, unit_probe, headlines, scale, _space, plant = modules
    verify_roundtrip(headlines)
    log("atomic round-trip verified for all 26 atoms")

    voy_tokens = naibbe_module.voynich_entropy_tokens(bundle, headlines)
    observed, _, _, _ = scale.load_voynich_lines(bundle, plant.LOCUS_RE, plant.collapse, plant.strip_markup)
    line_lengths = [len(line) for line in observed]
    pooled = unit_probe.voynich_lines()
    targets = {
        "entropy_tokens": len(voy_tokens),
        "line_lengths": line_lengths,
        "bpe_glyphs": sum(len(w) for ln in pooled for w in ln),
    }
    log(f"targets: entropy_tokens={targets['entropy_tokens']} lines={len(line_lengths)} "
        f"template_tokens={sum(line_lengths)}")

    tables = json.loads((bundle.parent / "data" / "controls" / "naibbe" / "naibbe_tables.json").read_text(encoding="utf-8"))
    cipher = naibbe_module.NaibbeCipher(tables, deck="deck_52", ambiguity_rule="v1")
    words = naibbe_module.caesar_words(_attack_lib)
    letters = "".join(words)

    args = SimpleNamespace(skip_attack=True, skip_crossing=True, shuffles=100, extra_k=[])
    return source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args


def pilot(units_repo: Path, log):
    source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args = setup(units_repo, log)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    cfg = manifest["coupling_v3"]
    pilot_cipher_seeds = manifest["seeds"]["cipher"][: cfg["pilot_seeds_per_beta"]]
    pilot_post_seeds = manifest["seeds"]["postprocessor"][: cfg["pilot_seeds_per_beta"]]

    atomic_cache = {}
    for i, cs in enumerate(pilot_cipher_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic_cache[i] = [headlines.collapse(t) for t in encrypted["tokens"]]

    print(f"{'beta':>6} | {'edge_mean':>10} | {'H2_mean':>8} | {'order_mean':>10} | edge_clears_floor")
    results = {}
    for beta in cfg["beta_pilot_grid"]:
        edge_vals, h2_vals, order_vals = [], [], []
        for i in range(cfg["pilot_seeds_per_beta"]):
            transformed = transform_replicate(
                atomic_cache[i], beta=beta, nu_shift=cfg["nu_shift_fixed"], nu_sub=cfg["nu_sub_fixed"],
                seed=pilot_post_seeds[i],
            )
            expanded = [expand(t) for t in transformed]
            ev = evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
            edge_vals.append(ev["edge_gain_bits_per_boundary"])
            h2_vals.append(ev["H2"])
            order_vals.append(ev["token_order_share"])
        mean_edge = sum(edge_vals) / len(edge_vals)
        mean_h2 = sum(h2_vals) / len(h2_vals)
        mean_order = sum(order_vals) / len(order_vals)
        clears = mean_edge >= SIX_CRITERIA["edge"]["gain_min"]
        results[beta] = {"edge_mean": mean_edge, "H2_mean": mean_h2, "order_mean": mean_order, "clears_edge_floor": clears}
        print(f"{beta:6.2f} | {mean_edge:10.4f} | {mean_h2:8.4f} | {mean_order:10.4f} | {clears}")

    qualifying = [b for b, r in results.items() if r["clears_edge_floor"]]
    if qualifying:
        selected = min(qualifying)
        print(f"\nSelected primary beta per manifest rule (lowest qualifying): {selected}")
    else:
        print("\nNo beta in the pilot grid clears the edge floor -- per the manifest's honesty "
              "precommitment, this is a negative result for the lower-fixed-beta approach. Do not "
              "expand the grid without a fresh precommitment.")
    return results


def run(units_repo: Path, log, beta: float) -> dict:
    source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args = setup(units_repo, log)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    reference = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    cfg = manifest["coupling_v3"]

    cipher_seeds = manifest["seeds"]["cipher"]
    post_seeds = manifest["seeds"]["postprocessor"]
    nu_sub = cfg["nu_sub_fixed"]
    nu_shift = cfg["nu_shift_fixed"]

    atomic_cache: dict[int, list[str]] = {}

    def get_atomic(seed_index: int) -> list[str]:
        if seed_index not in atomic_cache:
            encrypted = cipher.encrypt(letters, cipher_seeds[seed_index])
            atomic_cache[seed_index] = [headlines.collapse(t) for t in encrypted["tokens"]]
        return atomic_cache[seed_index]

    # baseline (no coupling at all) is beta-independent -- safe to reuse by reference.
    # edge_only depends on beta and MUST be recomputed fresh at this design's selected beta.
    replicates: dict[str, dict[str, dict]] = {
        "baseline": reference["replicates"]["baseline"],
    }

    def run_config(name: str, beta_: float, nu_shift_: float, nu_sub_: float, n: int):
        bucket = replicates.setdefault(name, {})
        for i in range(n):
            t = time.time()
            atomic = get_atomic(i)
            transformed_atomic = transform_replicate(atomic, beta_, nu_shift_, nu_sub_, post_seeds[i])
            expanded = [expand(tok) for tok in transformed_atomic]
            evaluation = evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
            bucket[str(cipher_seeds[i])] = evaluation
            log(f"{name} seed_index={i}: all_six_pass={evaluation['all_six_pass']} ({time.time()-t:.1f}s)")

    run_config("edge_only", beta, 0.0, 0.0, 20)
    run_config("primary", beta, nu_shift, nu_sub, cfg["primary_seeds"])

    def aggregate(rows):
        metrics = ["H1", "H2", "bpe_minimum_checkpoint", "bpe_k64_gap", "token_order_share",
                   "hapax_share_of_types", "edge_gain_bits_per_boundary", "edge_positive_blocks"]
        out = {"n": len(rows), "joint_pass": sum(1 for r in rows if r["all_six_pass"])}
        for m in metrics:
            values = [r[m] for r in rows]
            out[m] = {"mean": sum(values) / len(values), "min": min(values), "max": max(values)}
        for c in ("H1", "H2", "learned_units", "token_order_share", "edge", "hapax"):
            out[f"criterion_{c}_passes"] = sum(1 for r in rows if r["criteria_pass"][c])
        return out

    aggregates = {name: aggregate(list(bucket.values())) for name, bucket in replicates.items()}

    baseline_rows = replicates["baseline"]
    edge_only_rows = replicates["edge_only"]
    n_paired = len(baseline_rows)

    edge_increase = sum(
        1 for i in range(n_paired)
        if edge_only_rows[str(cipher_seeds[i])]["edge_gain_bits_per_boundary"]
        > baseline_rows[str(cipher_seeds[i])]["edge_gain_bits_per_boundary"]
    )
    edge_criterion_pass = sum(1 for r in edge_only_rows.values() if r["criteria_pass"]["edge"])
    boundary_check_pass = edge_increase >= 16 and edge_criterion_pass >= 16

    manipulation_checks = {
        "boundary": {"paired_edge_increase": edge_increase, "edge_criterion_pass": edge_criterion_pass,
                     "pass": boundary_check_pass, "computed_fresh_at_selected_beta": beta},
    }
    log(f"manipulation checks: boundary={manipulation_checks['boundary']}")

    primary_h2_values = [r["H2"] for r in replicates["primary"].values()]
    primary_h2_max = max(primary_h2_values)
    v3_headroom = COUPLING_V2_PRIMARY_H2_CEILING - primary_h2_max
    headroom_improved = v3_headroom > COUPLING_V2_PRIMARY_H2_HEADROOM_BITS

    primary_joint_pass = aggregates["primary"]["joint_pass"]
    if not boundary_check_pass:
        verdict = "INVALID_CONSTRUCTION"
    elif primary_joint_pass >= 16 and headroom_improved:
        verdict = "PASS"
    elif primary_joint_pass >= 16:
        verdict = "PASS_BUT_HEADROOM_NOT_IMPROVED"
    else:
        verdict = "FAIL"

    return {
        "source": source,
        "protocol": "solo design, self-reviewed (logs/2026-09-23-claude-coupling-v3-lower-beta-selfreview.md)",
        "manifest": "data/external/coupling-v3-lower-beta-hybrid-manifest-v1.json",
        "selected_beta": beta,
        "nu_sub": nu_sub,
        "cipher_seeds": cipher_seeds,
        "postprocessor_seeds": post_seeds,
        "six_criteria": SIX_CRITERIA,
        "replicates": replicates,
        "aggregate": aggregates,
        "manipulation_checks": manipulation_checks,
        "primary_joint_pass": primary_joint_pass,
        "h2_headroom_bits": v3_headroom,
        "coupling_v2_primary_h2_headroom_bits": COUPLING_V2_PRIMARY_H2_HEADROOM_BITS,
        "headroom_improved_vs_coupling_v2": headroom_improved,
        "primary_verdict": verdict,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("units_repo", type=Path)
    parser.add_argument("--output", type=Path, default=OUT_JSON)
    parser.add_argument("--pilot", action="store_true", help="run the beta calibration grid, no selection frozen")
    parser.add_argument("--beta", type=float, default=None, help="frozen beta value from pilot, required unless --pilot")
    args = parser.parse_args()

    started = time.time()

    def log(message: str) -> None:
        print(f"[{time.time()-started:7.1f}s] {message}", flush=True)

    if args.pilot:
        pilot(args.units_repo.resolve(), log)
        return

    if args.beta is None:
        print("error: --beta is required for a full run (use --pilot first to calibrate)", file=sys.stderr)
        sys.exit(2)

    summary = run(args.units_repo.resolve(), log, args.beta)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {args.output}; primary verdict: {summary['primary_verdict']}")


if __name__ == "__main__":
    main()
