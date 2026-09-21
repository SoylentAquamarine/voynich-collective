#!/usr/bin/env python3
"""Execute the preregistered boundary-shift novelty constructive null (Claude's design).

Implements data/external/boundary-shift-novelty-null-manifest-v1.json exactly
as frozen. Structurally different from the five-design substitution sequence:
boundary coupling runs first (identical to all prior designs), then a
SEPARATE pass shifts the boundary between adjacent token pairs instead of
substituting any character -- no character is ever added, removed, or
changed, only regrouped across a moved internal boundary.

Usage:
    python data/scripts/external_boundary_shift_novelty_null_audit.py <units_repo> [--pilot]
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
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-boundary-shift-novelty-null-audit-summary.json"
MANIFEST_PATH = ROOT / "data" / "external" / "boundary-shift-novelty-null-manifest-v1.json"
REFERENCE_PATH = ROOT / "data" / "external" / "reference" / "boundary-state-null-baseline-edgeonly-reference.json"

ATOMIC_ALPHABET = "CEIKNPSTadefgiklmnopqrstxy"
EXPAND_MAP = {"C": "ch", "E": "ee", "I": "in", "K": "ckh", "N": "iin", "P": "cph", "S": "sh", "T": "cth"}
TARGET_INITIALS = ["o", "q", "C", "S"]

SIX_CRITERIA = {
    "H1_bits": {"center": 3.9763, "tol": 0.15},
    "H2_bits": {"center": 2.6897, "tol": 0.15},
    "learned_units": {"checkpoints": [32, 64], "k64_min": 0.90, "k64_max": 1.20},
    "token_order_share": {"min": 0.0, "max": 0.02},
    "edge": {"gain_min": 0.15, "positive_min": 15, "blocks": 16},
    "hapax": {"min": 0.65},
}


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


def apply_coupling(atomic_tokens: list[str], beta: float, rng: random.Random) -> list[str]:
    output: list[str] = []
    prev_last = None
    for i, token in enumerate(atomic_tokens):
        candidate = list(token)
        if i > 0 and rng.random() < beta:
            target = TARGET_INITIALS[ATOMIC_ALPHABET.index(prev_last) % 4]
            candidate[0] = target
        candidate_str = "".join(candidate)
        output.append(candidate_str)
        prev_last = candidate_str[-1]
    return output


def apply_boundary_shift(coupled_tokens: list[str], nu: float, rng: random.Random) -> tuple[list[str], int]:
    result: list[str] = []
    emitted: set[str] = set()
    shift_events = 0
    i = 0
    n = len(coupled_tokens)
    while i < n:
        tok_i = coupled_tokens[i]
        eligible = tok_i in emitted and i + 1 < n
        if eligible and rng.random() < nu:
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
                if left not in emitted and right not in emitted:
                    result.append(left)
                    result.append(right)
                    emitted.add(left)
                    emitted.add(right)
                    found = True
                    shift_events += 1
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
    return result, shift_events


def transform_replicate(atomic_tokens: list[str], beta: float, nu: float, seed: int) -> tuple[list[str], int]:
    rng = random.Random(seed)
    coupled = apply_coupling(atomic_tokens, beta, rng)
    shifted, shift_events = apply_boundary_shift(coupled, nu, rng)
    return shifted, shift_events


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


def pilot(units_repo: Path, log, nu_values):
    source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args = setup(units_repo, log)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    pilot_cipher_seeds = manifest["seeds"]["cipher"][:3]
    pilot_post_seeds = manifest["seeds"]["postprocessor"][:3]

    atomic_cache = {}
    for i, cs in enumerate(pilot_cipher_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic_cache[i] = [headlines.collapse(t) for t in encrypted["tokens"]]

    # H1-invariance sanity check first (should be exact, per the self-review's provable claim)
    baseline_h1 = []
    shift_h1 = []
    for i in range(3):
        base_transformed, _ = transform_replicate(atomic_cache[i], beta=0.0, nu=0.0, seed=pilot_post_seeds[i])
        base_ev = evaluate_replicate([expand(t) for t in base_transformed], targets, naibbe_module, scale, args, modules)
        shift_transformed, _ = transform_replicate(atomic_cache[i], beta=0.0, nu=0.5, seed=pilot_post_seeds[i])
        shift_ev = evaluate_replicate([expand(t) for t in shift_transformed], targets, naibbe_module, scale, args, modules)
        baseline_h1.append(base_ev["H1"])
        shift_h1.append(shift_ev["H1"])
    log(f"H1-invariance check (nu=0 vs nu=0.5): baseline={baseline_h1} shift={shift_h1} "
        f"exact_match={[abs(a-b) < 1e-9 for a, b in zip(baseline_h1, shift_h1)]}")

    for nu in nu_values:
        hapax_vals, h2_vals, events_vals = [], [], []
        for i in range(3):
            transformed, events = transform_replicate(atomic_cache[i], beta=0.0, nu=nu, seed=pilot_post_seeds[i])
            expanded = [expand(t) for t in transformed]
            ev = evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
            hapax_vals.append(ev["hapax_share_of_types"])
            h2_vals.append(ev["H2"])
            events_vals.append(events)
        mean_h = sum(hapax_vals) / len(hapax_vals)
        mean_h2 = sum(h2_vals) / len(h2_vals)
        log(f"pilot nu={nu}: hapax={hapax_vals} mean={mean_h:.4f} | H2 mean={mean_h2:.4f} | shift_events={events_vals}")


def run(units_repo: Path, log, nu: float) -> dict:
    source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args = setup(units_repo, log)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    reference = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))

    cipher_seeds = manifest["seeds"]["cipher"]
    post_seeds = manifest["seeds"]["postprocessor"]

    atomic_cache: dict[int, list[str]] = {}

    def get_atomic(seed_index: int) -> list[str]:
        if seed_index not in atomic_cache:
            encrypted = cipher.encrypt(letters, cipher_seeds[seed_index])
            atomic_cache[seed_index] = [headlines.collapse(t) for t in encrypted["tokens"]]
        return atomic_cache[seed_index]

    replicates: dict[str, dict[str, dict]] = {
        "baseline": reference["replicates"]["baseline"],
        "edge_only": reference["replicates"]["edge_only"],
    }

    def run_config(name: str, beta: float, nu_: float, n: int):
        bucket = replicates.setdefault(name, {})
        for i in range(n):
            t = time.time()
            atomic = get_atomic(i)
            transformed_atomic, events = transform_replicate(atomic, beta, nu_, post_seeds[i])
            expanded = [expand(tok) for tok in transformed_atomic]
            evaluation = evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
            bucket[str(cipher_seeds[i])] = evaluation
            log(f"{name} seed_index={i}: all_six_pass={evaluation['all_six_pass']} events={events} ({time.time()-t:.1f}s)")

    run_config("primary", 0.5, nu, 20)
    run_config("boundary_shift_only", 0.0, nu, 20)
    run_config("weaker_novelty", 0.5, round(nu * 0.5, 4), 5)
    run_config("stronger_novelty", 0.5, min(round(nu * 1.5, 4), 1.0), 5)

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
    shift_novelty_rows = replicates["boundary_shift_only"]
    n_paired = len(baseline_rows)

    edge_increase = sum(
        1 for i in range(n_paired)
        if edge_only_rows[str(cipher_seeds[i])]["edge_gain_bits_per_boundary"]
        > baseline_rows[str(cipher_seeds[i])]["edge_gain_bits_per_boundary"]
    )
    edge_criterion_pass = sum(1 for r in edge_only_rows.values() if r["criteria_pass"]["edge"])
    boundary_check_pass = edge_increase >= 16 and edge_criterion_pass >= 16

    novelty_increase = sum(
        1 for i in range(n_paired)
        if shift_novelty_rows[str(cipher_seeds[i])]["hapax_share_of_types"]
        > baseline_rows[str(cipher_seeds[i])]["hapax_share_of_types"]
    )
    novelty_criterion_pass = sum(1 for r in shift_novelty_rows.values() if r["criteria_pass"]["hapax"])
    novelty_check_pass = novelty_increase >= 16 and novelty_criterion_pass >= 16

    manipulation_checks = {
        "boundary": {"paired_edge_increase": edge_increase, "edge_criterion_pass": edge_criterion_pass,
                     "pass": boundary_check_pass, "reused_from": "boundary-state-null reference"},
        "novelty": {"paired_hapax_increase": novelty_increase, "hapax_criterion_pass": novelty_criterion_pass,
                    "pass": novelty_check_pass},
    }
    log(f"manipulation checks: boundary={manipulation_checks['boundary']}, novelty={manipulation_checks['novelty']}")

    h1_diff = abs(aggregates["boundary_shift_only"]["H1"]["mean"] - aggregates["baseline"]["H1"]["mean"])
    log(f"H1 invariance diagnostic: |boundary_shift_only.H1 - baseline.H1| = {h1_diff:.6f} (should be ~0)")

    primary_joint_pass = aggregates["primary"]["joint_pass"]
    if not (boundary_check_pass and novelty_check_pass):
        verdict = "INVALID_CONSTRUCTION"
    elif primary_joint_pass >= 16:
        verdict = "PASS"
    else:
        verdict = "FAIL"

    return {
        "source": source,
        "protocol": "solo design, self-reviewed (logs/2026-09-21-claude-boundary-shift-novelty-selfreview.md)",
        "manifest": "data/external/boundary-shift-novelty-null-manifest-v1.json",
        "nu_calibrated": nu,
        "cipher_seeds": cipher_seeds,
        "postprocessor_seeds": post_seeds,
        "six_criteria": SIX_CRITERIA,
        "replicates": replicates,
        "aggregate": aggregates,
        "manipulation_checks": manipulation_checks,
        "h1_invariance_diff": h1_diff,
        "primary_joint_pass": primary_joint_pass,
        "primary_verdict": verdict,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("units_repo", type=Path)
    parser.add_argument("--output", type=Path, default=OUT_JSON)
    parser.add_argument("--pilot", action="store_true", help="run self-consistency-only nu calibration, no full sweep")
    parser.add_argument("--nu", type=float, default=None, help="frozen nu value from pilot, required unless --pilot")
    args = parser.parse_args()

    started = time.time()

    def log(message: str) -> None:
        print(f"[{time.time()-started:7.1f}s] {message}", flush=True)

    if args.pilot:
        pilot(args.units_repo.resolve(), log, nu_values=[0.1, 0.15, 0.2, 0.25, 0.3])
        return

    if args.nu is None:
        print("error: --nu is required for a full run (use --pilot first to calibrate)", file=sys.stderr)
        sys.exit(2)

    summary = run(args.units_repo.resolve(), log, args.nu)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {args.output}; primary verdict: {summary['primary_verdict']}")


if __name__ == "__main__":
    main()
