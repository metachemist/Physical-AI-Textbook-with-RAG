"""Profile endpoints — POST /api/v1/profile and GET /api/v1/profile."""

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.auth_middleware import get_current_user
from app.db.queries import get_user_profile, upsert_user_profile
from app.dependencies import get_db_pool

router = APIRouter(prefix="/api/v1")


class ProfileRequest(BaseModel):
    python_level: str  # "none" | "beginner" | "intermediate" | "advanced"
    ros_experience: str  # "none" | "beginner" | "intermediate" | "advanced"
    ai_knowledge: str  # "none" | "beginner" | "intermediate" | "advanced"


class ProfileResponse(BaseModel):
    python_level: str
    ros_experience: str
    ai_knowledge: str
    derivedTrack: str


@router.post("/profile", response_model=ProfileResponse)
async def set_profile(
    body: ProfileRequest,
    user_id: UUID = Depends(get_current_user),
    pool=Depends(get_db_pool),
) -> ProfileResponse:
    await upsert_user_profile(
        pool=pool,
        user_id=user_id,
        python_level=body.python_level,
        ros_experience=body.ros_experience,
        ai_knowledge=body.ai_knowledge,
    )
    profile = await get_user_profile(pool, user_id)
    return ProfileResponse(
        python_level=profile["python_level"],
        ros_experience=profile["ros_experience"],
        ai_knowledge=profile["ai_knowledge"],
        derivedTrack=profile["derived_track"],
    )


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(
    user_id: UUID = Depends(get_current_user),
    pool=Depends(get_db_pool),
) -> ProfileResponse:
    profile = await get_user_profile(pool, user_id)
    if profile is None:
        return ProfileResponse(
            python_level="none",
            ros_experience="none",
            ai_knowledge="none",
            derivedTrack="beginner",
        )
    return ProfileResponse(
        python_level=profile["python_level"],
        ros_experience=profile["ros_experience"],
        ai_knowledge=profile["ai_knowledge"],
        derivedTrack=profile["derived_track"],
    )
