from redis.asyncio import Redis
from src.core.settings import settings

redis = Redis.from_url(settings.REDIS_URL)


async def publish(channel: str, data: str):
    await redis.publish(channel, data)


async def subscribe(channel: str):
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)
    return pubsub
