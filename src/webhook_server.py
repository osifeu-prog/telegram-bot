import os, asyncio
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from src.router_loader import setup_routers
from src.bot.db.fsm_storage import storage
from src.bot.db.database import engine
from src.bot.db.models import Base, SystemConfig
from src.bot.handlers.admin_ops import router as admin_ops_router
from src.handlers.daily import router as daily_router
from src.handlers.payments import router as payments_router
from src.handlers.user_commands import router as user_commands_router
from src.handlers.shop import router as shop_router
from src.handlers.admin_users import router as admin_users_router
from src.handlers.admin_economy import router as admin_economy_router
from src.handlers.devops import router as devops_router
from src.handlers.governance import router as governance_router
from src.handlers.wallet import router as wallet_router
from src.handlers.deposits import router as deposits_router
from src.handlers.profile import router as profile_router
from src.handlers.demo import router as demo_router
from src.handlers.language import router as language_router
from src.handlers.menu_system import router as menu_system_router
from src.handlers.ops_commands import router as ops_commands_router
from src.api.mini_app import router as mini_app_router
from src.bot.bot import bot
from src.services.notifications import send_daily_reminders

dp = Dispatcher(storage=storage)
setup_routers(dp)
dp.include_router(admin_ops_router)
dp.include_router(payments_router)
dp.include_router(user_commands_router)
dp.include_router(shop_router)
dp.include_router(admin_users_router)
dp.include_router(admin_economy_router)
dp.include_router(devops_router)
dp.include_router(governance_router)
dp.include_router(wallet_router)
dp.include_router(deposits_router)
dp.include_router(profile_router)
dp.include_router(demo_router)
dp.include_router(language_router)
dp.include_router(menu_system_router)
dp.include_router(ops_commands_router)

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
    from sqlalchemy import text
    async with engine.begin() as conn:
        for col_name, col_def in [
            ("coins", "INTEGER DEFAULT 0"),
            ("current_streak", "INTEGER DEFAULT 0"),
            ("last_daily", "TIMESTAMP WITH TIME ZONE"),
            ("boosts_available", "INTEGER DEFAULT 0"),
            ("created_at", "TIMESTAMP WITH TIME ZONE DEFAULT now()"),
            ("wallet_address", "VARCHAR(100)"),
            ("role", "VARCHAR(20) DEFAULT 'user'"),
            ("is_kyc", "BOOLEAN DEFAULT FALSE"),
        ]:
            await conn.execute(text(
                f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col_name} {col_def}"
            ))
        await conn.run_sync(Base.metadata.create_all, tables=[SystemConfig.__table__])
        result = await conn.execute(text(
            "SELECT value FROM system_config WHERE key='system_wallet'"
        ))
        if not result.fetchone():
            await conn.execute(text(
                "INSERT INTO system_config (key, value) VALUES ('system_wallet', 'UQCd7XHWGj06cBLlWW_DZUN3TWMGr_oWoVy0G0LkC14gQklj')"
            ))
    asyncio.create_task(send_daily_reminders())
    mode = os.getenv("MODE", "DEV")
    if mode != "DEV":
        webhook_url = os.getenv("WEBHOOK_URL")
        if webhook_url:
            await bot.set_webhook(webhook_url)







