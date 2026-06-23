import os
import redis.asyncio as redis

r = redis.from_url(os.getenv("REDIS_URL"))

async def set_user_state(user_id: int, state: str):
    await r.set(f"user:{user_id}:state", state)

async def get_user_state(user_id: int):
    return await r.get(f"user:{user_id}:state")




