from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User, Purchase

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("report_deposit"))
async def report_deposit_cmd(message: types.Message):
    parts = message.text.split()
    if len(parts) < 3:
        await message.reply("Usage: /report_deposit <tx_hash> <amount_in_usdt>")
        return
    tx_hash = parts[1]
    try:
        amount = int(float(parts[2]) * 100)  # Convert to cents
    except ValueError:
        await message.reply("Invalid amount.")
        return
    
    async with AsyncSessionLocal() as session:
        purchase = Purchase(
            telegram_id=message.from_user.id,
            item="deposit",
            amount_usdt=amount,
            tx_hash=tx_hash,
            status="pending"
        )
        session.add(purchase)
        await session.commit()
        purchase_id = purchase.id
    
    await message.reply(
        f"📩 Deposit reported!\n"
        f"ID: #{purchase_id}\n"
        f"TX: `{tx_hash}`\n"
        f"Amount: {amount/100:.2f} USDT\n\n"
        f"⏳ Waiting for admin confirmation."
    )

@router.message(Command("confirm_deposit"))
async def confirm_deposit_cmd(message: types.Message):
    if not is_admin(message):
        await message.reply("⛔ Access denied.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply("Usage: /confirm_deposit <purchase_id>")
        return
    try:
        purchase_id = int(parts[1])
    except ValueError:
        await message.reply("Invalid ID.")
        return
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Purchase).where(Purchase.id == purchase_id))
        purchase = result.scalar_one_or_none()
        if not purchase:
            await message.reply("Purchase not found.")
            return
        if purchase.status != "pending":
            await message.reply(f"Already {purchase.status}.")
            return
        
        purchase.status = "confirmed"
        # Credit user
        result = await session.execute(select(User).where(User.telegram_id == purchase.telegram_id))
        user = result.scalar_one_or_none()
        if user:
            # 1 USDT = 100 coins
            coins_to_add = purchase.amount_usdt // 100 * 100
            user.coins += coins_to_add
            # Auto-verify if first deposit
            if not user.is_kyc:
                user.is_kyc = True
                user.role = "verified"
        await session.commit()
    
    await message.reply(
        f"✅ Deposit #{purchase_id} confirmed!\n"
        f"User: {purchase.telegram_id}\n"
        f"Amount: {purchase.amount_usdt/100:.2f} USDT"
    )
