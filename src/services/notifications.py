import asyncio
import logging
from datetime import datetime, time, timezone

from aiogram import Router
from sqlalchemy import or_, select

from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User
from src.bot.bot import bot

router = Router()
logger = logging.getLogger(__name__)


async def send_daily_reminders():
    """Send reminders only to opted-in users who have not claimed today.

    The first run is 24 hours after process startup, matching the existing
    cadence. Delivery failures are logged without exposing Telegram user IDs.
    """
    while True:
        await asyncio.sleep(86400)
        try:
            now = datetime.now(timezone.utc)
            day_start = datetime.combine(now.date(), time.min, tzinfo=timezone.utc)

            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(User.telegram_id).where(
                        User.notifications_enabled.is_(True),
                        or_(
                            User.last_daily.is_(None),
                            User.last_daily < day_start,
                        ),
                    )
                )
                telegram_ids = result.scalars().all()

            sent = 0
            failed = 0
            for telegram_id in telegram_ids:
                try:
                    await bot.send_message(
                        telegram_id,
                        "⏰ Don't forget to claim your daily reward! Use /daily",
                    )
                    sent += 1
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    failed += 1
                    logger.warning(
                        "Daily reminder delivery failed (%s)",
                        type(exc).__name__,
                    )

            logger.info(
                "Daily reminder cycle completed: eligible=%d sent=%d failed=%d",
                len(telegram_ids),
                sent,
                failed,
            )
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("Daily reminder cycle failed")
