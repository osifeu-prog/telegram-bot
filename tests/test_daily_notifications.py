import os
import unittest
from datetime import datetime, timezone, timedelta

os.environ.setdefault("BOT_TOKEN", "123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi")

from src.services.notifications import get_daily_reminder_users, utc_day_start


class _Scalars:
    def __init__(self, values):
        self._values = values

    def all(self):
        return self._values


class _Result:
    def __init__(self, values):
        self._values = values

    def scalars(self):
        return _Scalars(self._values)


class _Session:
    def __init__(self, values=None):
        self.values = values or []
        self.statement = None

    async def execute(self, statement):
        self.statement = statement
        return _Result(self.values)


class DailyReminderPolicyTests(unittest.TestCase):
    def test_utc_day_start_normalizes_offset_aware_datetime(self):
        local_time = datetime(
            2026, 11, 4, 1, 30,
            tzinfo=timezone(timedelta(hours=2)),
        )
        self.assertEqual(
            utc_day_start(local_time),
            datetime(2026, 11, 3, 0, 0, tzinfo=timezone.utc),
        )

    def test_utc_day_start_treats_naive_datetime_as_utc(self):
        self.assertEqual(
            utc_day_start(datetime(2026, 11, 4, 12, 0)),
            datetime(2026, 11, 4, 0, 0, tzinfo=timezone.utc),
        )


class DailyReminderQueryTests(unittest.IsolatedAsyncioTestCase):
    async def test_query_requires_opt_in_and_no_claim_today(self):
        session = _Session()
        await get_daily_reminder_users(
            session,
            now=datetime(2026, 11, 4, 12, 0, tzinfo=timezone.utc),
        )

        sql = str(session.statement.compile(compile_kwargs={"literal_binds": True}))
        self.assertIn("notifications_enabled IS true", sql)
        self.assertIn("last_daily IS NULL", sql)
        self.assertIn("last_daily <", sql)


if __name__ == "__main__":
    unittest.main()
