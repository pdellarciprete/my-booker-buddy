from freezegun import freeze_time
from datetime import datetime
from bot.utils import get_default_book_date, get_default_book_time_slot
import pytest
from zoneinfo import ZoneInfo

test_cases = [
    '2025-07-11 00:00:00',
    '2025-07-12 00:00:00',
    '2025-07-13 00:00:00',
]

answers = [
    '2025-07-21',
    '2025-07-22',
    '2025-07-23',
]

@pytest.mark.parametrize("test_case, answer", zip(test_cases, answers))
def test_get_default_book_date_no_freeze(test_case, answer):
    europe_tz = ZoneInfo('Europe/Warsaw')
    dt = datetime.strptime(test_case, "%Y-%m-%d %H:%M:%S").replace(tzinfo=europe_tz)
    utc_dt = dt.astimezone(ZoneInfo('UTC'))

    with freeze_time(utc_dt):
        assert get_default_book_date().strftime("%Y-%m-%d") == answer
        assert get_default_book_time_slot() == "18:00-19:30"
