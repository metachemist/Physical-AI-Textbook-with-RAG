"""FastAPI dependency for validating Better-Auth session tokens."""

from uuid import UUID

import asyncpg
from fastapi import Depends, HTTPException, Request

from app.dependencies import get_db_pool

_AUTH_REQUIRED = HTTPException(
    status_code=401,
    detail={"code": "AUTH_REQUIRED", "message": "Authentication required."},
)


async def get_current_user(
    request: Request,
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> UUID:
    """Extract Bearer token and validate against sessions table.

    Returns the user_id UUID of the authenticated user.
    Raises HTTP 401 if the token is missing, invalid, or expired.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise _AUTH_REQUIRED

    token = auth_header[7:].strip()
    if not token:
        raise _AUTH_REQUIRED

    row = await pool.fetchrow(
        "SELECT user_id FROM sessions WHERE token = $1 AND expires_at > now()",
        token,
    )
    if row is None:
        raise _AUTH_REQUIRED

    return UUID(str(row["user_id"]))
