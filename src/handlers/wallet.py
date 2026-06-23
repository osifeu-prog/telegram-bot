from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User, SystemConfig

router = Router()

@router.message(Command("wallet"))
async def wallet_cmd(message: types.Message):
    """הצג את כתובת הארנק של המערכת + הארנק האישי"""
    async with AsyncSessionLocal() as session:
        # System wallet
        result = await session.execute(
            select(SystemConfig).where(SystemConfig.key == "system_wallet")
        )
        config = result.scalar_one_or_none()
        system_wallet = config.value if config else "Not configured"
        
        # User wallet
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        user_wallet = user.wallet_address if user and user.wallet_address else "Not set"
    
    await message.answer(
        f"🏦 **System Wallet (send USDT here):**\n"
        f"`{system_wallet}`\n\n"
        f"👤 **Your Wallet (receive payments):**\n"
        f"`{user_wallet}`\n\n"
        f"💡 Use /set_wallet <address> to set your USDT wallet.\n"
        f"💡 Use /deposit to report a payment."
    )

@router.message(Command("set_wallet"))
async def set_wallet_cmd(message: types.Message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        await message.answer("Usage: /set_wallet <your_usdt_wallet_address>")
        return
    address = parts[1].strip()
    if len(address) < 30:
        await message.answer("❌ Invalid wallet address. Please enter a valid TON USDT address.")
        return
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        if not user:
            user = User(telegram_id=message.from_user.id, wallet_address=address)
            session.add(user)
        else:
            user.wallet_address = address
        await session.commit()
    
    await message.answer(
        f"✅ Your USDT wallet has been set:\n"
        f"`{address}`\n\n"
        f"You can now receive payments from the system."
    )

@router.message(Command("deposit"))
async def deposit_cmd(message: types.Message):
    """הוראות להפקדה"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SystemConfig).where(SystemConfig.key == "system_wallet")
        )
        config = result.scalar_one_or_none()
        system_wallet = config.value if config else "Not configured"
    
    await message.answer(
        "💸 **How to Deposit USDT**\n\n"
        "1️⃣ Send USDT to the system wallet:\n"
        f"`{system_wallet}`\n\n"
        "2️⃣ Copy the transaction hash (TXID)\n\n"
        "3️⃣ Report it with:\n"
        "/report_deposit <tx_hash> <amount_in_usdt>\n\n"
        "Example: `/report_deposit abc123def 50`\n\n"
        "⏳ An admin will verify and credit your account."
    )

