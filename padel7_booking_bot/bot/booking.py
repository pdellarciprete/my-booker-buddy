import logging
import time
import config.settings as settings
import bot.utils as utils

from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

INDOOR_COURTS = ["0","1", "2", "3"]
OUTDOOR_COURTS = ["8","9", "10", "11"]

def book_court(driver, court_preferences):
    """
    Book a court based on the provided preferences

    Args:
        driver (webdriver): A Selenium WebDriver instance after login.
        court_preferences (dict): A dictionary containing court preferences.

    Returns:
        None
    """

    book_date = utils.get_default_book_date()
    time_slot = utils.get_default_book_time_slot()

    try:
        logging.info(f"Booking the court for {book_date.strftime('%d-%m-%Y')} at {time_slot}")
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
            EC.element_to_be_clickable((By.XPATH, f"//td[@data-handler='selectDay' and @data-month='{book_date.month-1}' and @data-year='{book_date.year}']/a[text()='{book_date.day}']"))
        )
        logging.debug(f"Click the desired date in the calendar")
        desired_date_element.click()
        WebDriverWait(driver, 60)

        # Wait until the court slots are present
        logging.debug(f"wait until the court slots are present")
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"g[time='{time_slot}'] > rect.buttonHora[habilitado='true']")))
        available_slots = driver.find_elements(By.CSS_SELECTOR, f"g[time='{time_slot}'] > rect.buttonHora[habilitado='true']")  # Find all clickable slots
        logging.info(f"Found %d available slots for the desired date", len(available_slots))

        # Select the best court
        utils.select_best_court(driver, available_slots)

        # Wait until the popup is present
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

        if settings.DRY_RUN:
            logging.info("Dry run mode enabled. Skipping payment confirmation.")
            return
        else:
            logging.info("Dry run mode disabled. Proceeding with payment confirmation.")
            # Payment confirmation
            confirm_payment_button = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolderContenido_ButtonConfirmar")))
            confirm_payment_button.click()

    except Exception as e:
        logging.debug("Taking a final screenshot before closing the WebDriver.")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        utils.save_screenshot(driver, f"error_booking_final_state_{timestamp}.png")
        logging.error(f"Error during booking: {e}")
        driver.quit()
        raise e
