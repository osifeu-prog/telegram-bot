from aiogram import Router, types
from aiogram.filters import Command

from src.bot.keyboards.reply_keyboard import main_menu
from src.bot.keyboards.inline_keyboard import inline_menu

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "הבוט עובד! הנה התפריט שלך:",
        reply_markup=main_menu
    )
    await message.answer(
        "או שתבחר מהתפריט המתקדם:",
        reply_markup=inline_menu
    )




