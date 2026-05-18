import json
import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.deps import get_history_store, get_query_service
from app.api.schemas import QueryRequest, QueryResponse
from app.service.history_store import InMemoryHistoryStore
from app.service.query_service import QueryService

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    svc: QueryService = Depends(get_query_service),
    store: InMemoryHistoryStore = Depends(get_history_store),
):
    session_id = request.session_id or str(uuid.uuid4())
    history = store.get(session_id)
    result = await svc.answer(request.question, history)
    store.add_exchange(session_id, request.question, result["answer"])
    return QueryResponse(session_id=session_id, **result)


@router.post("/stream")
async def query_stream(
    request: QueryRequest,
    svc: QueryService = Depends(get_query_service),
    store: InMemoryHistoryStore = Depends(get_history_store),
):
    session_id = request.session_id or str(uuid.uuid4())
    history = store.get(session_id)

    async def event_generator():
        full_answer: list[str] = []
        async for event in svc.stream(request.question, history):
            yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
            if event["type"] == "token":
                full_answer.append(event["data"])
        store.add_exchange(session_id, request.question, "".join(full_answer))
        yield f"data: {json.dumps({'type': 'done', 'session_id': session_id})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
