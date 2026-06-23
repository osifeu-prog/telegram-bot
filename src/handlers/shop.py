from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()

@router.message(Command("shop"))
async def shop_cmd(message: types.Message):
    await message.answer(
        "🛒 **Shop**\n\n"
        "⚡ Streak Boost  100 Stars\n"
        "Protect your streak if you miss a day.\n"
        "Use /buy to purchase.\n\n"
        "💎 Premium  Coming Soon\n"
        "Extra rewards, voting power, exclusive content."
    )

@router.message(Command("buy"))
async def buy_cmd(message: types.Message):
    await message.answer(
        "🛍️ **Buy Boost**\n\n"
        "Open the Mini App to complete your purchase:\n"
        "👉 Use the button below or visit the shop.\n\n"
        "Price: 100 Telegram Stars"
    )

@router.message(Command("premium"))
async def premium_cmd(message: types.Message):
    telegram_id = message.from_user.id
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        coins = user.coins if user else 0
    await message.answer(
        "💎 **Premium**\n\n"
        "Coming soon!\n"
        f"Your balance: {coins} coins\n\n"
        "Premium benefits:\n"
        "• 2x daily rewards\n"
        "• 3x voting power\n"
        "• Exclusive achievements\n"
        "• Priority support"
    )

