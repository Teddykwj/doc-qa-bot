import uuid

from fastapi import APIRouter, Depends

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
