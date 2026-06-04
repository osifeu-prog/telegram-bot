import os
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis

redis_url = os.getenv("REDIS_URL")

redis_client = redis.from_url(redis_url)
storage = RedisStorage(redis_client)
