from aiogram import Bot, Dispatcher
from src.core.settings import settings

dp = Dispatcher()
bot = None


async def run_bot():
    global bot

    if not settings.BOT_TOKEN:
        print("BOT OFF - missing token")
        return

    bot = Bot(token=settings.BOT_TOKEN)

    # ?? CRITICAL FIX: remove webhook before polling
    await bot.delete_webhook(drop_pending_updates=True)

    print("BOT STARTED")
    await dp.start_polling(bot)
