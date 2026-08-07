import os
import logging
import config.settings as settings
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.chrome.service import Service


def setup_logging() -> None:
    logging.basicConfig(
        level=settings.LOGGING_LEVEL,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/bot.log"),
            logging.StreamHandler(),
        ],
    )


def get_service() -> Service:
    if os.path.exists("/usr/bin/chromedriver"):
        return Service("/usr/bin/chromedriver")
    return Service()


def create_chrome_driver(env: str = "docker") -> webdriver.Chrome:
    """
    Create a chrome driver using Selenium and options

    Returns:
        Chrome driver
    """
    service = get_service()
    options = webdriver.ChromeOptions()

    if env == "docker":
        options.add_argument("--headless=new")  # comment for local
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def save_screenshot(driver: webdriver.Chrome, filename: str) -> None:
    screenshots_dir = settings.SCREENSHOT_DIR
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    filepath = os.path.join(screenshots_dir, filename)
    width = driver.execute_script("return document.body.scrollWidth")
    height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(width, height)
    driver.save_screenshot(filepath)
    logging.info("Screenshot saved: %s", filepath)


def get_default_book_date() -> datetime:
    return datetime.now(ZoneInfo("Europe/Madrid")) + timedelta(days=10)


def get_default_book_time_slot() -> str:
    return "18:00-19:30"


def select_best_court(
    driver: webdriver.Chrome,
    available_slots: list,
    court_type: str,
    courts: dict[str, str],
    indoor_courts: set[str],
) -> str | None:
    court_dict = get_courts_dict(available_slots)
    court_names = [courts[str(key)] for key in court_dict.keys() if str(key) in courts]
    logging.info("The courts available are: %s", ", ".join(court_names))

    available_keys = {str(key) for key in court_dict.keys()}
    has_indoor = bool(available_keys & indoor_courts)
    has_outdoor = bool(available_keys - indoor_courts)

    if court_type.lower() == "indoor" and not has_indoor:
        logging.info("No indoor courts available, falling back to any court.")
        court_type = "both"
    elif court_type.lower() == "outdoor" and not has_outdoor:
        logging.info("No outdoor courts available, falling back to any court.")
        court_type = "both"

    if court_type.lower() == "indoor":
        court_number = min(key for key in court_dict.keys() if str(key) in indoor_courts)
    elif court_type.lower() == "outdoor":
        court_number = min(key for key in court_dict.keys() if str(key) not in indoor_courts)
    else:
        court_number = min(court_dict.keys())

    try:
        logging.info("Trying to book the court %s ...", courts[str(court_number)])
        driver.execute_script(court_dict[court_number])
    except JavascriptException:
        logging.info("The court %s is not bookable!", courts[str(court_number)])
        return None
    return courts[str(court_number)]


def get_courts_dict(available_slots: list) -> dict[int, str]:
    court_dict: dict[int, str] = {}
    for slot in available_slots:
        ajax_call = slot.get_attribute("onclick")
        parts = ajax_call.split(",")
        court_number = int(parts[1].strip("'"))
        court_dict[court_number] = ajax_call
    return court_dict
