# GLOBAL SETTINGS
BASE_URL = "https://padel7santmarti.com"
TIMEOUT = 10  # Default timeout for Selenium waits
LOGGING_LEVEL = "INFO"  # Logging level for the bot
SCREENSHOT_DIR = "screenshots"  # Directory to save screenshots
DRY_RUN = False  # Set to True to simulate the booking process without actually booking a court

# LOGIN SETTINGS
LOGIN_URL = BASE_URL + "/Login.aspx"
LOGIN_REFUSE_COOKIES_BUTTON_ID = "ctl00_ButtonPermitirNecesarios"
LOGIN_USERNAME_FIELD_ID = "ctl00_ContentPlaceHolderContenido_Login1_UserName"
LOGIN_PASSWORD_FIELD_ID = "ctl00_ContentPlaceHolderContenido_Login1_Password"
LOGIN_BUTTON_ID = "ctl00_ContentPlaceHolderContenido_Login1_LoginButton"
LOGIN_POST_LOGIN_ELEMENT_ID = "ctl00_ctl00_ContentPlaceHolderContenido_WUCMenuLateralIzquierdaIntranet_imgSocio"

# BOOKING SETTINGS

BOOKING_URL = BASE_URL + "/Booking/Grid.aspx?id=8"