import logging
import time
import config.settings as settings
import bot.utils as utils

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions

from bot.types import BookingDetails, CourtPreferences


def _navigate_to_date(driver: webdriver.Chrome, booking_url: str, book_date: datetime) -> None:
    driver.get(booking_url)
    logging.debug("Going to booking page: %s", booking_url)
    wait = WebDriverWait(driver, 10)
    time.sleep(2)

    date_label = wait.until(EC.element_to_be_clickable((By.ID, "labelFechaActual")))
    date_label.click()

    desired_date = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            f"//td[@data-handler='selectDay' and @data-month='{book_date.month - 1}' and @data-year='{book_date.year}']/a[text()='{book_date.day}']",
        ))
    )
    desired_date.click()


def _find_available_slots(driver: webdriver.Chrome, time_slot: str) -> list:
    wait = WebDriverWait(driver, 10)
    time.sleep(2)
    selector = f"g[time='{time_slot}'] > rect.buttonHora[habilitado='true']"
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    return driver.find_elements(By.CSS_SELECTOR, selector)


def _complete_booking(driver: webdriver.Chrome) -> bool:
    wait = WebDriverWait(driver, 10)
    time.sleep(2)

    terms_checkbox = wait.until(EC.presence_of_element_located((By.ID, "terminos")))
    terms_checkbox.click()
    driver.find_element(By.ID, "groupButtons").click()

    conditions_checkbox = wait.until(EC.presence_of_element_located((
        By.ID, "ContentPlaceHolderContenido_CheckBoxAceptoCondicionesLegales",
    )))
    driver.execute_script("arguments[0].click();", conditions_checkbox)

    pay_button = wait.until(EC.presence_of_element_located((
        By.ID, "ContentPlaceHolderContenido_ButtonPagoSaldo",
    )))
    if pay_button.get_attribute("disabled") is not None:
        raise RuntimeError("Payment button is disabled — insufficient balance?")
    pay_button.click()

    if settings.DRY_RUN:
        logging.info("Dry run mode: skipping payment confirmation.")
        return True

    confirm_button = wait.until(EC.presence_of_element_located((
        By.ID, "ContentPlaceHolderContenido_ButtonConfirmar",
    )))
    confirm_button.click()

    confirmation = wait.until(EC.presence_of_element_located((
        By.ID, "ContentPlaceHolderContenido_LabelReservaPistas",
    )))
    confirmation_text = confirmation.text.lower()  # read once before element can go stale
    logging.debug("Confirmation element text: '%s'", confirmation_text)
    if "reserva confirmada" in confirmation_text or "reserva de pistes" in confirmation_text:
        logging.info("Booking confirmed successfully!")
        return True

    logging.error("Unexpected confirmation text: '%s'", confirmation_text)
    return False


def book_court(
    driver: webdriver.Chrome, court_preferences: CourtPreferences
) -> tuple[BookingDetails, bool]:
    venue_config = court_preferences["venue_config"]
    booking_successful = False
    booking_details: BookingDetails = {
        "date": "",
        "time": "",
        "court": "No court available",
        "location": venue_config["location"],
        "cost": "€48",
        "booked_by": court_preferences["booked_by"],
    }

    try:
        date_str = court_preferences["date"]
        time_str = court_preferences["time"]
        if date_str and time_str:
            book_date = datetime.strptime(date_str, "%Y-%m-%d")
            time_slot = time_str
        else:
            logging.warning("No date or time provided. Using default values.")
            book_date = utils.get_default_book_date()
            time_slot = utils.get_default_book_time_slot()

        logging.info("Booking the court for %s at %s", book_date.strftime("%B %d, %Y"), time_slot)

        _navigate_to_date(driver, venue_config["booking_url"], book_date)

        available_slots = _find_available_slots(driver, time_slot)
        logging.info("Found %d available slots", len(available_slots))

        court_name = utils.select_best_court(
            driver, available_slots, court_preferences["court_type"],
            venue_config["courts"], venue_config["indoor_courts"],
        )

        if not court_name:
            booking_details["date"] = book_date.strftime("%B %d, %Y")
            booking_details["time"] = time_slot
            return booking_details, booking_successful

        booking_details = {
            "date": book_date.strftime("%B %d, %Y"),
            "time": time_slot,
            "court": court_name,
            "location": venue_config["location"],
            "cost": "€45" if "Outdoor" in court_name else "€48",
            "booked_by": court_preferences["booked_by"],
        }

        booking_successful = _complete_booking(driver)

    except selenium.common.exceptions.TimeoutException as e:
        logging.error("Timed out waiting for an element")
        logging.debug("Exception details: %s", e)

    return booking_details, booking_successful
