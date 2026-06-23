from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()

@router.message(Command("language"))
async def language_cmd(message: types.Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply("Usage: /language <en|he|ru|ar|es|fr>")
        return
    lang = parts[1].lower()
    if lang not in ("en", "he", "ru", "ar", "es", "fr"):
        await message.reply("Supported: en, he, ru, ar, es, fr")
        return
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.language = lang
            await session.commit()
    await message.reply(f"✅ Language set to: {lang}")
