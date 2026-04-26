from functools import lru_cache

from app.infrastructure.embedder import get_embeddings
from app.domain.llm.chain import build_rag_chain
from app.domain.llm.ollama_client import get_llm
from app.domain.retrieval.retriever import get_retriever
from app.infrastructure.vectorstore import get_vectorstore
from app.service.ingest_service import IngestService
from app.service.query_service import QueryService
from config.settings import settings


@lru_cache
def _vectorstore():
    embeddings = get_embeddings(model=settings.embedding_model, base_url=settings.ollama_base_url)
    return get_vectorstore(embeddings)


@lru_cache
def _query_service() -> QueryService:
    retriever = get_retriever(_vectorstore(), k=settings.retriever_k)
    chain = build_rag_chain(retriever, get_llm())
    return QueryService(chain)


@lru_cache
def _ingest_service() -> IngestService:
    return IngestService(_vectorstore())


def get_query_service() -> QueryService:
    return _query_service()


def get_ingest_service() -> IngestService:
    return _ingest_service()
