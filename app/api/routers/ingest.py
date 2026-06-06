import asyncio
import logging

from fastapi import APIRouter, BackgroundTasks, Depends

from app.api.deps import get_ingest_service
from app.api.schemas import IngestRequest, IngestResponse
from app.service.ingest_service import IngestService

router = APIRouter(prefix="/ingest", tags=["ingest"])
logger = logging.getLogger(__name__)


async def _run_ingest(svc: IngestService, source_dir: str | None) -> None:
    try:
        count = await svc.run(source_dir)
        logger.info("Ingestion complete. chunks_added=%d", count)
    except Exception as e:
        logger.error("Ingestion failed: %s", e)


@router.post("", response_model=IngestResponse, status_code=202)
async def ingest(
    request: IngestRequest,
    background_tasks: BackgroundTasks,
    svc: IngestService = Depends(get_ingest_service),
):
    background_tasks.add_task(_run_ingest, svc, request.source_dir)
    return IngestResponse(message="Ingestion started in background.", chunks_added=0)
