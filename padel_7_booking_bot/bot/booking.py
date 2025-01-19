import logging
import time
import config.settings as settings
import bot.utils as utils

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def book_court(driver, court_preferences):
    """
    Book a court based on the provided preferences

    Args:
        driver (webdriver): A Selenium WebDriver instance after login.
        court_preferences (dict): A dictionary containing court preferences.

    Returns:
        None
    """

    try:
        # Open the website
        driver.get(settings.BOOKING_URL)
        logging.debug(f"Going to booking page: {settings.BOOKING_URL}")
        wait = WebDriverWait(driver, 10)

        # Wait until the DatePicker input is clickable
        datepicker_element = wait.until(EC.presence_of_element_located((By.ID, "fechaTabla")))
        datepicker_element.click()
        logging.debug(f"Click the DatePicker input to open the calendar")

        # Find and click the desired date
        desired_date_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//td[@data-handler="selectDay" and @data-month="0" and @data-year="2025"]/a[text()="29"]'))  # Example XPath, adjust to match your DatePicker
        )
        logging.debug(f"Click the DatePicker input to open the calendar")
        desired_date_element.click()
        WebDriverWait(driver, 60)


        logging.debug(f"wait until the court slot is present")
        court_slot_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "g[time='18:00-19:30'] > rect.buttonHora[habilitado='true']")))
        # Some seconds to make sure the court slot is clickable
        time.sleep(2)

        logging.debug(f"Click on the court slot")
        court_slot_element.click()
        # Some seconds to make sure the popup is loaded
        time.sleep(2)

        # Popup elements
        terms_checkbox = wait.until(EC.presence_of_element_located((By.ID, "terminos")))
        terms_checkbox.click()
        rect_element_90_minutes = driver.find_element(By.ID, "groupButtons")
        rect_element_90_minutes.click()

        # Payment page
        conditions_checkbox = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolderContenido_CheckBoxAceptoCondicionesLegales")))
        conditions_checkbox.click()
        pay_button = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolderContenido_ButtonPagoSaldo")))
        pay_button.click()

    except Exception as e:
        logging.debug("Taking a final screenshot before closing the WebDriver.")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        utils.save_screenshot(driver, f"error_booking_final_state_{timestamp}.png")
        logging.error(f"Error during booking: {e}")
        driver.quit()
        raise e



