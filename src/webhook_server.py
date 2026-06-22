import os
from dotenv import load_dotenv

load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request

from src.router_loader import setup_routers
from src.bot.db.fsm_storage import storage

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(storage=storage)
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
    mode = os.getenv("MODE", "DEV")

    print(f"MODE={mode}")

    if mode == "DEV":
        print("DEV MODE - webhook disabled")
        return

    webhook_url = os.getenv("WEBHOOK_URL")

    if not webhook_url:
        print("WEBHOOK_URL missing - skipping webhook")
        return

    await bot.set_webhook(webhook_url)

@app.on_event("startup")
async def startup_event():
    await on_startup()




