import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.api.deps import _ingest_service, _query_service

logger = logging.getLogger(__name__)


async def _run_ingest() -> None:
    try:
        count = await _ingest_service().run()
        if count > 0:
            _query_service.cache_clear()  # BM25 인덱스 재구성을 위해 캐시 무효화
        logger.info("Scheduled ingest complete: %d new chunks", count)
    except Exception as e:
        logger.error("Scheduled ingest failed: %s", e)


def create_scheduler(hour: int) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(_run_ingest, "cron", hour=hour)
    return scheduler
