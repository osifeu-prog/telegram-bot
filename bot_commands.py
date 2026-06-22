from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import subprocess, asyncio, os, sys, platform
from dotenv import load_dotenv

# Force SelectorEventLoop on Windows
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv(override=True)
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ... (שאר הקוד נשאר זהה) ...
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass



