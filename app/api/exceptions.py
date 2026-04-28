import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class DocQAError(Exception):
    status_code: int = 500


class OllamaConnectionError(DocQAError):
    status_code = 503


class VectorStoreError(DocQAError):
    status_code = 500


class IngestError(DocQAError):
    status_code = 422


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DocQAError)
    async def _(request: Request, exc: DocQAError):
        logger.error("[%s] %s %s — %s", type(exc).__name__, request.method, request.url.path, exc, exc_info=True)
        return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)})
