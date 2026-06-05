import os

print("BOT_TOKEN =", "SET" if os.getenv("BOT_TOKEN") else "MISSING")
print("DATABASE_URL =", "SET" if os.getenv("DATABASE_URL") else "MISSING")
print("REDIS_URL =", "SET" if os.getenv("REDIS_URL") else "MISSING")
