#!/usr/bin/env python3
"""Execute the already-frozen coupling-v2 section-aware preregistration.

Implements methods/coupling-v2-section-aware-preregistration.md exactly as
frozen (2026-09-25, commit 9608ea4). Execution notes and the one interpretive
threshold fixed before any output existed:
logs/2026-09-25-claude-coupling-v2-section-aware-execution.md.

Base mechanism (Naibbe + boundary_coupling_v2 beta=0.5 target=prev_last +
boundary_shift_v2 nu_shift=1.0 + substitution top-up, six-criterion
evaluation) is reused byte-for-byte from
external_hybrid_shift_coupling_v2_substitution_novelty_null_audit.py.
The only change: substitution top-up's nu_sub becomes section-dependent
(nu_sub_A, nu_sub_B, nu_sub_default=0.01 for the 89 unlabeled lines).

Boundary/novelty manipulation checks are reused BY REFERENCE from
coupling-v2's own already-merged result (unchanged, per the design) --
this script adds only the new section-manipulation check (anchor pair).

Usage:
    python data/scripts/external_coupling_v2_section_aware_preregistered.py <units_repo> --pilot
    python data/scripts/external_coupling_v2_section_aware_preregistered.py <units_repo> --primary --nu-sub-a A --nu-sub-b B
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
OUT_PILOT_JSON = ROOT / "data" / "derived" / "external-coupling-v2-section-aware-pilot-summary.json"
OUT_PRIMARY_JSON = ROOT / "data" / "derived" / "external-coupling-v2-section-aware-primary-summary.json"
REFERENCE_PATH = ROOT / "data" / "external" / "reference" / "boundary-state-null-baseline-edgeonly-reference.json"
COUPLING_V2_RESULT_PATH = ROOT / "data" / "derived" / "external-hybrid-shift-coupling-v2-substitution-novelty-null-audit-summary.json"
COUPLING_V2_MANIFEST_PATH = ROOT / "data" / "external" / "hybrid-shift-coupling-v2-substitution-novelty-null-manifest-v1.json"

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

BETA_FIXED = 0.5
NU_SHIFT_FIXED = 1.0
NU_SUB_DEFAULT = 0.01
REAL_GAP_TARGET_BAND = (0.139, 0.417)  # 50%-150% of the real +0.2780-bit gap
ANCHOR_CHECK_THRESHOLD = 0.05  # fixed in the execution log before any output existed

PILOT_GRID = [
    (0.01, 0.01),   # anchor: identical to coupling-v2's own global value
    (0.02, 0.005),
    (0.03, 0.003),
    (0.05, 0.001),
    (0.08, 0.0),
    (0.12, 0.0),
]


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


def char_bigram_conditional_entropy(words: list[str]) -> float:
    pair_counts: Counter = Counter()
    prefix_counts: Counter = Counter()
    for w in words:
        for i in range(1, len(w)):
            prefix, nxt = w[i - 1], w[i]
            pair_counts[(prefix, nxt)] += 1
            prefix_counts[prefix] += 1
    total = sum(pair_counts.values())
    if total == 0:
        return 0.0
    h = 0.0
    for (prefix, nxt), c in pair_counts.items():
        p_joint = c / total
        p_cond = c / prefix_counts[prefix]
        h -= p_joint * math.log2(p_cond)
    return h


def apply_coupling_v2(atomic_tokens: list[str], beta: float, rng: random.Random) -> list[str]:
    """Unchanged from coupling-v2's own already-merged implementation."""
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
    """Unchanged from coupling-v2's own already-merged implementation."""
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


def apply_section_varying_substitution_topup(shifted_tokens, token_labels, nu_by_label, rng):
    """Same mechanics as coupling-v2's own apply_substitution_topup, except
    nu_sub is looked up per-token from that token's real Currier-label section."""
    output: list[str] = []
    emitted: set[str] = set()
    unigram_freq: Counter = Counter()
    bigram_freq: dict[str, Counter] = defaultdict(Counter)
    bigram_total: Counter = Counter()
    tokens_emitted = 0

    for idx, token in enumerate(shifted_tokens):
        candidate = list(token)
        candidate_str = "".join(candidate)
        label = token_labels[idx] if idx < len(token_labels) else "?"
        nu_sub = nu_by_label[label]
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


def transform_replicate(atomic_tokens, token_labels, nu_sub_a, nu_sub_b, seed):
    rng = random.Random(seed)
    coupled = apply_coupling_v2(atomic_tokens, BETA_FIXED, rng)
    shifted = apply_boundary_shift_v2(coupled, NU_SHIFT_FIXED, rng)
    nu_by_label = {"A": nu_sub_a, "B": nu_sub_b, "?": NU_SUB_DEFAULT}
    topped_up = apply_section_varying_substitution_topup(shifted, token_labels, nu_by_label, rng)
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


def section_gap(expanded_tokens, line_lengths, currier_labels_by_line, scale):
    gen_lines = scale.wrap_to_lengths(expanded_tokens, line_lengths)
    gen_a_words = [tok for line, label in zip(gen_lines, currier_labels_by_line) if label == "A" for tok in line]
    gen_b_words = [tok for line, label in zip(gen_lines, currier_labels_by_line) if label == "B" for tok in line]
    return char_bigram_conditional_entropy(gen_a_words) - char_bigram_conditional_entropy(gen_b_words)


