from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()

@router.message(Command("settings"))
async def settings_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
    if not user:
        await message.answer("You are not registered yet. Use /start.")
        return
    status = "✅ ON" if user.notifications_enabled else "❌ OFF"
    await message.answer(
        f"⚙️ **Notification Settings**\n"
        f"Status: {status}\n\n"
        f"Use /mute to disable notifications.\n"
        f"Use /unmute to enable them again."
    )

@router.message(Command("mute"))
async def mute_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.notifications_enabled = False
            await session.commit()
            await message.answer("🔕 Notifications disabled. You'll still receive important system messages.")
        else:
            await message.answer("Register first with /start.")

@router.message(Command("unmute"))
async def unmute_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.notifications_enabled = True
            await session.commit()
            await message.answer("🔔 Notifications enabled!")
        else:
            await message.answer("Register first with /start.")
