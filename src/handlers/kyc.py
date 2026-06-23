from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("kyc"))
async def kyc_info(message: types.Message):
    await message.answer(
        "🕵️ **KYC Verification**\n\n"
        "Send a clear photo of your ID/passport as a document.\n"
        "An admin will review and update your status.\n\n"
        "Use /kyc_status to check your status."
    )

@router.message(Command("kyc_status"))
async def kyc_status(message: types.Message):
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
            user = result.scalar_one_or_none()
            if user and user.is_kyc:
                await message.answer("✅ You are KYC verified.")
            else:
                await message.answer("❌ Not verified yet. Send your document.")
    except Exception as e:
        await message.answer(f"Error checking KYC: {e}")

@router.message(Command("kyc_approve"))
async def kyc_approve(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Usage: /kyc_approve <telegram_id>")
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
            user.is_kyc = True
            user.role = "verified"
            await session.commit()
            await message.answer(f"✅ User {tid} is now KYC verified.")
        else:
            await message.answer("User not found.")
