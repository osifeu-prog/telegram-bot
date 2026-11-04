import unittest
from datetime import datetime, timezone, timedelta

from src.services.daily_rewards import next_streak, utc_day


class DailyRewardDateTests(unittest.TestCase):
    def test_utc_day_normalizes_offset_aware_datetime(self):
        local_time = datetime(
            2026, 11, 4, 1, 30,
            tzinfo=timezone(timedelta(hours=2)),
        )
        self.assertEqual(utc_day(local_time), datetime(2026, 11, 3).date())

    def test_utc_day_treats_naive_datetime_as_utc(self):
        self.assertEqual(
            utc_day(datetime(2026, 11, 4, 12, 0)),
            datetime(2026, 11, 4).date(),
        )

    def test_streak_increments_after_previous_utc_day(self):
        yesterday = datetime(2026, 11, 3, 23, 30, tzinfo=timezone.utc)
        today = datetime(2026, 11, 4).date()
        self.assertIsNone(next_streak(yesterday, today))

    def test_streak_resets_after_a_gap(self):
        two_days_ago = datetime(2026, 11, 2, 23, 30, tzinfo=timezone.utc)
        today = datetime(2026, 11, 4).date()
        self.assertEqual(next_streak(two_days_ago, today), 1)

    def test_first_claim_starts_streak_at_one(self):
        today = datetime(2026, 11, 4).date()
        self.assertEqual(next_streak(None, today), 1)


if __name__ == "__main__":
    unittest.main()
