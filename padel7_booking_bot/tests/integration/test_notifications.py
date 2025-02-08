import pytest
from bot.notifications import send_booking_notification
import os
from config import settings
from dotenv import load_dotenv

@pytest.fixture(scope='module')
def setup_environment():
    # Set up any necessary state needed for integration tests
    load_dotenv()


def test_send_slack_notification(setup_environment):

    webhook_url = settings.SLACK_TEST_WEBHOOK_URL
    token = os.getenv("APP_SLACK_TOKEN")
    booking_details = {
        "date": "February 18th, 2025",
        "time": "6:00 PM - 7:30 PM",
        "court": "Indoor 1",
        "location": "Padel7 Glories, Barcelona",
        "cost": "€48"
    }
    result = send_booking_notification(webhook_url, token, booking_details)
    assert result == None
