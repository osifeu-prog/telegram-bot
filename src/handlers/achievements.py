from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User
import json

router = Router()

# רשימת ההישגים (id, description, secret)
ALL_ACHIEVEMENTS = {
    "first_daily": ("First Daily", "Complete your first daily quest", False),
    "streak_7": ("Week Warrior", "7-day streak", False),
    "streak_30": ("Monthly Legend", "30-day streak", False),
    "coins_1000": ("Coin Collector", "Earn 1000 Shards", False),
    "coins_10000": ("Shard Hoarder", "Earn 10000 Shards", False),
    "referral_1": ("Friend Bringer", "Invite 1 friend", False),
    "referral_5": ("Team Builder", "Invite 5 friends", False),
    "voter": ("Voice of the People", "Vote on a proposal", False),
    "streak_21": ("Secret Keeper", "21-day streak (secret!)", True),
}

async def check_and_award(user_id: int, trigger: str = None):
    """בדוק הישגים לפי trigger או סטטוס נוכחי."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return
        achieved = set(json.loads(user.achievements or "[]"))
        new_achievements = []
        # triggers
        if trigger == "daily":
            achieved.add("first_daily")  # always give on first daily (idempotent)
            if user.current_streak >= 7:
                achieved.add("streak_7")
            if user.current_streak >= 30:
                achieved.add("streak_30")
            if user.current_streak >= 21:
                achieved.add("streak_21")
        if user.coins >= 1000:
            achieved.add("coins_1000")
        if user.coins >= 10000:
            achieved.add("coins_10000")
        # referrals: we don't count here; will be checked when referral is done
        # votes: same
        updated = list(achieved - set(json.loads(user.achievements or "[]")))
        if updated:
            user.achievements = json.dumps(list(achieved))
            await session.commit()
            return updated

@router.message(Command("achievements"))
async def achievements_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
    if not user:
        await message.answer("You aren't registered yet. Use /start.")
        return
    achieved = json.loads(user.achievements or "[]")
    lines = ["🏅 **Your Achievements**"]
    for ach_id, (name, desc, secret) in ALL_ACHIEVEMENTS.items():
        if ach_id in achieved:
            lines.append(f"✅ {name}  {desc}")
        elif not secret:
            lines.append(f"🔒 {name}  {desc}")
        # secret ones hidden if not achieved
    await message.answer("\n".join(lines))
