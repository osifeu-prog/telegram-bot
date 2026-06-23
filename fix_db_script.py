import os, asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

async def main():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        # Drop and recreate users table
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        print("Old users table dropped.")
    # Now create tables using the models
    from src.bot.db.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, tables=[Base.metadata.tables["users"]])
        print("New users table created with all columns.")
    await engine.dispose()

asyncio.run(main())