def setup(units_repo: Path, log):
    source = verify_source(units_repo)
    log(f"verified source: commit {source['commit']} (reused pin from boundary-state-null)")

    sys.path.insert(0, str(units_repo / "analysis"))
    naibbe_module = importlib.import_module("reproduce_naibbe_control")
    from reproduce_space_sensitivity import parse_lines
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

    parsed, _ = parse_lines(bundle / "voynich_calibration_sources" / "ZL3b.txt", plant.LOCUS_RE, plant.strip_markup)
    currier_labels_by_line = [line["currier"] for line in parsed]
    assert len(line_lengths) == len(currier_labels_by_line)
    token_labels = [label for length, label in zip(line_lengths, currier_labels_by_line) for _ in range(length)]

    real_a_words = [tok for line, label in zip(observed, currier_labels_by_line) if label == "A" for tok in line]
    real_b_words = [tok for line, label in zip(observed, currier_labels_by_line) if label == "B" for tok in line]
    real_gap = char_bigram_conditional_entropy(real_a_words) - char_bigram_conditional_entropy(real_b_words)
    log(f"real Voynich Currier A/B gap (sanity check): {real_gap:.4f} bits")

    tables = json.loads((bundle.parent / "data" / "controls" / "naibbe" / "naibbe_tables.json").read_text(encoding="utf-8"))
    cipher = naibbe_module.NaibbeCipher(tables, deck="deck_52", ambiguity_rule="v1")
    words = naibbe_module.caesar_words(_attack_lib)
    letters = "".join(words)

    args = SimpleNamespace(skip_attack=True, skip_crossing=True, shuffles=100, extra_k=[])
    return (source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args,
            token_labels, line_lengths, currier_labels_by_line, real_gap)


def run_pilot(units_repo: Path, log) -> dict:
    (source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args,
     token_labels, line_lengths, currier_labels_by_line, real_gap) = setup(units_repo, log)

    manifest = json.loads(COUPLING_V2_MANIFEST_PATH.read_text(encoding="utf-8"))
    pilot_cipher_seeds = manifest["seeds"]["cipher"][:3]
    pilot_post_seeds = manifest["seeds"]["postprocessor"][:3]
    log(f"pilot seeds: cipher={pilot_cipher_seeds} postprocessor={pilot_post_seeds}")

    atomic_cache = {}
    for i, cs in enumerate(pilot_cipher_seeds):
        encrypted = cipher.encrypt(letters, cs)
        atomic_cache[i] = [headlines.collapse(t) for t in encrypted["tokens"]]

    pilot_results = []
    for nu_sub_a, nu_sub_b in PILOT_GRID:
        seed_rows = []
        for i in range(3):
            transformed = transform_replicate(atomic_cache[i], token_labels, nu_sub_a, nu_sub_b, pilot_post_seeds[i])
            expanded = [expand(t) for t in transformed]
            ev = evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
            gap = section_gap(expanded, line_lengths, currier_labels_by_line, scale)
            seed_rows.append({"cipher_seed": pilot_cipher_seeds[i], "all_six_pass": ev["all_six_pass"],
                               "H2": ev["H2"], "gap": gap})
            log(f"pilot ({nu_sub_a},{nu_sub_b}) seed {pilot_cipher_seeds[i]}: "
                f"all_six_pass={ev['all_six_pass']} H2={ev['H2']:.4f} gap={gap:.4f}")
        all_three_pass = all(r["all_six_pass"] for r in seed_rows)
        mean_gap = sum(r["gap"] for r in seed_rows) / len(seed_rows)
        pilot_results.append({
            "nu_sub_a": nu_sub_a, "nu_sub_b": nu_sub_b,
            "seed_rows": seed_rows,
            "all_three_seeds_pass_six_criteria": all_three_pass,
            "mean_gap": mean_gap,
            "mean_gap_as_fraction_of_real": mean_gap / real_gap,
        })

    anchor = pilot_results[0]
    assert (anchor["nu_sub_a"], anchor["nu_sub_b"]) == (0.01, 0.01)
    anchor_check_pass = abs(anchor["mean_gap"]) < ANCHOR_CHECK_THRESHOLD

    qualifying = [
        r for r in pilot_results
        if r["all_three_seeds_pass_six_criteria"] and r["mean_gap"] >= REAL_GAP_TARGET_BAND[0]
    ]
    selected = None
    if qualifying:
        selected = min(qualifying, key=lambda r: r["mean_gap"] - REAL_GAP_TARGET_BAND[0])

    summary = {
        "design": "methods/coupling-v2-section-aware-preregistration.md",
        "real_gap": real_gap,
        "anchor_check": {"mean_gap": anchor["mean_gap"], "threshold": ANCHOR_CHECK_THRESHOLD, "pass": anchor_check_pass},
        "pilot_grid_results": pilot_results,
        "selected_pair": {"nu_sub_a": selected["nu_sub_a"], "nu_sub_b": selected["nu_sub_b"]} if selected else None,
        "pilot_verdict": "QUALIFYING_PAIR_SELECTED" if selected else "NO_QUALIFYING_PILOT_PAIR",
    }
    OUT_PILOT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_PILOT_JSON}")
    log(f"anchor check pass={anchor_check_pass} (mean gap {anchor['mean_gap']:.4f}, threshold {ANCHOR_CHECK_THRESHOLD})")
    log(f"pilot verdict: {summary['pilot_verdict']}" + (f" -> {summary['selected_pair']}" if selected else ""))
    return summary


