"""Central config — all values overridable via environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3"
    llm_temperature: float = 0.0

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


settings = Settings()
