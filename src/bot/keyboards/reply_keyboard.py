from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="מידע")],
        [KeyboardButton(text="הגדרות")],
        [KeyboardButton(text="עזרה")],
    ],
    resize_keyboard=True
)
