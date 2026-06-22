import asyncio
import os
from dotenv import load_dotenv

load_dotenv(override=True)

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from src.router_loader import setup_routers

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # נוסיף אותו ל-.env

if not BOT_TOKEN:
    raise RuntimeError("Missing BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
setup_routers(dp)

async def main():
    print("SLH BOT RUNNING (CLEAN MODE)")
    if False and ADMIN_ID:
        try:
            await bot.send_message(
                chat_id=int(ADMIN_ID),
                text=(
                    "✅ *SLH Bot Started*\n"
                    "─────────────────\n"
                    f"🕐 {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    "📡 Mode: Polling\n"
                    "🗄 DB: SQLite\n"
                    "─────────────────\n"
                    "Bot is online and ready."
                ),
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"[WARN] Could not send startup message: {e}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



