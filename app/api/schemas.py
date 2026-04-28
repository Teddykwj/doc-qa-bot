from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


class IngestRequest(BaseModel):
    source_dir: str | None = None


class IngestResponse(BaseModel):
    message: str
    chunks_added: int
