import os

class ServiceHealth:
    @staticmethod
    async def check_all(bot, admin_id: int):
        try:
            issues = []

            # Check Telegram token
            try:
                me = await bot.get_me()
            except Exception as e:
                issues.append(f"❌ Telegram Bot: {e}")

            # Check Groq API
            groq_key = os.getenv("GROQ_API_KEY")
            if not groq_key:
                issues.append("⚠️ Groq API Key not set")

            # Check Database
            try:
                from src.bot.db.database import engine
                from sqlalchemy import text
                async with engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
            except Exception as e:
                issues.append(f"❌ Database: {e}")

            # Check Redis
            try:
                from src.bot.db.fsm_storage import redis_client
                await redis_client.ping()
            except Exception as e:
                issues.append(f"⚠️ Redis: {e}")

            # Notify admin
            if issues and admin_id:
                try:
                    await bot.send_message(
                        admin_id,
                        "🔍 **Health Check Alert**\n\n" + "\n".join(issues)
                    )
                except:
                    pass

            return issues
        except Exception as e:
            print(f"Health check failed: {e}")
            return []
