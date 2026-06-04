from aiogram import Router
from src.bot.handlers import buttons_demo

def setup_routers(dp):
    dp.include_router(buttons_demo.router)
from src.bot.handlers import fsm_demo
dp.include_router(fsm_demo.router)
