import os
import logging
import time
import config.settings as settings
import bot.utils as utils
from dotenv import load_dotenv
from datetime import datetime
from bot.login import login_to_site
from bot.booking import book_court

def setup_logging():
    """
    Sets up logging configuration to log all events at DEBUG level.
    """
    logging.basicConfig(
        level=settings.LOGGING_LEVEL,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/bot.log"),  # Logs to a file
            logging.StreamHandler()  # Logs to the console
        ]
    )

def main():
    """
    Main function to orchestrate the bot workflow.
    """
    # Initialize logging
    setup_logging()

    # Set the TZ environment variable for Europe/Madrid timezone
    os.environ['TZ'] = 'Europe/Madrid'
    # If the operating system supports, apply the timezone
    if hasattr(time, 'tzset'):
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

    if not username or not password:
        print("Error: Username or password not found in environment variables.")
        return

    # Perform login and booking
    try:
        logging.debug("Attempting to log in to the site.")
        driver = login_to_site(username, password)
        logging.info("Login successful with the username : %s", username)

        # Placeholder for booking functionality
        court_preferences = {
            "date": "2025-01-26",
            "time": "18:00",
            "court_type": "indoor"
        }

        logging.debug("Attempting to book a court with preferences: %s", court_preferences)
        book_court(driver, court_preferences)
        logging.info("Court booked successfully!")

    except Exception as e:
        logging.exception("An error occurred: %s", e)

    finally:
        # Close the WebDriver instance
        if 'driver' in locals():
            logging.debug("Taking a final screenshot before closing the WebDriver.")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            utils.save_screenshot(driver, f"final_state_{timestamp}.png")
            logging.debug("Closing the WebDriver instance.")
            driver.quit()

if __name__ == "__main__":
    main()
