from fastapi import FastAPI

from app.api.routers import health, ingest, query
from app.api.exceptions import register_exception_handlers

app = FastAPI(title="Doc QA Bot")

app.include_router(health.router)
app.include_router(query.router)
app.include_router(ingest.router)

register_exception_handlers(app)
