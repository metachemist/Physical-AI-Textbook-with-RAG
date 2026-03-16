from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
async def health_check(request: Request) -> JSONResponse:
    checks = {"api": "ok", "database": "ok", "vectorStore": "ok"}
    status = "healthy"
    http_status = 200

    # Check database
    try:
        pool = request.app.state.db_pool
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
    except Exception:
        checks["database"] = "error"
        status = "unhealthy"
        http_status = 503

    # Check vector store
    try:
        qdrant = request.app.state.qdrant_client
        qdrant.get_collections()
    except Exception:
        checks["vectorStore"] = "error"
        status = "unhealthy"
        http_status = 503

    return JSONResponse(
        status_code=http_status,
        content={"apiVersion": "v1", "status": status, "checks": checks},
    )
