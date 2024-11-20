from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.database.database import get_async_session
from api.app.schemas.schemas import SpimexTradingResultListSchema
from api.app.services.dynamics import get_dynamics

router = APIRouter(prefix="/trading_results")

@router.get("/", response_model=SpimexTradingResultListSchema)
async def trading_results(
        oil_id: str = Query(),
        delivery_type_id: str = Query(),
        delivery_basis_id: str = Query(),
        session: AsyncSession = Depends(get_async_session)
):
    result = await get_dynamics(oil_id, delivery_type_id, delivery_basis_id, session)
    return {"results": result}