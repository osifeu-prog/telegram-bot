from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select, func
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()
REFERRAL_BONUS = 50

@router.message(Command("ref"))
async def ref_cmd(message: types.Message):
    bot_username = (await message.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref_{message.from_user.id}"
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(func.count(User.telegram_id)).where(User.referrer_id == message.from_user.id)
        )
        count = result.scalar()
    await message.answer(
        f"👥 **Referral System**\n\n"
        f"Your referral link:\n{ref_link}\n\n"
        f"Friends invited: {count}\n"
        f"Bonus per friend: {REFERRAL_BONUS} coins\n\n"
        f"Share the link to earn!"
    )

@router.message(Command("start"))
async def start_with_ref(message: types.Message):
    # Check for referral code
    args = message.text.split()
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            ref_id = int(args[1][4:])
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
                user = result.scalar_one_or_none()
                if user and user.referrer_id is None:
                    user.referrer_id = ref_id
                    user.coins += REFERRAL_BONUS
                    # Give bonus to referrer
                    referrer = await session.get(User, ref_id)
                    if referrer:
                        referrer.coins += REFERRAL_BONUS
                    await session.commit()
                    await message.answer("🎉 You were referred! +50 bonus coins!")
        except:
            pass
    # Continue with normal start
    await message.answer("Welcome! Use /daily to get your first reward.")

