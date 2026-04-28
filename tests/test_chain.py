"""Basic smoke test for the RAG chain (requires Ollama running)."""
import pytest

from app.infrastructure.embedder import get_embeddings
from app.domain.llm.chain import build_rag_chain
from app.domain.llm.ollama_client import get_llm
from app.domain.retrieval.retriever import get_retriever
from app.infrastructure.vectorstore import get_vectorstore


@pytest.mark.integration
def test_chain_returns_answer_and_sources():
    embeddings = get_embeddings()
    vectorstore = get_vectorstore(embeddings)
    retriever = get_retriever(vectorstore)
    llm = get_llm()
    chain = build_rag_chain(retriever, llm)
    result = chain.invoke("What is this documentation about?")
    assert isinstance(result["answer"], str)
    assert isinstance(result["sources"], list)
