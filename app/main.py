from fastapi import FastAPI

from app.api.routers import health, ingest, query

app = FastAPI(title="Doc QA Bot")

app.include_router(health.router)
app.include_router(query.router)
app.include_router(ingest.router)
