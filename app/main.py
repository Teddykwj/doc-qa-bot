from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exceptions import register_exception_handlers
from app.api.routers import health, ingest, query
from app.service.scheduler import create_scheduler
from config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = create_scheduler(hour=settings.ingest_schedule_hour)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title="Doc QA Bot", lifespan=lifespan)

app.include_router(health.router)
app.include_router(query.router)
app.include_router(ingest.router)

register_exception_handlers(app)
