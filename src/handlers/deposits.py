from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User, Purchase, SystemConfig
from src.services.ton import verify_usdt_transfer

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("report_deposit"))
async def report_deposit_cmd(message: types.Message):
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Usage: /report_deposit <tx_hash> <amount_in_usdt>")
        return
    tx_hash = parts[1]
    try:
        amount = int(float(parts[2]) * 100)
    except ValueError:
        await message.answer("Invalid amount.")
        return

    async with AsyncSessionLocal() as session:
        # Get system wallet
        result = await session.execute(select(SystemConfig).where(SystemConfig.key == "system_wallet"))
        config = result.scalar_one_or_none()
        system_wallet = config.value if config else None

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

        # Auto-verify if system wallet is set
        if system_wallet:
            try:
                valid = await verify_usdt_transfer(tx_hash, amount, system_wallet)
            except Exception:
                valid = False
            if valid:
                purchase.status = "confirmed"
                result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
                user = result.scalar_one_or_none()
                if user:
                    coins_to_add = amount // 100 * 100
                    user.coins += coins_to_add
                    if not user.is_kyc:
                        user.is_kyc = True
                        user.role = "verified"
                await session.commit()
                await message.answer(
                    f"✅ Deposit verified automatically!\n"
                    f"ID: #{purchase_id}\n"
                    f"Amount: {amount/100:.2f} USDT → {coins_to_add} coins"
                )
                return

    await message.answer(
        f"📩 Deposit reported!\n"
        f"ID: #{purchase_id}\n"
        f"TX: `{tx_hash}`\n"
        f"Amount: {amount/100:.2f} USDT\n"
        f"⏳ Verification pending. Use /verify_deposit {purchase_id} to check manually."
    )

@router.message(Command("verify_deposit"))
async def verify_deposit_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Usage: /verify_deposit <purchase_id>")
        return
    try:
        purchase_id = int(parts[1])
    except ValueError:
        await message.answer("Invalid ID.")
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Purchase).where(Purchase.id == purchase_id))
        purchase = result.scalar_one_or_none()
        if not purchase or purchase.status != "pending":
            await message.answer("Not found or already processed.")
            return

        config = await session.execute(select(SystemConfig).where(SystemConfig.key == "system_wallet"))
        system_wallet = config.scalar_one_or_none().value if config else None
        if not system_wallet:
            await message.answer("System wallet not set.")
            return

        valid = await verify_usdt_transfer(purchase.tx_hash, purchase.amount_usdt, system_wallet)
        if valid:
            purchase.status = "confirmed"
            result = await session.execute(select(User).where(User.telegram_id == purchase.telegram_id))
            user = result.scalar_one_or_none()
            if user:
                coins = purchase.amount_usdt // 100 * 100
                user.coins += coins
                if not user.is_kyc:
                    user.is_kyc = True
                    user.role = "verified"
            await session.commit()
            await message.answer(f"✅ Deposit #{purchase_id} confirmed!")
        else:
            await message.answer(f"❌ Verification failed for #{purchase_id}")

