import uvicorn
import asyncio

from src.api.app import app
from src.core.bootstrap import bootstrap
from src.bot.runner import run_bot


@app.on_event("startup")
async def startup_event():
    await bootstrap()
    asyncio.create_task(run_bot())


if __name__ == "__main__":
    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=False
    )
