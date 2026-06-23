from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select, func
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("economy_status"))
async def economy_status_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    async with AsyncSessionLocal() as session:
        total_users = (await session.execute(select(func.count(User.telegram_id)))).scalar()
        total_coins = (await session.execute(select(func.coalesce(func.sum(User.coins), 0)))).scalar()
        avg_coins = total_coins // total_users if total_users > 0 else 0
    await message.answer(
        "💰 **Economy Status**\n"
        f"👥 Total users: {total_users}\n"
        f"🪙 Total coins: {total_coins}\n"
        f"📊 Avg coins: {avg_coins}"
    )

@router.message(Command("reward_add"))
async def reward_add_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Usage: /reward_add <telegram_id> <amount>")
        return
    try:
        tid = int(parts[1])
        amount = int(parts[2])
    except ValueError:
        await message.answer("Invalid arguments.")
        return
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == tid))
        user = result.scalar_one_or_none()
        if user:
            user.coins += amount
            await session.commit()
            await message.answer(f"✅ Added {amount} coins to {tid}. New balance: {user.coins}")
        else:
            await message.answer("User not found.")

@router.message(Command("token_mint"))
async def token_mint_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Usage: /token_mint <amount_per_user>")
        return
    try:
        amount = int(parts[1])
    except ValueError:
        await message.answer("Invalid amount.")
        return
    async with AsyncSessionLocal() as session:
        users = (await session.execute(select(User))).scalars().all()
        for user in users:
            user.coins += amount
        await session.commit()
        await message.answer(f"✅ Minted {amount} coins to {len(users)} users.")

