import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

async def seed():
    async with AsyncSessionLocal() as session:
        for i in range(1, 101):
            user = User(
                telegram_id=1000000000 + i,
                coins=i * 10,
                current_streak=i % 7 + 1,
                last_daily=None,
                wallet_address=f"UQ_demo_{i:03d}",
                role="user",
                is_kyc=False
            )
            session.add(user)
        await session.commit()
    print("100 demo users created.")

if __name__ == "__main__":
    asyncio.run(seed())
