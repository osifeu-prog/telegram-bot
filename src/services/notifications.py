import asyncio
import logging
from datetime import datetime, timezone

from aiogram import Router
from sqlalchemy import or_, select

from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User
from src.bot.bot import bot

router = Router()
logger = logging.getLogger(__name__)

REMINDER_INTERVAL_SECONDS = 86400


def utc_day_start(now=None):
    """Return the start of the current UTC day as a timezone-aware datetime."""
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    else:
        current = current.astimezone(timezone.utc)
    return current.replace(hour=0, minute=0, second=0, microsecond=0)


async def get_daily_reminder_users(session, now=None):
    """Return opted-in users who have not claimed the daily reward today (UTC)."""
    cutoff = utc_day_start(now)
    result = await session.execute(
        select(User).where(
            User.notifications_enabled.is_(True),
            or_(User.last_daily.is_(None), User.last_daily < cutoff),
        )
    )
    return result.scalars().all()


async def send_daily_reminders():
    """Send daily reminders only to opted-in users who have not claimed today."""
    while True:
        await asyncio.sleep(REMINDER_INTERVAL_SECONDS)
        try:
            async with AsyncSessionLocal() as session:
                users = await get_daily_reminder_users(session)
                delivered = 0
                failed = 0
                for user in users:
                    try:
                        await bot.send_message(
                            user.telegram_id,
                            "⏰ Don't forget to claim your daily reward! Use /daily",
                        )
                        delivered += 1
                    except Exception:
                        failed += 1
                        logger.exception("Daily reminder delivery failed")
                logger.info(
                    "Daily reminder cycle completed: eligible=%d delivered=%d failed=%d",
                    len(users),
                    delivered,
                    failed,
                )
        except Exception:
            logger.exception("Daily reminder cycle failed")
