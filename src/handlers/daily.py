from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User
from src.handlers.achievements import check_and_award
from datetime import datetime, timezone, timedelta

router = Router()

@router.message(Command("daily"))
async def daily_cmd(message: types.Message):
    today = datetime.now(timezone.utc).date()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(telegram_id=message.from_user.id, coins=0, current_streak=0)
            session.add(user)
        if user.last_daily and user.last_daily.date() == today:
            await message.answer("✅ Already claimed today's reward. Come back tomorrow!")
            return
        user.coins += 10
        if user.last_daily and user.last_daily.date() == today - timedelta(days=1):
            user.current_streak += 1
        else:
            user.current_streak = 1
        user.last_daily = datetime.now(timezone.utc)
        await session.commit()
        await check_and_award(message.from_user.id, trigger='daily')
        await message.answer(
            f"✅ Daily reward claimed! +10 Shards\n"
            f"🔥 Streak: {user.current_streak} days\n"
            f"💰 Total Shards: {user.coins}"
        )

@router.message(Command("reward"))
async def reward_cmd(message: types.Message):
    # simple alias for daily
    await daily_cmd(message)

@router.message(Command("streak"))
async def streak_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
    if not user:
        await message.answer("You haven't started yet. Use /daily.")
    else:
        await message.answer(f"🔥 Your current streak: {user.current_streak} days")
