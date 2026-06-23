from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func, text
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User
import os

router = Router()
ADMIN_ID = int(os.getenv("ADMIN_ID", "8789977826"))
LAUNCH_DATE = datetime(2026, 7, 7, 12, 0, 0, tzinfo=timezone.utc)

# ----------------------------------------------
# COUNTDOWN
# ----------------------------------------------
def countdown_str():
    now = datetime.now(timezone.utc)
    delta = LAUNCH_DATE - now
    if delta.total_seconds() <= 0:
        return "🚀 We are LIVE!"
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    mins, secs = divmod(remainder, 60)
    return f"{days}d {hours}h {mins}m {secs}s"

# ----------------------------------------------
# USER COMMANDS
# ----------------------------------------------
@router.message(Command("teaser"))
async def teaser_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        coins = user.coins if user else 0
        streak = user.current_streak if user else 0
    text = (
        "🔥 SLH Investor Wallet  Countdown to Launch!\n\n"
        f"⏳ Time left: {countdown_str()}\n"
        f"💰 Your Genesis Shards: {coins}\n"
        f"📅 Daily streak: {streak} days\n\n"
        "Earn shards every day and climb the leaderboard!\n"
        "Top 100 at launch get exclusive VIP access."
    )
    await message.answer(text)

@router.message(Command("daily_quest"))
async def daily_quest_cmd(message: types.Message):
    today = datetime.now(timezone.utc).date()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(telegram_id=message.from_user.id, coins=0, current_streak=0)
            session.add(user)
        if user.last_daily and user.last_daily.date() == today:
            await message.answer("✅ Already claimed today's quest. Come back tomorrow!")
            return
        user.coins += 10
        if user.last_daily and user.last_daily.date() == today - timedelta(days=1):
            user.current_streak += 1
        else:
            user.current_streak = 1
        user.last_daily = datetime.now(timezone.utc)
        await session.commit()
        await message.answer(
            f"✅ Daily quest complete! +10 Shards\n"
            f"🔥 Streak: {user.current_streak} days\n"
            f"💰 Total Shards: {user.coins}"
        )

@router.message(Command("leaderboard"))
async def leaderboard_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.telegram_id, User.coins, User.current_streak)
            .order_by(User.coins.desc())
            .limit(20)
        )
        rows = result.all()
    if not rows:
        await message.answer("No participants yet.")
        return
    lines = ["🏆 Top Genesis Holders"]
    for i, (tid, coins, streak) in enumerate(rows, 1):
        lines.append(f"{i}. `{tid}`  {coins} Shards (🔥{streak}d)")
    await message.answer("\n".join(lines))

# ----------------------------------------------
# DAILY REVEAL
# ----------------------------------------------
last_reveal = None  # global store (basic; future: DB)

@router.message(Command("hint"))
async def hint_cmd(message: types.Message):
    global last_reveal
    if last_reveal:
        await message.answer(f"💡 Daily Reveal:\n{last_reveal}")
    else:
        await message.answer("No hint yet. Stay tuned!")

# ----------------------------------------------
# ADMIN COMMANDS
# ----------------------------------------------
def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("set_launch"))
async def set_launch_cmd(message: types.Message):
    if not is_admin(message):
        return await message.answer("⛔ Access denied.")
    global LAUNCH_DATE
    args = message.text.split()
    if len(args) != 2:
        await message.answer("Usage: /set_launch YYYY-MM-DD")
        return
    try:
        new_date = datetime.strptime(args[1], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        LAUNCH_DATE = new_date
        await message.answer(f"✅ Launch date set to {args[1]}")
    except:
        await message.answer("Invalid date format. Use YYYY-MM-DD")

@router.message(Command("send_quest"))
async def send_quest_cmd(message: types.Message):
    if not is_admin(message):
        return await message.answer("⛔ Access denied.")
    quest_text = message.text.removeprefix("/send_quest ").strip()
    if not quest_text:
        await message.answer("Usage: /send_quest <message>")
        return
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User.telegram_id))
        users = result.scalars().all()
    count = 0
    for uid in users:
        try:
            await message.bot.send_message(uid, f"☀️ Morning Quest: {quest_text}\n\nComplete /daily_quest to earn shards!")
            count += 1
        except:
            pass
    await message.answer(f"Quest sent to {count}/{len(users)} users.")

@router.message(Command("reveal"))
async def reveal_cmd(message: types.Message):
    if not is_admin(message):
        return await message.answer("⛔ Access denied.")
    global last_reveal
    hint_text = message.text.removeprefix("/reveal ").strip()
    if not hint_text:
        await message.answer("Usage: /reveal <hint text>")
        return
    last_reveal = hint_text
    # Broadcast hint to all users
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User.telegram_id))
        users = result.scalars().all()
    count = 0
    for uid in users:
        try:
            await message.bot.send_message(uid, f"💡 Daily Reveal: {hint_text}")
            count += 1
        except:
            pass
    await message.answer(f"Reveal sent to {count}/{len(users)} users.")
