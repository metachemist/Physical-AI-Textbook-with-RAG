"""POST /api/v1/translate — translate a chapter section to Urdu while preserving structure."""

import re
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.api.auth_middleware import get_current_user
from app.config import get_settings
from app.dependencies import get_db_pool

router = APIRouter(prefix="/api/v1")

_TRANSLATE_SYSTEM = (
    "You are a technical translator. Translate the provided Markdown section from English to Urdu.\n\n"
    "Rules:\n"
    "1. Translate ONLY prose text (paragraphs, list items, heading text).\n"
    "2. Preserve every heading level exactly (# → #, ## → ##, etc.).\n"
    "3. Preserve all bullet and numbered list nesting exactly.\n"
    "4. Preserve all bold (**text**), italic (*text*), and inline code (`code`) markers.\n"
    "5. Do NOT translate content inside fenced code blocks (``` ... ```).\n"
    "6. Do NOT translate URLs, file paths, variable names, or command-line arguments.\n"
    "7. Output ONLY the translated Markdown — no explanations, no preamble."
)


def _count_headings_by_level(md: str) -> dict[int, int]:
    counts: dict[int, int] = {}
    for line in md.splitlines():
        m = re.match(r"^(#{1,6})\s", line)
        if m:
            lvl = len(m.group(1))
            counts[lvl] = counts.get(lvl, 0) + 1
    return counts


def _count_code_fences(md: str) -> int:
    return len(re.findall(r"^(`{3,}|~{3,})", md, re.MULTILINE))


async def _call_openrouter(content: str, api_key: str, model: str) -> str:
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
                    {"role": "system", "content": _TRANSLATE_SYSTEM},
                    {"role": "user", "content": content},
                ],
                "stream": False,
            },
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


class TranslateRequest(BaseModel):
    markdown: str
    targetLanguage: str = "urdu"


class TranslateResponse(BaseModel):
    translatedMarkdown: str
    formatPreservedFailed: bool = False


@router.post("/translate", response_model=TranslateResponse)
async def translate(
    body: TranslateRequest,
    request: Request,
    user_id: UUID = Depends(get_current_user),
    pool=Depends(get_db_pool),
) -> TranslateResponse:
    limiter = request.app.state.limiter
    await limiter._check_request_limit(request, None, "20/minute")

    settings = get_settings()

    translated = await _call_openrouter(body.markdown, settings.openrouter_api_key, settings.llm_model)

    # Structural validation
    orig_headings = _count_headings_by_level(body.markdown)
    new_headings = _count_headings_by_level(translated)
    orig_fences = _count_code_fences(body.markdown)
    new_fences = _count_code_fences(translated)

    if orig_headings != new_headings or orig_fences != new_fences:
        return TranslateResponse(
            translatedMarkdown=body.markdown,
            formatPreservedFailed=True,
        )

    return TranslateResponse(translatedMarkdown=translated)
