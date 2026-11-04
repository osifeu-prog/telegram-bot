from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.bot.db.models import User


def utc_day(value: datetime):
    """Return a datetime's calendar date in UTC, treating naive values as UTC."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).date()


def next_streak(last_daily, today):
    """Calculate the streak after a successful claim."""
    if last_daily is not None and utc_day(last_daily).toordinal() == today.toordinal() - 1:
        return None  # caller increments the existing streak
    return 1


async def claim_daily_reward(session, telegram_id: int, now=None):
    """Atomically claim the shared daily reward for /daily and /daily_quest.

    PostgreSQL ON CONFLICT creates the user safely when two first-time claims
    race. SELECT FOR UPDATE serializes claims for an existing user row.
    Returns (claimed, coins, current_streak).
    """
    now = now or datetime.now(timezone.utc)
    today = utc_day(now)

    if session.bind.dialect.name == "postgresql":
        await session.execute(
            pg_insert(User)
            .values(
                telegram_id=telegram_id,
                coins=0,
                current_streak=0,
            )
            .on_conflict_do_nothing(index_elements=[User.telegram_id])
        )
    else:
        existing_user = await session.get(User, telegram_id)
        if existing_user is None:
            session.add(
                User(
                    telegram_id=telegram_id,
                    coins=0,
                    current_streak=0,
                )
            )
            await session.flush()

    result = await session.execute(
        select(User)
        .where(User.telegram_id == telegram_id)
        .with_for_update()
    )
    user = result.scalar_one()

    if user.last_daily is not None and utc_day(user.last_daily) == today:
        return False, user.coins, user.current_streak

    streak_reset = next_streak(user.last_daily, today)
    if streak_reset is None:
        user.current_streak += 1
    else:
        user.current_streak = streak_reset

    user.coins = (user.coins or 0) + 10
    user.last_daily = now
    await session.commit()
    return True, user.coins, user.current_streak
