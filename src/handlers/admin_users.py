from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("user_info"))
async def user_info_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Usage: /user_info <telegram_id>")
        return
    try:
        tid = int(parts[1])
    except ValueError:
        await message.answer("Invalid ID.")
        return
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == tid))
        user = result.scalar_one_or_none()
        if user:
            await message.answer(
                f"👤 User: `{user.telegram_id}`\n"
                f"💰 Coins: {user.coins}\n"
                f"🔥 Streak: {user.current_streak}\n"
                f"⚡ Boosts: {user.boosts_available}\n"
                f"📅 Last Daily: {user.last_daily}\n"
                f"🕐 Created: {user.created_at}"
            )
        else:
            await message.answer("User not found.")

@router.message(Command("user_reset"))
async def user_reset_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Usage: /user_reset <telegram_id>")
        return
    try:
        tid = int(parts[1])
    except ValueError:
        await message.answer("Invalid ID.")
        return
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == tid))
        user = result.scalar_one_or_none()
        if user:
            user.coins = 0
            user.current_streak = 0
            user.last_daily = None
            user.boosts_available = 0
            await session.commit()
            await message.answer("✅ User reset.")
        else:
            await message.answer("User not found.")

@router.message(Command("ban"))
async def ban_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    await message.answer("🚫 Ban feature placeholder. Implement via DB flag if needed.")

@router.message(Command("unban"))
async def unban_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    await message.answer("✅ Unban feature placeholder. Implement via DB flag if needed.")

