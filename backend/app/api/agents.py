"""
POST /api/v1/agents/{agentName} — OpenAI Agents SDK dispatch router.

Agents:
  quiz_generator       — MCQ generation grounded in chapter chunks
  chapter_summarizer   — Summary + key points adapted to proficiency level
  prerequisite_mapper  — Prerequisite concepts with source URLs
"""

from __future__ import annotations

import json
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from qdrant_client import QdrantClient

from agents import Agent, Runner, function_tool, ModelSettings
from agents.models.openai_provider import OpenAIProvider
from openai import AsyncOpenAI

from app.api.auth_middleware import get_current_user
from app.config import get_settings
from app.dependencies import get_db_pool, get_qdrant_client, get_embedder
from app.services.embedder import Embedder

router = APIRouter(prefix="/api/v1")


# ---------------------------------------------------------------------------
# Custom OpenRouter model provider
# ---------------------------------------------------------------------------

def _make_openrouter_client(api_key: str) -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )


def _make_provider(api_key: str, model: str) -> OpenAIProvider:
    return OpenAIProvider(
        openai_client=_make_openrouter_client(api_key),
        model=model,
    )


# ---------------------------------------------------------------------------
# Shared Qdrant retrieval function tool
# ---------------------------------------------------------------------------

def make_retrieve_tool(embedder: Embedder, qdrant: QdrantClient, collection: str):
    @function_tool
    def retrieve_chunks(chapter_id: str, query: str, top_k: int = 8) -> str:
        """Retrieve the most relevant text chunks for a given query and chapter.

        Args:
            chapter_id: The chapter identifier (e.g. 'week-01-ros2-fundamentals').
            query: The search query or topic to retrieve chunks for.
            top_k: Number of chunks to return (default 8).

        Returns:
            JSON string with list of {text, section_heading, chapter_id, source_url}.
        """
        from qdrant_client.models import FieldCondition, Filter, MatchValue, Prefetch, Query as QQuery

        vec = embedder.embed_query(query)

        prefetches = [
            Prefetch(
                query=vec,
                using="",
                limit=top_k,
                filter=Filter(must=[FieldCondition(key="chapter_id", match=MatchValue(value=chapter_id))]),
            ),
            Prefetch(query=vec, using="", limit=top_k * 2),
        ]
        results = qdrant.query_points(
            collection_name=collection,
            prefetch=prefetches,
            query=QQuery(fusion="rrf"),
            limit=top_k,
            with_payload=True,
        )
        chunks = [
            {
                "text": p.payload.get("text", ""),
                "section_heading": p.payload.get("section_heading", ""),
                "chapter_id": p.payload.get("chapter_id", ""),
                "source_url": p.payload.get("source_url", ""),
            }
            for p in results.points
        ]
        return json.dumps(chunks)

    return retrieve_chunks


# ---------------------------------------------------------------------------
# Agent factory helpers
# ---------------------------------------------------------------------------

def build_quiz_agent(retrieve_tool, provider: OpenAIProvider, model: str) -> Agent:
    return Agent(
        name="quiz_generator",
        instructions=(
            "You generate multiple-choice quiz questions from textbook passages.\n"
            "1. Call retrieve_chunks to fetch content for the chapter and topic.\n"
            "2. If the combined text is fewer than 500 words, return exactly this JSON and nothing else:\n"
            '   {"error": "Insufficient content for a quiz on this section"}\n'
            "3. Otherwise generate the requested number of MCQs grounded in the retrieved text.\n"
            "4. Return ONLY valid JSON matching this schema (no markdown, no extra keys):\n"
            '   {"questions": [{"question": "...", "options": ["A","B","C","D"], '
            '"correctAnswer": "A", "explanation": "..."}]}'
        ),
        tools=[retrieve_tool],
        model=model,
        model_settings=ModelSettings(temperature=0.3, max_tokens=2048),
        model_provider=provider,
    )


