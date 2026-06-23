from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()

ACHIEVEMENTS = {
    "streak_7": {"name": "Weekly Streak", "desc": "Maintain a 7-day streak", "reward": 100},
    "streak_30": {"name": "Monthly Streak", "desc": "Maintain a 30-day streak", "reward": 500},
    "first_deposit": {"name": "First Deposit", "desc": "Make your first USDT deposit", "reward": 200},
    "invite_10": {"name": "Influencer", "desc": "Invite 10 friends", "reward": 300},
}

@router.message(Command("achievements"))
async def achievements_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            await message.reply("No profile yet.")
            return
        msg = "🏆 **Achievements**\n\n"
        # Check each achievement
        if user.current_streak >= 7:
            msg += "✅ Weekly Streak (7 days)\n"
        else:
            msg += f"⏳ Weekly Streak ({user.current_streak}/7)\n"
        if user.coins > 0:
            msg += "✅ First Deposit\n"
        await message.reply(msg)
