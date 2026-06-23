from dotenv import load_dotenv
import os

load_dotenv(override=True)

print("BOT_TOKEN =", repr(os.getenv("BOT_TOKEN")))
print("PWD =", os.getcwd())
