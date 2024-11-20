from datetime import date, datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import SpimexTradingResults


async def get_dynamics(
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        session: AsyncSession,
        start_date: date = datetime.today().date(),
        end_date: date = datetime.today().date(),
) -> List[SpimexTradingResults]:

    stmt = await session.execute(
        select(SpimexTradingResults)
        .order_by(SpimexTradingResults.date)
        .filter(
            SpimexTradingResults.date >= start_date,
            SpimexTradingResults.date <= end_date,
            SpimexTradingResults.oil_id == oil_id.upper(),
            SpimexTradingResults.delivery_type_id == delivery_type_id.upper(),
            SpimexTradingResults.delivery_basis_id == delivery_basis_id.upper(),
        )
        .order_by(SpimexTradingResults.date)
    )
    result = stmt.unique().scalars().all()

    return result