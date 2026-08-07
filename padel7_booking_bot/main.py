import os
import logging
import time
import config.settings as settings
import bot.utils as utils
import bot.notifications as notifications
import argparse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bot.login import login_to_site
from bot.booking import book_court
from bot.types import CourtPreferences

_BOT_TZ = ZoneInfo("Europe/Madrid")


def wait_until_time(target_time_str: str) -> None:
    target_time = datetime.strptime(target_time_str, "%H:%M:%S").time()
    now = datetime.now(_BOT_TZ)
    target_dt = datetime.combine(now.date(), target_time, tzinfo=_BOT_TZ)
    if target_dt <= now:
        target_dt += timedelta(days=1)

    remaining = (target_dt - now).total_seconds()
    logging.info("Waiting until %s (%.0fs)", target_dt.strftime("%Y-%m-%d %H:%M:%S %Z"), remaining)

    while True:
        remaining = (target_dt - datetime.now(_BOT_TZ)).total_seconds()
        if remaining <= 0:
            break
        interval = min(10 if remaining > 60 else 1, remaining)
        logging.info("Starting in %.0fs...", remaining)
        time.sleep(interval)

    logging.info("Target time reached, proceeding.")


def main(court_preferences: CourtPreferences, env: settings.AppSettings) -> None:
    utils.setup_logging()
    logging.debug("Starting the Padel7 booking bot.")

    os.environ["TZ"] = "Europe/Madrid"
    if hasattr(time, "tzset"):
        time.tzset()

    logging.debug("Attempting to log in to the site.")
    driver = login_to_site(env.app_username, env.app_password, env.env)
    logging.info("Login successful with the username: %s", env.app_username)

    logging.debug("Attempting to book a court with preferences: %s", court_preferences)
    booking_details, booking_successful = book_court(driver, court_preferences)
    if booking_successful:
        logging.info("Court booked successfully!")
    else:
        logging.error("Court booking failed.")
        logging.debug("Booking details: %s", booking_details)

    if "driver" in locals():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        utils.save_screenshot(driver, f"final_state_{timestamp}.png")
        driver.quit()

    if settings.NOTIFICATION_ENABLED:
        webhook_url = env.app_slack_test_webhook_url if settings.DRY_RUN else env.app_slack_prod_webhook_url
        notifications.send_booking_notification(
            webhook_url,
            env.app_slack_token,
            booking_details,
            booking_successful,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Padel7 Booking Bot")
    parser.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        help="Simulate the booking without spending money (default: on). Use --no-dry-run for a real booking.",
        default=True,
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
        default=False,
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date for booking in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--time",
        type=str,
        help="Time for booking in HH:MM format.",
    )
    parser.add_argument(
        "--court-type",
        type=str,
        choices=["indoor", "outdoor", "both"],
        help="Type of court to book (indoor or outdoor).",
        default="both",
    )
    parser.add_argument(
        "--notifications",
        action="store_true",
        help="Enable Slack notifications.",
        default=settings.NOTIFICATION_ENABLED,
    )
    parser.add_argument(
        "--centre",
        type=str,
        choices=list(settings.VENUES.keys()),
        help="Padel7 centre to book (default: poblenou).",
        default="poblenou",
    )
    parser.add_argument(
        "--wait-until",
        type=str,
        metavar="HH:MM:SS",
        help="Wait until this exact time (Europe/Madrid) before running, e.g. 00:00:00.",
    )

    args = parser.parse_args()

    settings.DRY_RUN = args.dry_run
    if args.verbose:
        settings.LOGGING_LEVEL = "DEBUG"
    if args.notifications:
        settings.NOTIFICATION_ENABLED = True

    if args.wait_until:
        utils.setup_logging()
        wait_until_time(args.wait_until)

    env = settings.AppSettings()
    court_preferences: CourtPreferences = {
        "date": args.date,
        "time": args.time,
        "court_type": args.court_type,
        "venue_config": settings.VENUES[args.centre],
        "booked_by": env.app_username.split("@")[0],
    }

    main(court_preferences, env)
