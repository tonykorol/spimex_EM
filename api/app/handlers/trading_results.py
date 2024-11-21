from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.cache.cache_services import generate_cache_key, get_cache, set_cache
from api.app.database.database import get_async_session
from api.app.schemas.schemas import SpimexTradingResultListSchema
from api.app.services.dynamics import get_dynamics

router = APIRouter(prefix="/trading_results")

@router.get("/", response_model=SpimexTradingResultListSchema)
async def trading_results(
        request: Request,
        oil_id: str = Query(),
        delivery_type_id: str = Query(),
        delivery_basis_id: str = Query(),
        session: AsyncSession = Depends(get_async_session)
):
    cache_key = await generate_cache_key(request.method, request.url)
    result = await get_cache(cache_key)
    if result is None:
        result = await get_dynamics(oil_id, delivery_type_id, delivery_basis_id, session)
        await set_cache(cache_key, result)
    return {"results": result}