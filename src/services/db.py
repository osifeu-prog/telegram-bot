from sqlalchemy.ext.asyncio import create_async_engine
from src.core.settings import settings

engine = None

def init_db():
    global engine

    if not settings.DATABASE_URL:
        print("DB OFF")
        return False

    try:
        url = settings.DATABASE_URL.replace(
            "postgres://", "postgresql+asyncpg://"
        )
        engine = create_async_engine(url, pool_pre_ping=True)
        print("DB ON")
        return True
    except Exception as e:
        print("DB ERROR:", e)
        return False
