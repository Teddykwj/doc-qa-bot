"""Retriever configuration (similarity search, MMR, etc.)."""
from langchain_core.vectorstores import VectorStore


def get_retriever(vectorstore: VectorStore, search_type: str = "similarity", k: int = 4):
    return vectorstore.as_retriever(search_type=search_type, search_kwargs={"k": k})
