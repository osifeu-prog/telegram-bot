from src.core.settings import settings

async def init_redis():
    if not settings.REDIS_URL:
        print("REDIS OFF")
        return False

    from redis.asyncio import Redis

    r = Redis.from_url(settings.REDIS_URL)
    await r.ping()

    print("REDIS ON")
    return True
