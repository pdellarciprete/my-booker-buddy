import os
import logging
import time
import config.settings as settings
import bot.utils as utils
import bot.notifications as notifications
import argparse
from dotenv import load_dotenv
from datetime import datetime
from bot.login import login_to_site
from bot.booking import book_court
import selenium.common.exceptions


def main(court_preferences):
    """
    Main function to orchestrate the bot workflow.
    """
    # Initialize logging
    utils.setup_logging()
    logging.debug("Starting the Padel7 booking bot.")
    logging.debug("Current logging level: %s", settings.LOGGING_LEVEL)

    # Set the TZ environment variable for Europe/Madrid timezone
    os.environ["TZ"] = "Europe/Madrid"
    # If the operating system supports, apply the timezone
    if hasattr(time, "tzset"):
        time.tzset()

    # Load environment variables from .env file
    logging.debug("Loading environment variables from .env file.")
    load_dotenv()

    # Retrieve credentials from environment variables
    username = os.getenv("APP_USERNAME")
    password = os.getenv("APP_PASSWORD")

    if not username or not password:
        logging.error("Username or password not found in environment variables.")
        return

    # Perform login and booking

    logging.debug("Attempting to log in to the site.")
    driver = login_to_site(username, password)
    logging.info("Login successful with the username : %s", username)

    logging.debug(
            "Attempting to book a court with preferences: %s", court_preferences
        )
    booking_details, booking_succesful = book_court(driver, court_preferences)
    if booking_succesful is True:
        logging.info("Court booked successfully!")
    else:
        logging.error("Court booking failed.")
        logging.debug("Booking details: %s", booking_details)
    if "driver" in locals():
        logging.debug("Taking a final screenshot before closing the WebDriver.")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        utils.save_screenshot(driver, f"final_state_{timestamp}.png")
        logging.debug("Closing the WebDriver instance.")
        driver.quit()

    # Send notification
    if settings.NOTIFICATION_ENABLED:
        webhook_url = (
            os.getenv("APP_SLACK_TEST_WEBHOOK_URL")
            if settings.DRY_RUN
            else os.getenv("APP_SLACK_PROD_WEBHOOK_URL")
        )
        notifications.send_booking_notification(
            webhook_url,
            os.getenv("APP_SLACK_TOKEN"),
            booking_details,
            booking_succesful,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Padel7 Booking Bot")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the bot in dry run mode without making actual bookings.",
        default=False,
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
        help="Date for booking in YYYY-MM-DD format."
    )
    parser.add_argument(
        "--time",
        type=str,
        help="Time for booking in HH:MM format."
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

    args = parser.parse_args()
    if args.dry_run:
        settings.DRY_RUN = True
    if args.verbose:
        settings.LOGGING_LEVEL = "DEBUG"
    if args.notifications:
        settings.NOTIFICATION_ENABLED = True
    court_preferences = {
        "date": args.date,
        "time": args.time,
        "court_type": args.court_type,
    }

    main(court_preferences)
