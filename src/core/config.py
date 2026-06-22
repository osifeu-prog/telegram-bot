import os
from dotenv import load_dotenv
load_dotenv(override=True)

class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0"))
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise RuntimeError("BOT_TOKEN missing")
        if not cls.DATABASE_URL:
            raise RuntimeError("DATABASE_URL missing")

config = Config()
config.validate()



