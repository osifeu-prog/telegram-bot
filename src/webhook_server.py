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
from src.handlers.broadcast import router as broadcast_router
from src.handlers.groups import router as groups_router
from src.handlers.contacts import router as contacts_router
from src.handlers.test_i18n import router as test_i18n_router
from src.handlers.pdf_analyzer import router as pdf_analyzer_router
from src.handlers.kyc import router as kyc_router
from src.handlers.ton_testnet import router as ton_testnet_router
from src.handlers.referral import router as referral_router
from src.handlers.teaser import router as teaser_router, start_scheduler
from src.handlers.help import router as help_router
from src.handlers.recalc_progress import router as recalc_progress_router
from src.handlers.achievements import router as achievements_router
from src.handlers.settings_notifications import router as settings_router
from src.handlers.mini_app_improved import router as mini_app_improved_router
from src.api.mini_app import router as mini_app_router
from src.bot.bot import bot
from src.services.notifications import send_daily_reminders
from src.services.health_monitor import ServiceHealth

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
dp.include_router(broadcast_router)
dp.include_router(groups_router)
dp.include_router(contacts_router)
dp.include_router(test_i18n_router)
dp.include_router(pdf_analyzer_router)
dp.include_router(kyc_router)
dp.include_router(ton_testnet_router)
dp.include_router(referral_router)
dp.include_router(teaser_router)
dp.include_router(help_router)
dp.include_router(recalc_progress_router)
dp.include_router(achievements_router)
dp.include_router(settings_router)
dp.include_router(mini_app_improved_router)

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
            ("referrer_id", "BIGINT"),
            ("language", "VARCHAR(5) DEFAULT 'en'"),
            ("achievements", "TEXT"),
            ("notifications_enabled", "BOOLEAN DEFAULT TRUE"),
        ]:
            await conn.execute(text(
                f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col_name} {col_def}"
            ))
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(bind=sync_conn, tables=[Vote.__table__]))
        result = await conn.execute(text(
            "SELECT value FROM system_config WHERE key='system_wallet'"
        ))
        if not result.fetchone():
            await conn.execute(text(
                "INSERT INTO system_config (key, value) VALUES ('system_wallet', 'UQCd7XHWGj06cBLlWW_DZUN3TWMGr_oWoVy0G0LkC14gQklj')"
            ))
    import asyncio as _asyncio
    _asyncio.create_task(send_daily_reminders())
    _asyncio.create_task(ServiceHealth.check_all(bot, int(os.getenv('ADMIN_ID', '0'))))
    mode = os.getenv("MODE", "DEV")
    if mode != "DEV":
        webhook_url = os.getenv("WEBHOOK_URL")
        if webhook_url:
            current = await bot.get_webhook_info()
            if current.url != webhook_url:
                await bot.set_webhook(webhook_url)
    start_scheduler(bot)


