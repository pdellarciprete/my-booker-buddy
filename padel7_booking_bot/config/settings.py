from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_username: str
    app_password: str
    app_slack_token: str = ""
    app_slack_prod_webhook_url: str = ""
    app_slack_test_webhook_url: str = ""
    env: str = "docker"  # or local


# GLOBAL SETTINGS
BASE_URL = "https://padel7santmarti.com"
TIMEOUT = 10  # Default timeout for Selenium waits
LOGGING_LEVEL = "INFO"  # Logging level for the bot
SCREENSHOT_DIR = "screenshots"  # Directory to save screenshots
DRY_RUN = True  # Set to True to simulate the booking process without actually booking a court
NOTIFICATION_ENABLED = False  # Set to True to enable Slack notifications

# LOGIN SETTINGS
LOGIN_URL = BASE_URL + "/Login.aspx"
LOGIN_REFUSE_COOKIES_BUTTON_ID = "ButtonPermitirNecesarios"
LOGIN_USERNAME_FIELD_ID = "ContentPlaceHolderContenido_Login1_UserName"
LOGIN_PASSWORD_FIELD_ID = "ContentPlaceHolderContenido_Login1_Password"
LOGIN_BUTTON_ID = "ContentPlaceHolderContenido_Login1_LoginButton"

# VENUE SETTINGS
VENUES = {
    "glories": {
        "booking_url": BASE_URL + "/Booking/Grid.aspx?id=8",
        "location": "Padel7 Glories, Barcelona",
        "courts": {
            "0": "Indoor 1",
            "1": "Indoor 2",
            "2": "Indoor 3",
            "3": "Indoor 4",
            "4": "Outdoor 5",
            "5": "Outdoor 6",
            "6": "Outdoor 7",
            "7": "Outdoor 8",
            "8": "Outdoor 9",
            "9": "Outdoor 10",
        },
        "indoor_courts": {"0", "1", "2", "3"},
    },
    "poblenou": {
        "booking_url": BASE_URL + "/Booking/Grid.aspx?id=10",
        "location": "Padel7 Poblenou, Barcelona",
        "courts": {
            "0": "P7Poblenou 1",
            "1": "P7Poblenou 2",
            "2": "P7Poblenou 3",
            "3": "P7Poblenou 4",
            "4": "P7Poblenou 5",
        },
        "indoor_courts": {"0", "1", "2", "3", "4"},
    },
}
