import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.app.cache.redis_client import redis_client
from api.app.handlers.last_trading_dates import router as ltd_router
from api.app.handlers.dynamics import router as dyn_router
from api.app.handlers.trading_results import router as tr_router
from api.logging_config import setup_logging

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Start app")
    await redis_client.connect()
    yield
    await redis_client.clear()
    await redis_client.close()
    logging.info("Stop app")

app = FastAPI(lifespan=lifespan)

app.include_router(ltd_router, tags=["Last Trading Dates"])
app.include_router(dyn_router, tags=["Dynamics"])
app.include_router(tr_router, tags=["Trading Results"])
