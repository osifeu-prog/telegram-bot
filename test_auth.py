import json
import redis
import os
from dotenv import load_dotenv

load_dotenv('D:/0/0.1/slh-telegram-bot/.env')
# בדיקת חיבור ל-Redis המוגדר ב-ENV
r = redis.from_url(os.getenv('REDIS_URL'))
try:
    test_data = {"user_id": 1, "session": "test_token"}
    r.set("test_key", json.dumps(test_data))
    val = json.loads(r.get("test_key"))
    print(f"Auth Integrity Check: PASSED. Data: {val}")
except Exception as e:
    print(f"Auth Integrity Check: FAILED. Error: {e}")
