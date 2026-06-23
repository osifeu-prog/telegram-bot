import asyncio

from src.webhook_server import bot, dp

async def main():
    print("SLH INVESTOR BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



