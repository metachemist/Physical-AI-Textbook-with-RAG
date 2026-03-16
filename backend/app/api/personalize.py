"""POST /api/v1/personalize — rewrite chapter section for the user's derived track."""

import re
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from app.api.auth_middleware import get_current_user
from app.config import get_settings
from app.db.queries import get_user_profile
from app.dependencies import get_db_pool

router = APIRouter(prefix="/api/v1")

_TRACK_PROMPTS: dict[str, str] = {
    "beginner": (
        "You are a textbook editor rewriting a section for a complete beginner. "
        "Use simple language, relatable analogies, and avoid unexplained jargon. "
        "Keep every heading, code block, and bullet point structurally identical to the original."
    ),
    "software_engineer": (
        "You are a textbook editor rewriting a section for an experienced software engineer "
        "new to robotics. Use API/integration analogies, reference common software patterns, "
        "and assume deep Python knowledge. "
        "Keep every heading, code block, and bullet point structurally identical to the original."
    ),
    "hardware_robotics": (
        "You are a textbook editor rewriting a section for a hardware engineer with robotics "
        "background but limited software experience. Emphasise physical intuition, sensor/actuator "
        "concepts, and embedded-system analogies. "
        "Keep every heading, code block, and bullet point structurally identical to the original."
    ),
    "accelerated": (
        "You are a textbook editor rewriting a section for an advanced AI/ML researcher. "
        "Be concise and technical. Use precise terminology, skip motivational explanations, "
        "and highlight novel or non-obvious aspects. "
        "Keep every heading, code block, and bullet point structurally identical to the original."
    ),
}


def _extract_headings(md: str) -> list[tuple[int, str]]:
    """Return (level, text) tuples for all ATX headings."""
    result = []
    for line in md.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            result.append((len(m.group(1)), m.group(2).strip()))
    return result


def _extract_code_fences(md: str) -> int:
    """Count the number of fenced code blocks (``` or ~~~)."""
    return len(re.findall(r"^(`{3,}|~{3,})", md, re.MULTILINE))


async def _call_openrouter(system_prompt: str, user_content: str, api_key: str, model: str) -> str:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                "stream": False,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


class PersonalizeRequest(BaseModel):
    markdown: str
    chapterId: str | None = None


class PersonalizeResponse(BaseModel):
    rewrittenMarkdown: str
    appliedTrack: str
    validationFailed: bool = False


@router.post("/personalize", response_model=PersonalizeResponse)
async def personalize(
    body: PersonalizeRequest,
    request: Request,
    user_id: UUID = Depends(get_current_user),
    pool=Depends(get_db_pool),
) -> PersonalizeResponse:
    limiter = request.app.state.limiter
    await limiter._check_request_limit(request, None, "20/minute")

    settings = get_settings()

    profile = await get_user_profile(pool, user_id)
    track = profile["derived_track"] if profile else "beginner"

    system_prompt = _TRACK_PROMPTS.get(track, _TRACK_PROMPTS["beginner"])

    rewritten = await _call_openrouter(
        system_prompt=system_prompt,
        user_content=f"Rewrite the following section:\n\n{body.markdown}",
        api_key=settings.openrouter_api_key,
        model=settings.llm_model,
    )

    # Structural validation
    orig_headings = _extract_headings(body.markdown)
    new_headings = _extract_headings(rewritten)
    orig_fences = _extract_code_fences(body.markdown)
    new_fences = _extract_code_fences(rewritten)

    if orig_headings != new_headings or orig_fences != new_fences:
        return PersonalizeResponse(
            rewrittenMarkdown=body.markdown,
            appliedTrack=track,
            validationFailed=True,
        )

    return PersonalizeResponse(rewrittenMarkdown=rewritten, appliedTrack=track)
