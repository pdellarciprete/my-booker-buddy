import os
import logging
import config.settings as settings

from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.chrome.service import Service


def get_service() -> Service:
    """
    Get the service for the Chrome driver

    Returns:
        Service
    """
    if (os.path.exists('/usr/bin/chromedriver')):
        return Service('/usr/bin/chromedriver')
    else:
        return Service()

def create_chrome_driver() -> webdriver.Chrome:
    """
    Create a chrome driver using Selenium and options

    Returns:
        Chrome driver
    """
    service = get_service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def save_screenshot(driver, filename):
    """
    Takes a screenshot of the current page and saves it to the screenshots directory.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        filename (str): The name of the file to save the screenshot as.
    """
    screenshots_dir = settings.SCREENSHOT_DIR
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    filepath = os.path.join(screenshots_dir, filename)
    driver.save_screenshot(filepath)
    logging.info("Screenshot saved: %s", filepath)

def get_default_book_date():
    # Calculate the date 10 days from today
    return datetime.now() + timedelta(days=10)

def get_default_book_time_slot():
    # Calculate the date 10 days from today
    return "18:00-19:30"

def select_best_court(driver, available_slots):
    court_dict = get_courts_dict(available_slots)
    logging.info("The courts available are: %s", court_dict.keys())
    court_number = min(court_dict.keys()) # precedence to INDOOR COURTS
    try:
        logging.info("Trying to book the court number %s ... ", court_number)
        driver.execute_script(court_dict[court_number])
    except JavascriptException as e:
        logging.info("The court number %s is not bookable! :( ", court_number)
        return False
    return True

def get_courts_dict(available_slots):
    court_dict = {}

    # Iterate over each available_slot string
    for slot in available_slots:
        ajaxCall = slot.get_attribute("onclick")
        # Extract numbers using string manipulation or regular expressions
        parts = ajaxCall.split(",")
        # Extract and convert the court number to an integer
        court_number = int(parts[1].strip("'"))
        # Add the court number and AJAX call to the dictionary
        court_dict[court_number] = ajaxCall

    return court_dict