def build_summarizer_agent(retrieve_tool, provider: OpenAIProvider, model: str) -> Agent:
    return Agent(
        name="chapter_summarizer",
        instructions=(
            "You summarize textbook chapters and extract key learning points.\n"
            "1. Call retrieve_chunks to fetch up to 12 chunks for the chapter.\n"
            "2. Adapt language complexity to the student's proficiency level:\n"
            "   - beginner: plain English, minimal jargon, relatable analogies\n"
            "   - intermediate: standard technical language\n"
            "   - advanced: precise terminology, concise\n"
            "3. Return ONLY valid JSON (no markdown, no extra keys):\n"
            '   {"summary": "...", "keyPoints": ["...", "...", "..."], '
            '"citations": [{"chapterId": "...", "sectionId": "...", "sourceUrl": "..."}]}'
        ),
        tools=[retrieve_tool],
        model=model,
        model_settings=ModelSettings(temperature=0.4, max_tokens=1024),
        model_provider=provider,
    )


def build_prereq_agent(retrieve_tool, provider: OpenAIProvider, model: str) -> Agent:
    return Agent(
        name="prerequisite_mapper",
        instructions=(
            "You identify prerequisite concepts needed to understand a given topic.\n"
            "1. Call retrieve_chunks to find relevant passages for the topic.\n"
            "2. Identify ≥2 prerequisite concepts referenced in the retrieved passages.\n"
            "3. For each prerequisite, link to the section URL from the retrieved chunks.\n"
            "4. Return ONLY valid JSON (no markdown, no extra keys):\n"
            '   {"prerequisites": [{"concept": "...", "description": "...", "sourceUrl": "..."}]}\n'
            "5. Every sourceUrl must come directly from a retrieved chunk's source_url field."
        ),
        tools=[retrieve_tool],
        model=model,
        model_settings=ModelSettings(temperature=0.2, max_tokens=1024),
        model_provider=provider,
    )


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class AgentRequest(BaseModel):
    chapterId: str
    # quiz_generator
    difficulty: str | None = "medium"
    count: int | None = 5
    # chapter_summarizer
    proficiencyLevel: str | None = "intermediate"
    # prerequisite_mapper
    topic: str | None = None


class ErrorResponse(BaseModel):
    error: str


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------

@router.post("/agents/{agent_name}")
async def run_agent(
    agent_name: str,
    body: AgentRequest,
    request: Request,
    user_id: UUID = Depends(get_current_user),
    pool=Depends(get_db_pool),
    qdrant: QdrantClient = Depends(get_qdrant_client),
    embedder: Embedder = Depends(get_embedder),
) -> Any:
    limiter = request.app.state.limiter
    await limiter._check_request_limit(request, None, "20/minute")

    settings = get_settings()
    provider = _make_provider(settings.openrouter_api_key, settings.llm_model)
    retrieve_tool = make_retrieve_tool(embedder, qdrant, settings.qdrant_collection)

    if agent_name == "quiz_generator":
        agent = build_quiz_agent(retrieve_tool, provider, settings.llm_model)
        prompt = (
            f"Generate {body.count} {body.difficulty} MCQs for chapter '{body.chapterId}'."
        )
    elif agent_name == "chapter_summarizer":
        agent = build_summarizer_agent(retrieve_tool, provider, settings.llm_model)
        prompt = (
            f"Summarize chapter '{body.chapterId}' for a {body.proficiencyLevel} student."
        )
    elif agent_name == "prerequisite_mapper":
        if not body.topic:
            raise HTTPException(status_code=422, detail="topic is required for prerequisite_mapper")
        agent = build_prereq_agent(retrieve_tool, provider, settings.llm_model)
        prompt = (
            f"Identify prerequisites for topic '{body.topic}' in chapter '{body.chapterId}'."
        )
    else:
        raise HTTPException(status_code=404, detail={"error": f"Unknown agent: {agent_name}"})

    result = await Runner.run(agent, prompt)
    raw = result.final_output

    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {"result": raw}
