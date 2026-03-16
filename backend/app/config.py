from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection: str = "physical_ai_textbook"
    openrouter_api_key: str
    llm_model: str = "meta-llama/llama-3.1-8b-instruct:free"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    better_auth_secret: str = ""
    auth_service_url: str = "http://localhost:3001"
    allowed_origins: str = "http://localhost:3000"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def asyncpg_dsn(self) -> str:
        dsn = self.database_url
        if dsn.startswith("postgresql+asyncpg://"):
            dsn = dsn.replace("postgresql+asyncpg://", "postgresql://", 1)
        return dsn


def get_settings() -> Settings:
    from pathlib import Path

    env_path = Path(__file__).resolve().parent.parent / ".env"
    return Settings(_env_file=str(env_path))  # type: ignore[call-arg]
