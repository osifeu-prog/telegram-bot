from fastapi import FastAPI
import uvicorn
import asyncio

from src.api.app import app
from src.core.bootstrap import bootstrap
from src.bot.runner import run_bot


def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")


async def start_background():
    await bootstrap()
    asyncio.create_task(run_bot())


if __name__ == "__main__":
    # ? NO asyncio.run
    loop = asyncio.get_event_loop()
    loop.create_task(start_background())
    run_api()
