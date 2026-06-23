import os
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from src.router_loader import setup_routers
from src.bot.db.fsm_storage import storage
from src.bot.db.database import engine
from src.bot.db.models import Base
from src.bot.handlers.admin_ops import router as admin_ops_router
from src.handlers.daily import router as daily_router
from src.handlers.payments import router as payments_router
from src.api.mini_app import router as mini_app_router
from src.bot.bot import bot

dp = Dispatcher(storage=storage)
setup_routers(dp)
dp.include_router(admin_ops_router)
dp.include_router(payments_router)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(mini_app_router)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "running"}

@app.on_event("startup")
async def startup_event():
    # Ensure users table columns exist
    from sqlalchemy import text
    async with engine.begin() as conn:
        for col_name, col_def in [
            ("coins", "INTEGER DEFAULT 0"),
            ("current_streak", "INTEGER DEFAULT 0"),
            ("last_daily", "TIMESTAMP WITH TIME ZONE"),
            ("boosts_available", "INTEGER DEFAULT 0"),
        ]:
            await conn.execute(text(
                f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col_name} {col_def}"
            ))
    # Create any missing tables (like purchases)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Set webhook in production
    mode = os.getenv("MODE", "DEV")
    if mode != "DEV":
        webhook_url = os.getenv("WEBHOOK_URL")
        if webhook_url:
            await bot.set_webhook(webhook_url)

