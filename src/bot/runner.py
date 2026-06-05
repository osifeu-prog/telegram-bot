from aiogram import Bot, Dispatcher
from src.core.settings import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

async def run_bot():
    if not settings.BOT_TOKEN:
        print("BOT OFF")
        return

    print("BOT STARTED")
    await dp.start_polling(bot)
