from aiogram import Router, F
from aiogram.types import PreCheckoutQuery, Message
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User

router = Router()

@router.pre_checkout_query()
async def process_pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    telegram_id = message.from_user.id
    payload = message.successful_payment.invoice_payload
    if payload == "boost_purchase":
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalar_one_or_none()
            if user:
                user.boosts_available += 1
                await session.commit()
        await message.answer("✅ Boost purchased! Your streak is protected.")
