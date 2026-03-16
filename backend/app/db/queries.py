"""Typed query helpers for the messages and user_profiles tables.

All queries use asyncpg parameterized queries (no string interpolation).
"""

from typing import Any
from uuid import UUID

import asyncpg


async def get_session_messages(
    pool: asyncpg.Pool,
    session_id: str,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Fetch the most recent messages for a browser session, ordered oldest-first."""
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, session_id, user_id, chapter_id, role, content, citations, selected_text, created_at
            FROM messages
            WHERE session_id = $1
            ORDER BY created_at DESC
            LIMIT $2
            """,
            session_id,
            limit,
        )
    return [dict(r) for r in reversed(rows)]


async def save_message(
    pool: asyncpg.Pool,
    session_id: str,
    user_id: UUID | None,
    chapter_id: str,
    role: str,
    content: str,
    citations: list[dict[str, str]] | None = None,
    selected_text: str | None = None,
) -> UUID:
    """Persist a chat message and return its ID."""
    import json

    citations_json = json.dumps(citations) if citations else None
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO messages (session_id, user_id, chapter_id, role, content, citations, selected_text)
            VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7)
            RETURNING id
            """,
            session_id,
            user_id,
            chapter_id,
            role,
            content,
            citations_json,
            selected_text,
        )
    return row["id"]  # type: ignore[index]


async def get_user_profile(
    pool: asyncpg.Pool,
    user_id: UUID,
) -> dict[str, Any] | None:
    """Fetch a user's profile and compute the derived track."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT user_id, python_level, ros_experience, ai_knowledge FROM user_profiles WHERE user_id = $1",
            user_id,
        )
    if row is None:
        return None

    profile = dict(row)
    profile["derived_track"] = _derive_track(
        ros_experience=profile["ros_experience"],
        python_level=profile["python_level"],
        ai_knowledge=profile["ai_knowledge"],
    )
    return profile


async def upsert_user_profile(
    pool: asyncpg.Pool,
    user_id: UUID,
    python_level: str,
    ros_experience: bool,
    ai_knowledge: str,
) -> None:
    """Insert or update a user profile."""
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO user_profiles (user_id, python_level, ros_experience, ai_knowledge)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (user_id) DO UPDATE SET
                python_level = EXCLUDED.python_level,
                ros_experience = EXCLUDED.ros_experience,
                ai_knowledge = EXCLUDED.ai_knowledge,
                updated_at = now()
            """,
            user_id,
            python_level,
            ros_experience,
            ai_knowledge,
        )


def _derive_track(ros_experience: bool, python_level: str, ai_knowledge: str) -> str:
    """Priority-ordered rules table from spec FR-015."""
    if ros_experience:
        return "hardware_robotics"
    if python_level == "advanced" and ai_knowledge in ("intermediate", "advanced"):
        return "accelerated"
    if python_level in ("intermediate", "advanced"):
        return "software_engineer"
    return "beginner"
