from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()

@router.message(Command("demo_deposit"))
async def demo_deposit_cmd(message: types.Message):
    """Add demo coins for testing  no real USDT required."""
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Usage: /demo_deposit <amount>\nExample: /demo_deposit 100")
        return
    try:
        amount = int(parts[1])
    except ValueError:
        await message.answer("Invalid amount. Use a number.")
        return
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        if not user:
            user = User(telegram_id=message.from_user.id, coins=0)
            session.add(user)
        user.coins += amount
        await session.commit()
    
    await message.answer(
        f"✅ {amount} DEMO coins added!\n"
        f"💰 New balance: {user.coins} coins\n\n"
        f"Use /shop or /buy to test purchases."
    )

