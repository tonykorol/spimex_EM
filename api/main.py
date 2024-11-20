from fastapi import FastAPI

from api.app.handlers.last_trading_dates import router as ltd_router
from api.app.handlers.dynamics import router as tr_router

app = FastAPI()

app.include_router(ltd_router, tags=["Last Trading Dates"])
app.include_router(tr_router, tags=["Trading Results"])
