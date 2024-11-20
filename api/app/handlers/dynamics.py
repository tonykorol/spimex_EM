from datetime import date, datetime

from fastapi import APIRouter
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.database.database import get_async_session
from api.app.schemas.schemas import SpimexTradingResultListSchema
from api.app.services.dynamics import get_dynamics

router = APIRouter(prefix='/dynamics')

@router.get('/', response_model=SpimexTradingResultListSchema)
async def dynamics(
        oil_id: str = Query(),
        delivery_type_id: str = Query(),
        delivery_basis_id: str = Query(),
        start_date: date = Query(),
        end_date: date = Query(default=datetime.today().date()),
        session: AsyncSession = Depends(get_async_session)
):
    result = await get_dynamics(
        oil_id,
        delivery_type_id,
        delivery_basis_id,
        start_date,
        end_date,
        session)
    return {"results": result}
