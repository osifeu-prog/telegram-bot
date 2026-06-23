from aiogram import Router, types
from aiogram.filters import Command
from src.utils.i18n import get_string

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

LANGUAGES = ["en", "he", "ru", "ar", "es", "fr"]
TEST_KEYS = ["welcome", "daily_reward", "shop", "profile", "access_denied"]

@router.message(Command("test_i18n"))
async def test_i18n(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    results = []
    for lang in LANGUAGES:
        lang_results = []
        for key in TEST_KEYS:
            value = get_string(key, lang)
            ok = value != key and len(value) > 0
            lang_results.append("✅" if ok else "❌")
        all_ok = all(r == "✅" for r in lang_results)
        results.append(f"{'✅' if all_ok else '⚠️'} **{lang}**: {' '.join(lang_results)}")
    await message.answer("🌍 **i18n Test Results**\n\n" + "\n".join(results))
