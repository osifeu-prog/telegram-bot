import os
from typing import Optional

class ServiceHealth:
    @staticmethod
    async def check_all(bot, admin_id: int):
        """Check all services and notify admin if any are down."""
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
        from src.bot.db.database import engine
        from sqlalchemy import text
        try:
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
        
        if issues and admin_id:
            try:
                await bot.send_message(
                    admin_id,
                    "🔍 **Health Check Alert**\n\n" + "\n".join(issues)
                )
            except:
                pass
        
        return issues
