import asyncio
import json
from aiogram import Bot, Dispatcher
from src.core.settings import settings
from src.queue.client import subscribe

dp = Dispatcher()


async def run_worker():
    if not settings.BOT_TOKEN:
        print("BOT OFF")
        return

    bot = Bot(token=settings.BOT_TOKEN)
    print("BOT WORKER STARTED")

    pubsub = await subscribe("events")

    if not pubsub:
        print("REDIS OFF - idle mode")
        while True:
            await asyncio.sleep(10)

    async for msg in pubsub.listen():
        if msg["type"] == "message":
            data = json.loads(msg["data"])
            await bot.send_message(
                chat_id=data["payload"]["chat_id"],
                text=data["payload"]["text"]
            )
