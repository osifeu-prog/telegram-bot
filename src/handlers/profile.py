from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()

@router.message(Command("profile"))
async def profile_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
    
    if not user:
        await message.answer("No profile yet. Use /start to begin!")
        return
    
    role_emoji = {"user": "👤", "verified": "✅", "admin": "🛡️", "founder": "👑"}
    role_name = {"user": "User", "verified": "Verified", "admin": "Admin", "founder": "Founder"}
    
    await message.answer(
        f"{role_emoji.get(user.role, '👤')} **Profile**\n\n"
        f"🆔 ID: `{user.telegram_id}`\n"
        f"🏷️ Role: {role_name.get(user.role, user.role)}\n"
        f"🕵️ KYC: {'✅ Verified' if user.is_kyc else '❌ Not Verified'}\n"
        f"💰 Coins: {user.coins}\n"
        f"🔥 Streak: {user.current_streak}\n"
        f"⚡ Boosts: {user.boosts_available}\n"
        f"💳 Wallet: `{user.wallet_address or 'Not set'}`\n"
        f"📅 Joined: {user.created_at.strftime('%Y-%m-%d') if user.created_at else 'N/A'}"
    )

@router.message(Command("prices"))
async def prices_cmd(message: types.Message):
    await message.answer(
        "💎 **Price List (USDT)**\n\n"
        "⚡ Streak Boost  1 USDT\n"
        "Protect your streak for 24h if you miss a day.\n\n"
        "🗳️ Extra Vote Power (x3)  5 USDT/month\n"
        "Multiply your voting weight in community decisions.\n\n"
        "💎 Premium  10 USDT/month\n"
        "• 2x daily rewards\n"
        "• 3x voting power\n"
        "• Exclusive achievements\n"
        "• Priority support\n\n"
        "💡 Use /deposit to learn how to fund your account."
    )

