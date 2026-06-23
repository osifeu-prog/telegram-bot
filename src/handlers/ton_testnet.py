from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import SystemConfig

router = Router()

TON_TESTNET_WALLET = "UQ...testnet_wallet_address..."  # Replace with your testnet wallet

@router.message(Command("testnet_wallet"))
async def testnet_wallet(message: types.Message):
    await message.answer(
        f"🧪 **TON Testnet Wallet**\n\n"
        f"Send test USDT here:\n"
        f"`{TON_TESTNET_WALLET}`\n\n"
        f"Use /testnet_deposit <tx_hash> <amount> to report."
    )

@router.message(Command("testnet_deposit"))
async def testnet_deposit(message: types.Message):
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Usage: /testnet_deposit <tx_hash> <amount>")
        return
    tx_hash = parts[1]
    try:
        amount = int(float(parts[2]) * 100)
    except ValueError:
        await message.answer("Invalid amount.")
        return
    # Auto-approve for testnet (demo)
    async with AsyncSessionLocal() as session:
        from src.bot.db.models import User
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.coins += amount
            await session.commit()
            await message.answer(f"✅ Testnet deposit approved! +{amount} coins")
        else:
            await message.answer("User not found.")

