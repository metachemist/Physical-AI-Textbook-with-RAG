"""Orchestrates chunker → embedder → Qdrant upsert. Idempotent via deterministic UUID5 IDs."""

import uuid
from pathlib import Path

import tiktoken
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from app.services.chunker import chunk_chapter
from app.services.embedder import Embedder

NAMESPACE = uuid.NAMESPACE_URL


def _make_point_id(chapter_id: str, chunk_index: int) -> str:
    """Deterministic UUID5 for idempotent upsert."""
    return str(uuid.uuid5(NAMESPACE, f"physical-ai-textbook:{chapter_id}:{chunk_index}"))


def _count_tokens(text: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def run_ingestion(
    doc_path: str,
    chapter_id: str,
    module_id: str,
    base_url: str,
    collection_name: str,
    qdrant: QdrantClient,
    embedder: Embedder,
) -> int:
    """
    Read a chapter MDX file, chunk it, embed, and upsert to Qdrant.

    Returns the number of chunks upserted.
    """
    raw_mdx = Path(doc_path).read_text(encoding="utf-8")

    chunks = chunk_chapter(
        raw_mdx=raw_mdx,
        chapter_id=chapter_id,
        module_id=module_id,
        base_url=base_url,
    )

    if not chunks:
        return 0

    texts = [text for text, _ in chunks]
    vectors = embedder.embed_batch(texts)

    points = []
    for (text, metadata), vector in zip(chunks, vectors):
        point_id = _make_point_id(chapter_id, metadata["chunk_index"])
        payload = {
            **metadata,
            "token_count": _count_tokens(text),
            "text": text,
        }
        points.append(PointStruct(id=point_id, vector=vector, payload=payload))

    qdrant.upsert(collection_name=collection_name, wait=True, points=points)

    return len(points)
