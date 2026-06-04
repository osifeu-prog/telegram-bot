from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="מידע", callback_data="info")],
        [InlineKeyboardButton(text="הגדרות", callback_data="settings")],
        [InlineKeyboardButton(text="עזרה", callback_data="help")],
    ]
)
