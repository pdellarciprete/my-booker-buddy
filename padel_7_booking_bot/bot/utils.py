import os
import logging
import config.settings as settings

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