#!/usr/bin/env python3
"""Execute the preregistered boundary-state constructive null (ChatGPT's design).

Implements methods/boundary-state-null-preregistration.md and
data/external/boundary-state-null-manifest-v1.json exactly as frozen. Applies
a two-operation postprocessor (boundary coupling, then novelty injection) to
Naibbe/Caesar ciphertext at fixed paired seeds, expands the atomic
representation back to raw EVA, and scores through the project's unchanged
entropy/BPE/token-order/edge pipeline.

Usage:
    python data/scripts/external_boundary_state_null_audit.py \
        ../paper-audit/voynich-units
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
OUT_JSON = ROOT / "data" / "derived" / "external-boundary-state-null-audit-summary.json"
MANIFEST_PATH = ROOT / "data" / "external" / "boundary-state-null-manifest-v1.json"

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


def verify_source(repo: Path, manifest: dict) -> dict:
    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    expected_commit = manifest["external_source"]["commit"]
    if commit != expected_commit:
        raise RuntimeError(f"external repository at {commit}, expected {expected_commit}")
    statuses = {}
    for entry in manifest["external_source"]["files"]:
        path = entry["path"]
        expected = entry["sha256"]
        actual = sha256(repo / path)
        statuses[path] = {"expected": expected, "actual": actual, "matches": actual == expected}
        if actual != expected:
            raise RuntimeError(f"checksum mismatch for {path}: {actual}, expected {expected}")
    return {"commit": commit, "files": statuses}


def expand(atomic_token: str) -> str:
    return "".join(EXPAND_MAP.get(a, a) for a in atomic_token)


def verify_roundtrip(headlines_module) -> None:
    for atom in ATOMIC_ALPHABET:
        if headlines_module.collapse(expand(atom)) != atom:
            raise RuntimeError(f"round-trip failed for atom {atom}")


def transform_replicate(atomic_tokens: list[str], beta: float, nu: float, seed: int) -> list[str]:
    rng = random.Random(seed)
    output: list[str] = []
    emitted: set[str] = set()
    prev_last = None
    for i, token in enumerate(atomic_tokens):
        candidate = list(token)
        if i > 0 and rng.random() < beta:
            target = TARGET_INITIALS[ATOMIC_ALPHABET.index(prev_last) % 4]
            candidate[0] = target
        candidate_str = "".join(candidate)
        if candidate_str in emitted and len(candidate) >= 2 and rng.random() < nu:
            n = len(candidate)
            start_pos = rng.randrange(1, n)
            start_step = rng.randrange(1, 26)
            positions = [(start_pos - 1 + k) % (n - 1) + 1 for k in range(n - 1)]
            found = False
            for pos in positions:
                original = candidate[pos]
                alternatives = [a for a in ATOMIC_ALPHABET if a != original]
                order = [alternatives[(start_step - 1 + k) % 25] for k in range(25)]
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
        prev_last = candidate_str[-1]
    return output


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


def run(units_repo: Path, log) -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    source = verify_source(units_repo, manifest)
    log(f"verified source: commit {source['commit']}, 3 files OK")

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

    cipher_seeds = manifest["seeds"]["cipher"]
    post_seeds = manifest["seeds"]["postprocessor"]
    args = SimpleNamespace(skip_attack=True, skip_crossing=True, shuffles=100, extra_k=[])

    # cache atomic Naibbe tokens per cipher seed (shared across configs)
    atomic_cache: dict[int, list[str]] = {}

    def get_atomic(seed_index: int) -> list[str]:
        if seed_index not in atomic_cache:
            encrypted = cipher.encrypt(letters, cipher_seeds[seed_index])
            raw = encrypted["tokens"]
            atomic_cache[seed_index] = [headlines.collapse(t) for t in raw]
        return atomic_cache[seed_index]

    replicates: dict[str, dict[str, dict]] = {}

    def run_config(name: str, beta: float, nu: float, n: int):
        bucket = replicates.setdefault(name, {})
        for i in range(n):
            t = time.time()
            atomic = get_atomic(i)
            transformed_atomic = transform_replicate(atomic, beta, nu, post_seeds[i])
            expanded = [expand(tok) for tok in transformed_atomic]
            evaluation = evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
            bucket[str(cipher_seeds[i])] = evaluation
            log(f"{name} seed_index={i}: all_six_pass={evaluation['all_six_pass']} ({time.time()-t:.1f}s)")

    configs = manifest["configurations"]
    run_config("primary", configs["primary"]["beta"], configs["primary"]["nu"], configs["primary"]["replicates"])
    for cname, cfg in configs["controls"].items():
        run_config(cname, cfg["beta"], cfg["nu"], cfg["replicates"])
    for sname, cfg in configs["sensitivities"].items():
        if sname == "sensitivities_cannot_rescue_primary_failure":
            continue
        run_config(sname, cfg["beta"], cfg["nu"], cfg["replicates"])

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

    # manipulation checks (paired by seed index against baseline)
    baseline_rows = replicates["baseline"]
    edge_only_rows = replicates["edge_only"]
    novelty_only_rows = replicates["novelty_only"]
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
        if novelty_only_rows[str(cipher_seeds[i])]["hapax_share_of_types"]
        > baseline_rows[str(cipher_seeds[i])]["hapax_share_of_types"]
    )
    novelty_criterion_pass = sum(1 for r in novelty_only_rows.values() if r["criteria_pass"]["hapax"])
    novelty_check_pass = novelty_increase >= 16 and novelty_criterion_pass >= 16

    manipulation_checks = {
        "boundary": {"paired_edge_increase": edge_increase, "edge_criterion_pass": edge_criterion_pass,
                     "pass": boundary_check_pass},
        "novelty": {"paired_hapax_increase": novelty_increase, "hapax_criterion_pass": novelty_criterion_pass,
                    "pass": novelty_check_pass},
    }
    log(f"manipulation checks: boundary={manipulation_checks['boundary']}, novelty={manipulation_checks['novelty']}")

    primary_joint_pass = aggregates["primary"]["joint_pass"]
    if not (boundary_check_pass and novelty_check_pass):
        verdict = "INVALID_CONSTRUCTION"
    elif primary_joint_pass >= 16:
        verdict = "PASS"
    else:
        verdict = "FAIL"

    return {
        "source": source,
        "protocol": "methods/boundary-state-null-preregistration.md",
        "manifest": "data/external/boundary-state-null-manifest-v1.json",
        "cipher_seeds": cipher_seeds,
        "postprocessor_seeds": post_seeds,
        "six_criteria": SIX_CRITERIA,
        "replicates": replicates,
        "aggregate": aggregates,
        "manipulation_checks": manipulation_checks,
        "primary_joint_pass": primary_joint_pass,
        "primary_verdict": verdict,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("units_repo", type=Path)
    parser.add_argument("--output", type=Path, default=OUT_JSON)
    args = parser.parse_args()

    started = time.time()

    def log(message: str) -> None:
        print(f"[{time.time()-started:7.1f}s] {message}", flush=True)

    summary = run(args.units_repo.resolve(), log)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {args.output}; primary verdict: {summary['primary_verdict']}")


if __name__ == "__main__":
    main()
