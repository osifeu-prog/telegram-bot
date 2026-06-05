import asyncio
import uvicorn

from src.core.bootstrap import bootstrap
from src.api.app import app
from src.bot.runner import run_bot


def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8080)


async def main():
    await bootstrap()
    asyncio.create_task(run_bot())
    run_api()


if __name__ == "__main__":
    asyncio.run(main())
