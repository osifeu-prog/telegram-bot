from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select, func
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User
import uuid

router = Router()

@router.message(Command("partner_register"))
async def partner_register_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        if not user:
            await message.answer("You must /start first.")
            return
        try:
            _ = user.partner_code
        except AttributeError:
            # Column still missing after migration? Run fix script.
            await message.answer("System update in progress. Please try again in a minute.")
            return
        if user.partner_code:
            await message.answer(f"You are already a partner! Code: `{user.partner_code}`")
            return
        user.partner_code = uuid.uuid4().hex[:8]
        session.add(user)
        await session.commit()
    bot_username = (await message.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref_{message.from_user.id}"
    await message.answer(
        f"🎉 You are now a partner!\n"
        f"Your referral link: {ref_link}\n"
        f"Commission: {user.partner_commission}%\n"
        f"Share it to earn!"
    )

@router.message(Command("partner_stats"))
async def partner_stats_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if not user or not getattr(user, 'partner_code', None):
            await message.answer("You are not a partner yet. Use /partner_register.")
            return
        result = await session.execute(
            select(func.count(User.telegram_id)).where(User.referrer_id == message.from_user.id)
        )
        referral_count = result.scalar()
    await message.answer(
        f"📊 **Partner Stats**\n"
        f"Referrals: {referral_count}\n"
        f"Commission rate: {user.partner_commission}%\n"
        f"Your code: `{user.partner_code}`"
    )
