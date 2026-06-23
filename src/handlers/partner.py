from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("partner_register"))
async def test_partner(message: types.Message):
    await message.answer("✅ partner_router is active! The command works. DB column check next.")
