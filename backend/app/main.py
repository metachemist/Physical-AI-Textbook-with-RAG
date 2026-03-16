from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config import get_settings
from app.db.pool import close_pool, init_pool

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    # Init asyncpg pool
    pool = await init_pool(settings.asyncpg_dsn)
    app.state.db_pool = pool

    # Init Qdrant client and ensure collection exists
    qdrant = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    app.state.qdrant_client = qdrant

    if not qdrant.collection_exists(settings.qdrant_collection):
        qdrant.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        qdrant.create_payload_index(settings.qdrant_collection, "chapter_id", "keyword")
        qdrant.create_payload_index(settings.qdrant_collection, "section_id", "keyword")

    app.state.settings = settings

    yield

    await close_pool(pool)
    qdrant.close()


def create_app() -> FastAPI:
    app = FastAPI(title="Physical AI Textbook API", version="1", lifespan=lifespan)

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    settings_for_cors = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings_for_cors.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.api.health import router as health_router
    from app.api.ingest import router as ingest_router
    from app.api.chat import router as chat_router
    from app.api.profile import router as profile_router
    from app.api.agents import router as agents_router
    from app.api.personalize import router as personalize_router
    from app.api.translate import router as translate_router

    app.include_router(health_router)
    app.include_router(ingest_router)
    app.include_router(chat_router)
    app.include_router(profile_router)
    app.include_router(agents_router)
    app.include_router(personalize_router)
    app.include_router(translate_router)

    return app


app = create_app()
