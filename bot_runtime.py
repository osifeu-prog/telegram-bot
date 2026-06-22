import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError, TelegramUnauthorizedError
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN missing")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def run():
    retry = 0
    while True:
        try:
            logging.info("BOT STARTED")
            await dp.start_polling(bot)

        except TelegramUnauthorizedError:
            logging.error("INVALID TOKEN - STOPPING")
            break

        except TelegramNetworkError as e:
            retry += 1
            wait = min(60, 2 ** retry)
            logging.warning(f"NETWORK ERROR: {e} retry in {wait}s")
            await asyncio.sleep(wait)

        except Exception as e:
            retry += 1
            wait = min(60, 2 ** retry)
            logging.exception(e)
            await asyncio.sleep(wait)

asyncio.run(run())
