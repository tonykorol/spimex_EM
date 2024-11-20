from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import SpimexTradingResults


async def get_dynamics(
        oil_id,
        delivery_type_id,
        delivery_basis_id,
        start_date,
        end_date,
        session: AsyncSession
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