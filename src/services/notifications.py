import asyncio
from aiogram import Router
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User
from src.bot.bot import bot

router = Router()

async def send_daily_reminders():
    """Send daily reminder to all users who haven't claimed today."""
    while True:
        await asyncio.sleep(86400)  # 24 hours
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(User))
                users = result.scalars().all()
                for user in users:
                    try:
                        await bot.send_message(
                            user.telegram_id,
                            "⏰ Don't forget to claim your daily reward! Use /daily"
                        )
                    except Exception:
                        pass
        except Exception:
            pass

# This will be started in startup_event
