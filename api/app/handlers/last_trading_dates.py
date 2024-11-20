from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.database.database import get_async_session
from api.app.schemas.schemas import SpimexLastTradingDatesListSchema
from api.app.services.last_trading_dates import get_last_trading_dates

router = APIRouter(prefix="/last_trading_dates")

@router.get("/", response_model=SpimexLastTradingDatesListSchema)
async def last_trading_dates(
        count: int = Query(ge=1, default=10),
        session: AsyncSession = Depends(get_async_session),
):
    result = await get_last_trading_dates(count, session)
    return {"dates": result}
