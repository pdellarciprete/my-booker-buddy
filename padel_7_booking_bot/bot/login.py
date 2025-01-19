import logging
import config.settings as settings
import bot.utils as utils

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_to_site(username, password):
    """
    Logs in to the padel booking website using the provided credentials.

    Args:
        username (str): The username for login.
        password (str): The password for login.

    Returns:
        WebDriver: A Selenium WebDriver instance after login.
    """
    # Initialize the WebDriver
    driver = webdriver.Chrome()

    try:
        # Open the website
        driver.get(settings.LOGIN_URL)
        driver.maximize_window()
        logging.debug(f"Going to login page: {settings.LOGIN_URL}")

        # Wait for the cookies window and click it
        wait = WebDriverWait(driver, 10)
        logging.debug("Wait for the cookies window")

        refuse_cookies_button = wait.until(EC.presence_of_element_located((By.ID, settings.LOGIN_REFUSE_COOKIES_BUTTON_ID)))
        logging.debug("Search for the refuse cookies button")
        refuse_cookies_button.click()
        logging.debug("Click refuse cookies button")

        # Wait for the login form to load
        username_field = wait.until(EC.presence_of_element_located((By.ID, settings.LOGIN_USERNAME_FIELD_ID)))
        logging.debug("Search for the username field")
        password_field = driver.find_element(By.ID, settings.LOGIN_PASSWORD_FIELD_ID)
        logging.debug("Search for the password field")

        # Enter the credentials
        username_field.send_keys(username)
        password_field.send_keys(password)
        logging.debug("Fill Username and Password fields.")

        # Click the submit button
        submit_button = driver.find_element(By.ID, settings.LOGIN_BUTTON_ID)
        submit_button.click()
        logging.debug("Click submit button")

        # Verify successful login by checking a specific element on the post-login page
        wait.until(EC.presence_of_element_located((By.ID, settings.LOGIN_POST_LOGIN_ELEMENT_ID)))
        logging.debug("Landed in the user profile page")

        return driver

    except Exception as e:
        logging.debug("Taking a final screenshot before closing the WebDriver.")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        utils.save_screenshot(driver, f"error_login_final_state_{timestamp}.png")
        logging.error(f"Error during login: {e}")
        driver.quit()
        raise
