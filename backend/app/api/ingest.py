"""POST /api/v1/ingest — Admin-only trigger for content ingestion."""

import time

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from app.dependencies import get_embedder, get_qdrant_client
from app.services.embedder import Embedder
from app.services.ingestion import run_ingestion

router = APIRouter(prefix="/api/v1")


class IngestRequest(BaseModel):
    chapter_id: str
    doc_path: str


@router.post("/ingest")
async def ingest_chapter(
    body: IngestRequest,
    request: Request,
    qdrant: QdrantClient = Depends(get_qdrant_client),
    st_model: SentenceTransformer = Depends(get_embedder),
):
    settings = request.app.state.settings
    embedder = Embedder.__new__(Embedder)
    embedder.model = st_model

    # Derive module_id and base_url from chapter_id
    module_map = {
        "week-01": ("module-1-ros2", "/docs/module-1-ros2/week-01-ros2-fundamentals"),
        "week-02": ("module-1-ros2", "/docs/module-1-ros2/week-02-ros2-advanced"),
        "week-03": ("module-1-ros2", "/docs/module-1-ros2/week-03-ros2-tooling"),
        "week-04": ("module-1-ros2", "/docs/module-1-ros2/week-04-ros2-navigation"),
        "week-05": ("module-1-ros2", "/docs/module-1-ros2/week-05-ros2-capstone"),
        "week-06": ("module-2-simulation", "/docs/module-2-simulation/week-06-gazebo"),
        "week-07": ("module-2-simulation", "/docs/module-2-simulation/week-07-unity"),
        "week-08": ("module-3-nvidia-isaac", "/docs/module-3-nvidia-isaac/week-08-isaac-sim"),
        "week-09": ("module-3-nvidia-isaac", "/docs/module-3-nvidia-isaac/week-09-isaac-ros"),
        "week-10": ("module-3-nvidia-isaac", "/docs/module-3-nvidia-isaac/week-10-isaac-perceptor"),
        "week-11": ("module-4-vla-humanoid", "/docs/module-4-vla-humanoid/week-11-vla-foundations"),
        "week-12": ("module-4-vla-humanoid", "/docs/module-4-vla-humanoid/week-12-humanoid-platforms"),
        "week-13": ("module-4-vla-humanoid", "/docs/module-4-vla-humanoid/week-13-deployment"),
    }

    prefix = body.chapter_id[:7]  # e.g., "week-01"
    module_id, base_url = module_map.get(prefix, ("unknown", f"/docs/{body.chapter_id}"))

    start = time.monotonic()
    count = run_ingestion(
        doc_path=body.doc_path,
        chapter_id=body.chapter_id,
        module_id=module_id,
        base_url=base_url,
        collection_name=settings.qdrant_collection,
        qdrant=qdrant,
        embedder=embedder,
    )
    elapsed = int((time.monotonic() - start) * 1000)

    return {
        "apiVersion": "v1",
        "chapterId": body.chapter_id,
        "chunksUpserted": count,
        "durationMs": elapsed,
    }
