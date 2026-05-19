from langchain_community.retrievers import BM25Retriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore


def get_retriever(vectorstore: VectorStore, k: int = 4) -> BaseRetriever:
    return vectorstore.as_retriever(search_kwargs={"k": k})


class HybridRetriever(BaseRetriever):
    """Combines BM25 and vector retrieval using Reciprocal Rank Fusion."""

    bm25: BM25Retriever
    vector: BaseRetriever
    k: int = 4
    rrf_k: int = 60  # RRF constant — higher = less weight to top ranks

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> list[Document]:
        bm25_docs = self.bm25.invoke(query)
        vector_docs = self.vector.invoke(query)

        scores: dict[str, float] = {}
        doc_map: dict[str, Document] = {}

        for rank, doc in enumerate(bm25_docs):
            key = doc.page_content
            scores[key] = scores.get(key, 0) + 1 / (rank + self.rrf_k)
            doc_map[key] = doc

        for rank, doc in enumerate(vector_docs):
            key = doc.page_content
            scores[key] = scores.get(key, 0) + 1 / (rank + self.rrf_k)
            doc_map[key] = doc

        ranked = sorted(scores, key=lambda k: scores[k], reverse=True)
        return [doc_map[key] for key in ranked[: self.k]]


def get_hybrid_retriever(vectorstore: VectorStore, k: int = 4) -> BaseRetriever:
    result = vectorstore._collection.get(include=["documents", "metadatas"])
    docs = [
        Document(page_content=text, metadata=meta or {})
        for text, meta in zip(result["documents"], result["metadatas"])
    ]

    if not docs:
        return get_retriever(vectorstore, k=k)

    bm25 = BM25Retriever.from_documents(docs, k=k)
    vector = get_retriever(vectorstore, k=k)
    return HybridRetriever(bm25=bm25, vector=vector, k=k)
