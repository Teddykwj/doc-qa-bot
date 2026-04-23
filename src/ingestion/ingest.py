"""Entry point: load docs → split → embed → store in ChromaDB."""
import argparse

from src.ingestion.loader import load_documents
from src.ingestion.splitter import split_documents
from src.ingestion.embedder import get_embeddings
from src.retrieval.vectorstore import get_vectorstore
from config.settings import settings


def ingest(source_dir: str | None = None):
    source = source_dir or settings.data_raw_dir
    print(f"Loading documents from: {source}")
    docs = load_documents(source)
    print(f"Loaded {len(docs)} documents")

    chunks = split_documents(docs, chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
    print(f"Split into {len(chunks)} chunks")

    embeddings = get_embeddings(model=settings.embedding_model, base_url=settings.ollama_base_url)
    vectorstore = get_vectorstore(embeddings, collection_name=settings.chroma_collection)
    vectorstore.add_documents(chunks)
    print("Ingestion complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=None)
    args = parser.parse_args()
    ingest(args.source)
