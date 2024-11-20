from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.schemas.schemas import SpimexLastTradingDatesListSchema
from database.models import SpimexTradingResults


async def get_last_trading_dates(count: int, session: AsyncSession) -> List[SpimexLastTradingDatesListSchema]:
    stmt = await session.execute(
        select(SpimexTradingResults.date)
        .order_by(SpimexTradingResults.date.desc())
        .distinct()
        .limit(count)
    )
    results = stmt.unique().scalars().all()
    results = [i.date() for i in results]
    return results
