"""FastAPI app — thin layer over the RAG chain."""
from fastapi import FastAPI
from pydantic import BaseModel

from src.ingestion.embedder import get_embeddings
from src.llm.chain import build_rag_chain
from src.llm.ollama_client import get_llm
from src.retrieval.retriever import get_retriever
from src.retrieval.vectorstore import get_vectorstore
from config.settings import settings

app = FastAPI(title="Doc QA Bot")

embeddings = get_embeddings(model=settings.embedding_model, base_url=settings.ollama_base_url)
vectorstore = get_vectorstore(embeddings)
retriever = get_retriever(vectorstore, k=settings.retriever_k)
llm = get_llm()
chain = build_rag_chain(retriever, llm)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    answer = chain.invoke(request.question)
    return QueryResponse(answer=answer)


@app.get("/health")
def health():
    return {"status": "ok"}
