from fastapi import APIRouter, Depends

from app.api.deps import get_query_service
from app.api.schemas import QueryRequest, QueryResponse
from app.service.query_service import QueryService

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
async def query(request: QueryRequest, svc: QueryService = Depends(get_query_service)):
    result = await svc.answer(request.question)
    return QueryResponse(**result)
