"""POST /api/v1/chat — RAG chatbot streaming endpoint."""

import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient

from app.db.queries import get_session_messages, save_message
from app.dependencies import get_db_pool, get_qdrant_client
from app.services.embedder import Embedder
from app.services.rag import stream_response

router = APIRouter(prefix="/api/v1")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    chapter_id: str
    session_id: str
    selected_text: str | None = None


@router.post("/chat")
async def chat(
    body: ChatRequest,
    request: Request,
    qdrant: QdrantClient = Depends(get_qdrant_client),
):
    limiter = request.app.state.limiter
    await limiter._check_request_limit(request, None, "60/minute")

    settings = request.app.state.settings
    pool = request.app.state.db_pool

    # Build the Embedder from the cached SentenceTransformer model
    embedder = Embedder.__new__(Embedder)
    from app.dependencies import _embedder as st_model

    if st_model is None:
        from sentence_transformers import SentenceTransformer

        import app.dependencies

        app.dependencies._embedder = SentenceTransformer(settings.embedding_model)

    embedder.model = app.dependencies._embedder  # type: ignore[attr-defined]

    # Fetch session history
    session_messages = await get_session_messages(pool, body.session_id, limit=10)

    async def event_stream():
        full_answer_parts: list[str] = []
        citations: list[dict] = []

        async for chunk in stream_response(
            question=body.message,
            chapter_id=body.chapter_id,
            session_id=body.session_id,
            selected_text=body.selected_text,
            embedder=embedder,
            qdrant=qdrant,
            collection_name=settings.qdrant_collection,
            api_key=settings.openrouter_api_key,
            model=settings.llm_model,
            session_messages=session_messages,
        ):
            yield chunk
            # Parse the SSE event to capture the final answer
            if chunk.startswith("data: "):
                try:
                    data = json.loads(chunk[6:].strip())
                    if data.get("done"):
                        full_answer_parts.append(data.get("answer", ""))
                        citations = data.get("citations", [])
                    elif data.get("delta"):
                        full_answer_parts.append(data["delta"])
                except json.JSONDecodeError:
                    pass

        # Persist messages as a non-blocking background task
        final_answer = full_answer_parts[-1] if full_answer_parts and any(
            "done" in p for p in full_answer_parts
        ) else "".join(full_answer_parts)

        asyncio.create_task(_persist_messages(
            pool=pool,
            session_id=body.session_id,
            chapter_id=body.chapter_id,
            question=body.message,
            answer=final_answer,
            citations=citations,
            selected_text=body.selected_text,
        ))

    return StreamingResponse(event_stream(), media_type="text/event-stream")


async def _persist_messages(
    pool,
    session_id: str,
    chapter_id: str,
    question: str,
    answer: str,
    citations: list[dict],
    selected_text: str | None,
) -> None:
    """Save user question and assistant answer to the database."""
    try:
        await save_message(
            pool=pool,
            session_id=session_id,
            user_id=None,
            chapter_id=chapter_id,
            role="user",
            content=question,
            selected_text=selected_text,
        )
        await save_message(
            pool=pool,
            session_id=session_id,
            user_id=None,
            chapter_id=chapter_id,
            role="assistant",
            content=answer,
            citations=citations,
        )
    except Exception:
        # Background persistence failure should not crash the request
        pass
