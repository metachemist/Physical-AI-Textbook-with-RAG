from typing import AsyncGenerator

import asyncpg
from fastapi import Request
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from app.services.embedder import Embedder

_embedder: SentenceTransformer | None = None
_embedder_wrapper: Embedder | None = None


async def get_db_pool(request: Request) -> AsyncGenerator[asyncpg.Pool, None]:
    yield request.app.state.db_pool


async def get_qdrant_client(request: Request) -> AsyncGenerator[QdrantClient, None]:
    yield request.app.state.qdrant_client


async def get_embedder(request: Request) -> AsyncGenerator[Embedder, None]:
    global _embedder, _embedder_wrapper
    if _embedder is None:
        _embedder = SentenceTransformer(request.app.state.settings.embedding_model)
        _embedder_wrapper = Embedder(request.app.state.settings.embedding_model)
        _embedder_wrapper.model = _embedder
    yield _embedder_wrapper
