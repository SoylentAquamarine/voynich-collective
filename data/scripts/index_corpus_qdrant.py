#!/usr/bin/env python3
"""Embed the project's own logs/comms/knowledge-base/methods into Qdrant for semantic search.

This is a navigation aid over already-established findings, not a research tool: it
never generates, scores, or judges anything that enters a report or the knowledge
base. See comms/meetings/2026-09-20-steering-committee-05.md for the scope decision.

Usage:
    python data/scripts/index_corpus_qdrant.py [--ollama-url URL] [--qdrant-url URL]

Requires network access to the linuxbox Ollama (nomic-embed-text) and Qdrant instances.
"""
import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
COLLECTION = "voynich-collective"
EMBED_MODEL = "nomic-embed-text"
CHUNK_CHARS = 1800
CHUNK_OVERLAP = 200

GLOBS = [
    "logs/*.md",
    "comms/FromClaudeToChatGPT.md",
    "comms/FromChatGPTToClaude.md",
    "comms/meetings/*.md",
    "knowledge-base/state.md",
    "methods/*.md",
]


def http_json(url, payload=None, method=None, timeout=60):
    data = json.dumps(payload).encode() if payload is not None else None
    if method is None:
        method = "POST" if data is not None else "GET"
    req = urllib.request.Request(url, data=data, method=method,
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read()
        return json.loads(body) if body else {}


def chunk_text(text, size=CHUNK_CHARS, overlap=CHUNK_OVERLAP):
    """Chunk on markdown section boundaries first, falling back to fixed windows."""
    sections = re.split(r"\n(?=#{1,3} )", text)
    chunks = []
    for section in sections:
        if len(section) <= size:
            if section.strip():
                chunks.append(section.strip())
            continue
        start = 0
        while start < len(section):
            end = start + size
            chunks.append(section[start:end].strip())
            start = end - overlap
    return [c for c in chunks if c]


def stable_id(path, idx):
    return int(hashlib.sha256(f"{path}::{idx}".encode()).hexdigest()[:16], 16) % (2**63)


def ensure_collection(qdrant_url, dim):
    try:
        http_json(f"{qdrant_url}/collections/{COLLECTION}")
        return
    except Exception:
        pass
    http_json(
        f"{qdrant_url}/collections/{COLLECTION}",
        method="PUT",
        payload={"vectors": {"size": dim, "distance": "Cosine"}},
    )


def embed(ollama_url, text):
    d = http_json(f"{ollama_url}/api/embed",
                   payload={"model": EMBED_MODEL, "input": text}, timeout=60)
    return d["embeddings"][0]


def embed_batch(ollama_url, texts):
    d = http_json(f"{ollama_url}/api/embed",
                   payload={"model": EMBED_MODEL, "input": texts}, timeout=120)
    return d["embeddings"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ollama-url", default="http://10.0.0.154:11434")
    ap.add_argument("--qdrant-url", default="http://10.0.0.154:6333")
    args = ap.parse_args()

    files = []
    for pattern in GLOBS:
        files.extend(sorted(REPO.glob(pattern)))
    files = [f for f in files if f.is_file()]
    print(f"found {len(files)} files to index")

    all_chunks = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        rel = str(f.relative_to(REPO)).replace("\\", "/")
        for idx, chunk in enumerate(chunk_text(text)):
            all_chunks.append((rel, idx, chunk))
    print(f"{len(all_chunks)} chunks total")

    probe = embed(args.ollama_url, "dimension probe")
    dim = len(probe)
    print(f"embedding dim: {dim}")
    ensure_collection(args.qdrant_url, dim)

    BATCH = 16
    for start in range(0, len(all_chunks), BATCH):
        group = all_chunks[start:start + BATCH]
        vecs = embed_batch(args.ollama_url, [c[2] for c in group])
        points = [
            {
                "id": stable_id(rel, idx),
                "vector": vec,
                "payload": {"file": rel, "chunk_index": idx, "text": chunk},
            }
            for (rel, idx, chunk), vec in zip(group, vecs)
        ]
        http_json(f"{args.qdrant_url}/collections/{COLLECTION}/points",
                  method="PUT", payload={"points": points})
        print(f"  upserted {min(start + BATCH, len(all_chunks))}/{len(all_chunks)}")

    print(f"done. collection '{COLLECTION}' has {len(all_chunks)} points from {len(files)} files.")


if __name__ == "__main__":
    sys.exit(main())
