import logging
import config.settings as settings
import bot.utils as utils
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_to_site(username: str, password: str, env: str) -> webdriver.Chrome:
    driver = utils.create_chrome_driver(env)

    try:
        driver.get(settings.LOGIN_URL)
        logging.debug("Going to login page: %s", settings.LOGIN_URL)

        wait = WebDriverWait(driver, 10)

        # 1. Click Cookie Button
        refuse_cookies_button = wait.until(
            EC.element_to_be_clickable((By.ID, settings.LOGIN_REFUSE_COOKIES_BUTTON_ID))
        )
        refuse_cookies_button.click()

        # 2. (Optional but safer) Wait for overlay to disappear if present
        wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "banner-block-screen"))
        )

        # 3. Fill Username
        username_field = wait.until(
            EC.element_to_be_clickable((By.ID, settings.LOGIN_USERNAME_FIELD_ID))
        )
        username_field.send_keys(username)

        # 4. Fill Password
        password_field = wait.until(
            EC.element_to_be_clickable((By.ID, settings.LOGIN_PASSWORD_FIELD_ID))
        )
        password_field.send_keys(password)

        # 5. Wait for Submit Button to be Clickable
        submit_button = wait.until(
            EC.element_to_be_clickable((By.ID, settings.LOGIN_BUTTON_ID))
        )
        submit_button.click()

        wait.until(EC.url_changes(settings.LOGIN_URL))
        logging.debug("Landed in the user profile page: %s", driver.current_url)

        return driver

    except Exception as e:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        utils.save_screenshot(driver, f"error_login_final_state_{timestamp}.png")
        logging.error("Error during login: %s", e)
        driver.quit()
        raise
