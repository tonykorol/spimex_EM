import json

from api.app.cache.redis_client import redis_client
from database.models import SpimexTradingResults


async def get_cache(key):
    cache = await redis_client.redis.get(key)
    if cache is None:
        return None
    return json.loads(cache)

async def set_cache(key: str, data: list):
    if isinstance(data[0], SpimexTradingResults):
        data = [obj.to_dict() for obj in data]
    await redis_client.redis.set(key, json.dumps(data))

async def clear_cache():
    if redis_client.redis:
        await redis_client.redis.flushdb()

async def generate_cache_key(method: str, url: str) -> str:
    key = f"{method}:{url}"
    return key


