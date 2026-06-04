import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request

from src.router_loader import setup_routers

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
setup_routers(dp)

app = FastAPI()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "running"}

async def on_startup():
    webhook_url = os.getenv("WEBHOOK_URL")
    await bot.set_webhook(webhook_url)

asyncio.get_event_loop().create_task(on_startup())
