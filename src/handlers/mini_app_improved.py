from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command

router = Router()

@router.message(Command("app"))
async def open_app(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Open Dashboard", web_app=WebAppInfo(url="https://telegrambot-production-a4c0.up.railway.app/static/index.html"))],
        [InlineKeyboardButton(text="🛒 Shop", callback_data="menu_shop"),
         InlineKeyboardButton(text="👥 Referral", callback_data="menu_ref")],
    ])
    await message.answer("🚀 **SLH App**", reply_markup=keyboard)

