"""Basic smoke test for the RAG chain (requires Ollama running)."""
import pytest

from src.ingestion.embedder import get_embeddings
from src.llm.chain import build_rag_chain
from src.llm.ollama_client import get_llm
from src.retrieval.retriever import get_retriever
from src.retrieval.vectorstore import get_vectorstore


@pytest.mark.integration
def test_chain_returns_string():
    embeddings = get_embeddings()
    vectorstore = get_vectorstore(embeddings)
    retriever = get_retriever(vectorstore)
    llm = get_llm()
    chain = build_rag_chain(retriever, llm)
    result = chain.invoke("What is this documentation about?")
    assert isinstance(result, str)
