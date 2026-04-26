from langchain_chroma import Chroma

from app.domain.ingestion.loader import load_documents
from app.domain.ingestion.splitter import split_documents

from config.settings import settings


class IngestService:
    def __init__(self, vectorstore: Chroma):
        self._vectorstore = vectorstore

    def run(self, source_dir: str | None = None) -> int:
        source = source_dir or settings.data_raw_dir
        docs = load_documents(source)
        chunks = split_documents(docs, chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
        self._vectorstore.add_documents(chunks)
        return len(chunks)
