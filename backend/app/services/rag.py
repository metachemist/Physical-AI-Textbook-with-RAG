"""RAG retrieval + prompt assembly + OpenRouter streaming."""

import json
import time
from collections.abc import AsyncGenerator
from typing import Any

import httpx
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue, Prefetch, Query

from app.services.embedder import Embedder

SYSTEM_PROMPT = """You are a teaching assistant for the Physical AI & Humanoid Robotics textbook.
Answer the student's question using ONLY the provided context passages.

Rules:
1. Every factual claim must come from the context. Do not use your own knowledge.
2. If the context does not contain enough information to answer, say: "I couldn't find specific content on this topic in the textbook. Try rephrasing your question or asking about a related concept covered in the chapters."
3. Cite your sources using [Chapter: Section] format at the end of relevant sentences.
4. If the student highlighted text, address that passage directly in your first paragraph before expanding to related content.
5. Keep responses concise and student-friendly. Use examples from the context when available.
6. Do not mention that you are reading from "context passages" — respond naturally as if you know the textbook content."""

FALLBACK_MESSAGE = (
    "I couldn't find specific content on this topic in the textbook. "
    "Try rephrasing your question or asking about a related concept covered in the chapters."
)

SIMILARITY_THRESHOLD = 0.70


def retrieve_chunks(
    query_vector: list[float],
    qdrant: QdrantClient,
    collection_name: str,
    chapter_id: str | None = None,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Two-prefetch RRF retrieval: chapter-scoped + global."""
    prefetches = []
    if chapter_id:
        prefetches.append(
            Prefetch(
                query=query_vector,
                using="",
                limit=5,
                filter=Filter(must=[FieldCondition(key="chapter_id", match=MatchValue(value=chapter_id))]),
            )
        )
    prefetches.append(Prefetch(query=query_vector, using="", limit=10))

    results = qdrant.query_points(
        collection_name=collection_name,
        prefetch=prefetches,
        query=Query(fusion="rrf"),
        limit=top_k,
        with_payload=True,
    )

    chunks = []
    for point in results.points:
        chunks.append(
            {
                "score": point.score if point.score is not None else 0.0,
                **point.payload,
            }
        )
    return chunks


def build_prompt(
    question: str,
    chunks: list[dict[str, Any]],
    session_history: list[dict[str, Any]],
    selected_text_chunk: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    """Assemble the messages list for the LLM."""
    messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Inject context chunks
    context_parts = []
    if selected_text_chunk:
        context_parts.append(
            f"--- The student highlighted this passage ---\n"
            f"{selected_text_chunk.get('text', '')}\n"
            f"Source: {selected_text_chunk.get('source_url', '')}"
        )

    for chunk in chunks:
        heading = chunk.get("section_heading", "")
        chapter = chunk.get("chapter_id", "")
        text = chunk.get("text", "")
        url = chunk.get("source_url", "")
        context_parts.append(f"--- Context from [{heading}] in [{chapter}] ---\n{text}\nSource: {url}")

    if context_parts:
        messages.append({"role": "user", "content": "\n\n".join(context_parts)})
        messages.append({"role": "assistant", "content": "I've read the context passages. What's your question?"})

    # Inject session history (last 5 exchanges, or 3 for small context)
    for msg in session_history[-10:]:
        role = "user" if msg.get("role") == "user" else "assistant"
        messages.append({"role": role, "content": msg.get("content", "")})

    messages.append({"role": "user", "content": question})
    return messages


async def stream_openrouter(
    messages: list[dict[str, str]],
    api_key: str,
    model: str,
) -> AsyncGenerator[str, None]:
    """Stream tokens from OpenRouter."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        async with client.stream(
            "POST",
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "stream": True,
            },
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line.startswith("data: "):
                    continue
                data = line[6:]
                if data.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    if delta:
                        yield delta
                except json.JSONDecodeError:
                    continue


async def stream_response(
    question: str,
    chapter_id: str,
    session_id: str,
    selected_text: str | None,
    embedder: Embedder,
    qdrant: QdrantClient,
    collection_name: str,
    api_key: str,
    model: str,
    session_messages: list[dict[str, Any]],
) -> AsyncGenerator[str, None]:
    """Full RAG pipeline: embed → retrieve → threshold check → stream."""
    start = time.monotonic()

    # Handle selected text
    selected_text_chunk = None
    notice_short = False
    if selected_text:
        if len(selected_text) >= 20:
            sel_vector = embedder.embed_query(selected_text)
            sel_results = retrieve_chunks(sel_vector, qdrant, collection_name, chapter_id, top_k=1)
            if sel_results:
                selected_text_chunk = sel_results[0]
        else:
            notice_short = True

    # Main retrieval
    query_vector = embedder.embed_query(question)
    chunks = retrieve_chunks(query_vector, qdrant, collection_name, chapter_id, top_k=5)

    # Check similarity threshold
    top_score = chunks[0]["score"] if chunks else 0.0
    if top_score < SIMILARITY_THRESHOLD:
        event = json.dumps({
            "answer": FALLBACK_MESSAGE,
            "citations": [],
            "latencyMs": int((time.monotonic() - start) * 1000),
            "fallback": True,
            "noticeShort": notice_short,
            "done": True,
        })
        yield f"data: {event}\n\n"
        return

    # Build prompt and stream
    messages = build_prompt(question, chunks, session_messages, selected_text_chunk)

    full_answer = []
    async for delta in stream_openrouter(messages, api_key, model):
        full_answer.append(delta)
        event = json.dumps({"delta": delta, "done": False})
        yield f"data: {event}\n\n"

    # Final event with citations
    citations = []
    seen = set()
    for chunk in chunks:
        key = (chunk.get("chapter_id"), chunk.get("section_id"))
        if key not in seen:
            seen.add(key)
            citations.append({
                "chapterId": chunk.get("chapter_id", ""),
                "sectionId": chunk.get("section_id", ""),
                "sourceUrl": chunk.get("source_url", ""),
            })

    elapsed = int((time.monotonic() - start) * 1000)
    final_event = json.dumps({
        "answer": "".join(full_answer),
        "citations": citations,
        "latencyMs": elapsed,
        "noticeShort": notice_short,
        "done": True,
    })
    yield f"data: {final_event}\n\n"