def run_primary(units_repo: Path, log, nu_sub_a: float, nu_sub_b: float) -> dict:
    (source, naibbe_module, headlines, scale, modules, targets, cipher, letters, args,
     token_labels, line_lengths, currier_labels_by_line, real_gap) = setup(units_repo, log)

    coupling_v2_result = json.loads(COUPLING_V2_RESULT_PATH.read_text(encoding="utf-8"))
    manipulation_checks_reused = coupling_v2_result["manipulation_checks"]
    log(f"manipulation checks reused by reference from coupling-v2's own result: {manipulation_checks_reused}")

    manifest = json.loads(COUPLING_V2_MANIFEST_PATH.read_text(encoding="utf-8"))
    cipher_seeds = manifest["seeds"]["cipher"]
    post_seeds = manifest["seeds"]["postprocessor"]

    atomic_cache: dict[int, list[str]] = {}

    def get_atomic(idx: int) -> list[str]:
        if idx not in atomic_cache:
            encrypted = cipher.encrypt(letters, cipher_seeds[idx])
            atomic_cache[idx] = [headlines.collapse(t) for t in encrypted["tokens"]]
        return atomic_cache[idx]

    replicates = []
    for i in range(20):
        t0 = time.time()
        atomic = get_atomic(i)
        transformed = transform_replicate(atomic, token_labels, nu_sub_a, nu_sub_b, post_seeds[i])
        expanded = [expand(tok) for tok in transformed]
        ev = evaluate_replicate(expanded, targets, naibbe_module, scale, args, modules)
        gap = section_gap(expanded, line_lengths, currier_labels_by_line, scale)
        in_band = REAL_GAP_TARGET_BAND[0] <= gap <= REAL_GAP_TARGET_BAND[1]
        joint_pass = ev["all_six_pass"] and in_band
        replicates.append({
            "cipher_seed": cipher_seeds[i], "all_six_pass": ev["all_six_pass"],
            "H1": ev["H1"], "H2": ev["H2"], "gap": gap, "gap_in_band": in_band, "joint_pass": joint_pass,
        })
        log(f"primary seed_index={i} seed={cipher_seeds[i]}: all_six_pass={ev['all_six_pass']} "
            f"gap={gap:.4f} in_band={in_band} joint_pass={joint_pass} ({time.time()-t0:.1f}s)")

    joint_pass_count = sum(1 for r in replicates if r["joint_pass"])
    anchor_pilot = json.loads(OUT_PILOT_JSON.read_text(encoding="utf-8"))["anchor_check"] if OUT_PILOT_JSON.exists() else None
    section_check_pass = anchor_pilot["pass"] if anchor_pilot else None

    boundary_pass = manipulation_checks_reused["boundary"]["pass"]
    novelty_pass = manipulation_checks_reused["novelty"]["pass"]

    if not (boundary_pass and novelty_pass and section_check_pass):
        verdict = "INVALID_CONSTRUCTION"
    elif joint_pass_count >= 16:
        verdict = "PASS"
    else:
        verdict = "FAIL"

    summary = {
        "design": "methods/coupling-v2-section-aware-preregistration.md",
        "selected_pair": {"nu_sub_a": nu_sub_a, "nu_sub_b": nu_sub_b},
        "real_gap": real_gap,
        "target_band": REAL_GAP_TARGET_BAND,
        "manipulation_checks_reused_by_reference": manipulation_checks_reused,
        "section_manipulation_check_from_pilot": anchor_pilot,
        "replicates": replicates,
        "joint_pass_count": joint_pass_count,
        "primary_verdict": verdict,
    }
    OUT_PRIMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_PRIMARY_JSON}")
    log(f"joint_pass_count={joint_pass_count}/20; primary verdict: {verdict}")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("units_repo", type=Path)
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--primary", action="store_true")
    parser.add_argument("--nu-sub-a", type=float, default=None)
    parser.add_argument("--nu-sub-b", type=float, default=None)
    args = parser.parse_args()

    started = time.time()

    def log(message: str) -> None:
        print(f"[{time.time()-started:7.1f}s] {message}", flush=True)

    if args.pilot:
        run_pilot(args.units_repo.resolve(), log)
        return

    if args.primary:
        if args.nu_sub_a is None or args.nu_sub_b is None:
            print("error: --nu-sub-a and --nu-sub-b required for --primary", file=sys.stderr)
            sys.exit(2)
        run_primary(args.units_repo.resolve(), log, args.nu_sub_a, args.nu_sub_b)
        return

    print("error: specify --pilot or --primary", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
