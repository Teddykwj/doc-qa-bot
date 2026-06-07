"""Central config — all values overridable via environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Ollama (embedding only)
    ollama_base_url: str = "http://localhost:11434"
    llm_temperature: float = 0.0

    # Claude API
    anthropic_api_key: str = ""
    llm_model: str = "claude-haiku-4-5-20251001"

    # Embedding — swap model name here once decided
    embedding_model: str = "nomic-embed-text"

    # ChromaDB
    chroma_persist_dir: str = "data/processed/chroma"
    chroma_collection: str = "docs"

    # Ingestion
    data_raw_dir: str = "data/raw"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Retrieval
    retriever_k: int = 4

    # Scheduler
    ingest_schedule_hour: int = 3  # 매일 새벽 3시

    # CORS
    cors_origins: list[str] = ["http://localhost:8501"]


settings = Settings()
