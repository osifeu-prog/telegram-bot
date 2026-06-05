from src.core.state import state
from src.services.db import init_db
from src.services.redis import init_redis

async def bootstrap():
    print("BOOT START")

    state.db = init_db()

    try:
        state.redis = await init_redis()
    except Exception as e:
        print("REDIS ERROR:", e)
        state.redis = False

    print("BOOT DONE")
