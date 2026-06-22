from aiogram import Router
from src.bot.handlers import buttons_demo, fsm_demo

def setup_routers(dp):
    router = Router()
    router.include_router(buttons_demo.router)
    router.include_router(fsm_demo.router)
    dp.include_router(router)




