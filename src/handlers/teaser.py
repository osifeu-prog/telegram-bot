from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func, text
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User
from src.services.daily_rewards import claim_daily_reward
import os, asyncio, random
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()
ADMIN_ID = int(os.getenv("ADMIN_ID", "8789977826"))
LAUNCH_DATE = datetime(2026, 7, 7, 12, 0, 0, tzinfo=timezone.utc)
scheduler = AsyncIOScheduler()

def countdown_str():
    now = datetime.now(timezone.utc)
    delta = LAUNCH_DATE - now
    if delta.total_seconds() <= 0:
        return "🚀 We are LIVE!"
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    mins, secs = divmod(remainder, 60)
    return f"{days}d {hours}h {mins}m {secs}s"

# ---------- USER COMMANDS ----------
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
    async with AsyncSessionLocal() as session:
        claimed, coins, streak = await claim_daily_reward(
            session,
            message.from_user.id,
        )

    if not claimed:
        await message.answer("✅ Already claimed today's quest. Come back tomorrow!")
        return

    await message.answer(
        f"✅ Daily quest complete! +10 Shards\n"
        f"🔥 Streak: {streak} days\n"
        f"💰 Total Shards: {coins}"
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

# ---------- DAILY REVEAL (randomly every 2-3 days) ----------
last_reveal = None
reveal_list = [
    "We're building something huge! Stay tuned.",
    "Secret feature: Governance will give you real voting power!",
    "Rumour: There's a hidden achievement for 21-day streaks.",
    "Did you know? You can earn Shards by inviting friends.",
    "Exclusive access will be given to the Top 100 holders.",
    "The mini-app is getting a new look soon!",
    "A new shop item is coming: Boost your voting power!",
]
reveal_index = 0

async def send_daily_reveal(bot):
    global last_reveal, reveal_index
    hint = reveal_list[reveal_index % len(reveal_list)]
    reveal_index += 1
    last_reveal = hint
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User.telegram_id, User.notifications_enabled))
        users = result.all()
    for uid, enabled in users:
        if enabled:
            try:
                await bot.send_message(uid, f"💡 Daily Reveal: {hint}")
            except:
                pass
    # Schedule next reveal in 2-3 days at random hour
    next_delay = timedelta(days=random.randint(2, 3), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    scheduler.add_job(send_daily_reveal, 'date', run_date=datetime.now(timezone.utc) + next_delay, args=[bot])

@router.message(Command("hint"))
async def hint_cmd(message: types.Message):
    global last_reveal
    if last_reveal:
        await message.answer(f"💡 Daily Reveal:\n{last_reveal}")
    else:
        await message.answer("No hint yet. Stay tuned!")

# ---------- ADMIN COMMANDS ----------
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
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User.telegram_id, User.notifications_enabled))
        users = result.all()
    count = 0
    for uid, enabled in users:
        if enabled:
            try:
                await message.bot.send_message(uid, f"💡 Daily Reveal: {hint_text}")
                count += 1
            except:
                pass
    await message.answer(f"Reveal sent to {count}/{len(users)} users.")

# ---------- START SCHEDULER (without test job) ----------
def start_scheduler(bot):
    # Schedule first reveal only if no jobs exist (prevent duplicates)
    if not scheduler.get_jobs():
        next_delay = timedelta(days=random.randint(2, 3), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        scheduler.add_job(send_daily_reveal, 'date', run_date=datetime.now(timezone.utc) + next_delay, args=[bot])
    scheduler.start()
