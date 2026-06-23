from datetime import datetime, timedelta
from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()

@router.message(Command("daily"))
async def daily_reward(message: types.Message):
    telegram_id = message.from_user.id
    now = datetime.utcnow()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id, coins=0, current_streak=0)
            session.add(user)
            await session.commit()
        if user.last_daily and now - user.last_daily < timedelta(hours=24):
            next_time = user.last_daily + timedelta(hours=24)
            await message.reply(f"? Already claimed today. Try again after {next_time.strftime('%H:%M')}.")
            return
        if user.last_daily and now - user.last_daily < timedelta(hours=48):
            user.current_streak += 1
        else:
            user.current_streak = 1
        streak_bonus = min(user.current_streak * 2, 40)
        reward = 10 + streak_bonus
        user.coins += reward
        user.last_daily = now
        await session.commit()
        await message.reply(
            f"?? Daily reward!\n+{reward} coins\n?? Streak: {user.current_streak} days\n?? Balance: {user.coins} coins"
        )

@router.message(Command("balance"))
async def balance_cmd(message: types.Message):
    telegram_id = message.from_user.id
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user:
            await message.reply(f"?? {user.coins} coins | ?? {user.current_streak} day streak")
        else:
            await message.reply("You haven't started yet. Use /daily!")

@router.message(Command("top"))
async def top_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).order_by(User.coins.desc()).limit(10))
        top_users = result.scalars().all()
        if not top_users:
            await message.reply("No users yet.")
            return
        lines = ["?? Top 10:"]
        for i, user in enumerate(top_users, start=1):
            lines.append(f"{i}. {user.telegram_id} - {user.coins} coins")
        await message.reply("\n".join(lines))
