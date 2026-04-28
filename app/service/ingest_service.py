import hashlib

from langchain_chroma import Chroma

from app.domain.ingestion.loader import load_documents
from app.domain.ingestion.splitter import split_documents

from config.settings import settings


def _chunk_id(source: str, content: str) -> str:
    return hashlib.md5(f"{source}:{content}".encode()).hexdigest()


class IngestService:
    def __init__(self, vectorstore: Chroma):
        self._vectorstore = vectorstore

    def run(self, source_dir: str | None = None) -> int:
        source = source_dir or settings.data_raw_dir
        docs = load_documents(source)
        chunks = split_documents(docs, chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)

        ids = [_chunk_id(c.metadata.get("source", ""), c.page_content) for c in chunks]

        existing = set(self._vectorstore._collection.get(ids=ids)["ids"])
        new_pairs = [(chunk, id_) for chunk, id_ in zip(chunks, ids) if id_ not in existing]

        if new_pairs:
            new_chunks, new_ids = zip(*new_pairs)
            self._vectorstore.add_documents(list(new_chunks), ids=list(new_ids))

        return len(new_pairs)
