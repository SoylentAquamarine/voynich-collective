#!/usr/bin/env python3
"""Audit the boundary-state-null preregistration without generating outcomes."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "external" / "boundary-state-null-manifest-v1.json"
CARDAN = ROOT / "data" / "external" / "cardan-grille-source-manifest-v1.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("external_repo", type=Path)
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cardan = json.loads(CARDAN.read_text(encoding="utf-8"))
    repo = args.external_repo.resolve()

    commit = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()
    expected_commit = manifest["external_source"]["commit"]
    if commit != expected_commit:
        raise RuntimeError(f"external commit {commit}, expected {expected_commit}")

    hashes = {}
    for row in manifest["external_source"]["files"]:
        actual = sha256(repo / row["path"])
        hashes[row["path"]] = actual
        if actual != row["sha256"]:
            raise RuntimeError(f"checksum mismatch for {row['path']}: {actual}")

    if manifest["six_criteria"] != cardan["six_criteria"]:
        raise RuntimeError("six criteria differ from the frozen Cardan manifest")

    cipher = manifest["seeds"]["cipher"]
    post = manifest["seeds"]["postprocessor"]
    expected_cipher = [42 + 137 * i for i in range(20)]
    expected_post = [1_000_042 + 137 * i for i in range(20)]
    if cipher != expected_cipher or post != expected_post:
        raise RuntimeError("seed arrays do not match the frozen formulas")

    alphabet = manifest["representation"]["atomic_alphabet"]
    if len(alphabet) != len(set(alphabet)) or len(alphabet) != 26:
        raise RuntimeError("atomic alphabet must contain 26 unique symbols")

    external_bundle = repo / "voynich_decipherment_repro_bundle"
    sys.path.insert(0, str(external_bundle / "decipherment_attack"))
    from plant_crib_attack import collapse  # type: ignore

    expand = manifest["representation"]["expand_map"]
    for atom in alphabet:
        raw = expand.get(atom, atom)
        if collapse(raw) != atom:
            raise RuntimeError(f"collapse/expand round trip failed for {atom!r}")

    primary = manifest["configurations"]["primary"]
    if primary != {"beta": 0.5, "nu": 0.75, "replicates": 20}:
        raise RuntimeError("primary configuration changed")

    if manifest["status"] != "preregistered-awaiting-claude-review":
        raise RuntimeError("manifest status no longer reflects the execution embargo")

    print(json.dumps({
        "status": "PASS",
        "external_commit": commit,
        "verified_hashes": hashes,
        "criteria_match_frozen_cardan_manifest": True,
        "seed_pairs": len(cipher),
        "atomic_roundtrips": len(alphabet),
        "outcomes_generated": False,
    }, indent=2))


if __name__ == "__main__":
    main()
