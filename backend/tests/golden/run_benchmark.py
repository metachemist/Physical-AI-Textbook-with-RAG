#!/usr/bin/env python3
"""
Golden-set benchmark for the Physical AI Textbook RAG chatbot.

Phase A: Citation presence + Recall@10
  - POST /api/v1/chat for each of the 30 golden questions
  - Record citation_present (bool) and whether expected section appears in top-10 Qdrant results

Phase B: Write CSV for manual grounding review
  {question, response, citations, expected_section, grounded, uncertain, hallucinated}

Usage:
  BASE_URL=http://localhost:8000 python run_benchmark.py [--output-dir results/]
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import uuid
from pathlib import Path

import httpx
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

GOLDEN_SET_PATH = Path(__file__).parent / "golden_set.json"
DEFAULT_OUTPUT_DIR = Path(__file__).parent / "results"

CHAT_ENDPOINT = "/api/v1/chat"
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
COLLECTION = os.getenv("QDRANT_COLLECTION", "physical_ai_textbook")


def _load_golden() -> list[dict]:
    with GOLDEN_SET_PATH.open() as f:
        return json.load(f)


def _stream_chat(base_url: str, question: str, chapter_id: str, session_id: str) -> dict:
    """Call POST /api/v1/chat and accumulate the SSE stream. Returns parsed final event."""
    url = base_url.rstrip("/") + CHAT_ENDPOINT
    payload = {
        "message": question,
        "chapter_id": chapter_id,
        "session_id": session_id,
        "selected_text": None,
    }
    answer_parts: list[str] = []
    citations: list[dict] = []

    with httpx.Client(timeout=60.0) as client:
        with client.stream("POST", url, json=payload) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line.startswith("data: "):
                    continue
                raw = line[6:].strip()
                if not raw:
                    continue
                try:
                    event = json.loads(raw)
                    if event.get("done"):
                        citations = event.get("citations", [])
                        answer_parts.append(event.get("answer", ""))
                    elif event.get("delta"):
                        answer_parts.append(event["delta"])
                except json.JSONDecodeError:
                    pass

    answer = answer_parts[-1] if answer_parts else ""
    return {"answer": answer, "citations": citations}


def _recall_at_10(
    question: str,
    expected_section: str,
    embedder: SentenceTransformer,
    qdrant: QdrantClient,
) -> bool:
    """Return True if expected_section appears in top-10 Qdrant results."""
    vec = embedder.encode(question, normalize_embeddings=True).tolist()
    results = qdrant.search(
        collection_name=COLLECTION,
        query_vector=vec,
        limit=10,
        with_payload=True,
    )
    for point in results:
        if point.payload and point.payload.get("section_id") == expected_section:
            return True
        if point.payload and point.payload.get("chapter_id") == expected_section:
            return True
    return False


def run_phase_a(
    golden: list[dict],
    base_url: str,
    embedder: SentenceTransformer,
    qdrant: QdrantClient,
) -> list[dict]:
    results = []
    session_id = str(uuid.uuid4())
    for i, item in enumerate(golden, 1):
        print(f"[{i:2d}/30] {item['question'][:70]}…")
        t0 = time.monotonic()
        chat = _stream_chat(base_url, item["question"], item["expectedSection"], session_id)
        latency_ms = int((time.monotonic() - t0) * 1000)

        citation_present = len(chat["citations"]) > 0
        recall_hit = _recall_at_10(item["question"], item["expectedSection"], embedder, qdrant)

        results.append({
            **item,
            "answer": chat["answer"],
            "citations": chat["citations"],
            "citation_present": citation_present,
            "recall_at_10": recall_hit,
            "latency_ms": latency_ms,
            "grounded": "",
            "uncertain": "",
            "hallucinated": "",
        })
        print(f"       citations={'YES' if citation_present else 'NO ':3s}  recall10={'HIT' if recall_hit else 'MISS'}  latency={latency_ms}ms")

    return results


def write_csv(results: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    csv_path = output_dir / f"benchmark-{ts}.csv"
    fieldnames = [
        "question", "module", "difficulty", "expected_section",
        "answer", "citations", "citation_present", "recall_at_10", "latency_ms",
        "grounded", "uncertain", "hallucinated",
    ]
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in results:
            row_out = dict(row)
            row_out["citations"] = json.dumps(row_out["citations"])
            writer.writerow(row_out)
    print(f"\nCSV written to: {csv_path}")


def print_summary(results: list[dict]) -> None:
    total = len(results)
    citation_hits = sum(1 for r in results if r["citation_present"])
    recall_hits = sum(1 for r in results if r["recall_at_10"])
    avg_latency = sum(r["latency_ms"] for r in results) / total if total else 0
    print("\n" + "=" * 60)
    print(f"Citation presence : {citation_hits}/{total}  ({citation_hits/total*100:.1f}%)  [target ≥27/30]")
    print(f"Recall@10         : {recall_hits}/{total}  ({recall_hits/total*100:.1f}%)  [target ≥80%]")
    print(f"Avg latency       : {avg_latency:.0f}ms")
    print("=" * 60)
    if citation_hits < 27:
        print("⚠  Citation threshold NOT met — review chunking/retrieval pipeline")
    else:
        print("✓  Citation threshold met")
    if recall_hits / total < 0.80:
        print("⚠  Recall@10 target NOT met")
    else:
        print("✓  Recall@10 target met")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run golden-set RAG benchmark")
    parser.add_argument("--base-url", default=os.getenv("BASE_URL", "http://localhost:8000"))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")
    if not qdrant_url:
        print("ERROR: QDRANT_URL env var required", file=sys.stderr)
        sys.exit(1)

    print(f"Loading embedding model: {EMBED_MODEL}")
    embedder = SentenceTransformer(EMBED_MODEL)
    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_key)

    golden = _load_golden()
    print(f"Running {len(golden)} questions against {args.base_url}\n")

    results = run_phase_a(golden, args.base_url, embedder, qdrant)
    print_summary(results)
    write_csv(results, Path(args.output_dir))


if __name__ == "__main__":
    main()
