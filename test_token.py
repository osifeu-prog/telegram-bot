import os, asyncio, aiohttp
from dotenv import load_dotenv
load_dotenv(override=True)
async def test():
    async with aiohttp.ClientSession() as s:
        async with s.get(f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/getMe") as resp:
            print(await resp.json())
asyncio.run(test())



