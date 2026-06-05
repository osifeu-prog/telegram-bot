from src.core.settings import settings

print("BOT =", bool(settings.BOT_TOKEN))
print("DB  =", bool(settings.DATABASE_URL))
print("REDIS =", bool(settings.REDIS_URL))
