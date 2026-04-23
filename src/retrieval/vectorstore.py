"""ChromaDB vectorstore factory."""
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings

from config.settings import settings


def get_vectorstore(embeddings: Embeddings, collection_name: str | None = None) -> Chroma:
    return Chroma(
        collection_name=collection_name or settings.chroma_collection,
        embedding_function=embeddings,
        persist_directory=settings.chroma_persist_dir,
    )
