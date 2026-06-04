from aiogram import Router, types
from aiogram.filters import Command

from src.bot.keyboards.reply_keyboard import main_menu

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "הבוט עובד! הנה התפריט שלך:",
        reply_markup=main_menu
    )
@router.message(lambda m: m.text == "מידע")
async def info_handler(message: types.Message):
    await message.answer("זהו מסך המידע.")

@router.message(lambda m: m.text == "הגדרות")
async def settings_handler(message: types.Message):
    await message.answer("כאן יהיו הגדרות.")

@router.message(lambda m: m.text == "עזרה")
async def help_handler(message: types.Message):
    await message.answer("כאן תהיה עזרה.")
