from fastapi import APIRouter, Depends

from app.api.deps import get_ingest_service
from app.api.schemas import IngestRequest, IngestResponse
from app.service.ingest_service import IngestService

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("", response_model=IngestResponse)
async def ingest(request: IngestRequest, svc: IngestService = Depends(get_ingest_service)):
    count = await svc.run(request.source_dir)
    return IngestResponse(message="Ingestion complete.", chunks_added=count)
