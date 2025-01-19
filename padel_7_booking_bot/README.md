# Padel 7 Booking Bot

## Overview
This project is a Selenium-based bot designed to automate the booking process for padel courts on the Padel7 Sant Martí website. The bot can log into the website and reserve a court based on user preferences.

## Directory Structure
```
padel_booking_bot/
├── README.md                  # Documentation for the project
├── requirements.txt           # List of dependencies (e.g., Selenium, requests)
├── .env                       # Environment file for sensitive data (e.g., credentials)
├── main.py                    # Entry point for the bot
├── config/
│   └── settings.py            # Configuration settings (e.g., URLs, timeouts)
├── bot/
│   ├── __init__.py            # Makes the folder a package
│   ├── login.py               # Code to handle login functionality
│   ├── booking.py             # Code to handle booking functionality
│   └── utils.py               # Helper functions (e.g., wait utilities, logging)
├── tests/
│   ├── __init__.py            # Makes the folder a package
│   ├── test_login.py          # Tests for the login module
│   ├── test_booking.py        # Tests for the booking module
│   └── test_utils.py          # Tests for utility functions
├── logs/
│   └── bot.log                # Logs for debugging and monitoring
├── screenshots/               # Folder for storing screenshots (e.g., for debugging)
│   └── example.png            # Example screenshot
└── drivers/
    └── chromedriver           # WebDriver executable (place for ChromeDriver or other browsers)
```

## Explanation of Components

### 1. `README.md`
Documentation explaining the purpose, setup instructions, and usage of the bot.

### 2. `requirements.txt`
List of Python dependencies. Example:
```text
selenium
python-dotenv
```
Install dependencies with:
```bash
pip install -r requirements.txt
```

### 3. `.env`
A file to securely store sensitive information like usernames and passwords. Example:
```env
USERNAME=your_username
PASSWORD=your_password
```
Use the `python-dotenv` package to load these variables into your code.

### 4. `main.py`
The entry point of the project that orchestrates the bot workflow. It imports and uses the modules from the `bot` folder.

### 5. `config/settings.py`
Contains configuration values like:
```python
BASE_URL = "https://padel7santmarti.com/Booking/Grid.aspx?id=6"
LOGIN_URL = BASE_URL + "/login"
TIMEOUT = 10  # Default timeout for Selenium waits
```

### 6. `bot/`
The core logic of the bot, divided into modules:
- **`login.py`**: Handles the login process.
- **`booking.py`**: Automates the court booking process.
- **`utils.py`**: Contains helper functions like logging, taking screenshots, or retries.

### 7. `tests/`
Contains unit and integration tests to ensure the bot's functionality. Use a framework like `unittest` or `pytest`.

### 8. `logs/`
Stores logs for monitoring and debugging. Configure logging to output to this file.

### 9. `screenshots/`
Saves screenshots of the browser (useful for debugging or verifying bot actions).

### 10. `drivers/`
A folder to store browser drivers like ChromeDriver or GeckoDriver. This keeps your project clean and portable.

## How to Use

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd padel_booking_bot
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file with your credentials:
    ```env
    USERNAME=your_username
    PASSWORD=your_password
    ```

4. Run the bot:
    ```bash
    python main.py
    ```

## Example Workflow
1. The bot uses `login.py` to log in to the website.
2. It uses `booking.py` to automate the booking process based on user preferences.
3. Logs are saved in `logs/bot.log`, and screenshots are saved in `screenshots/` in case of errors.

## Future Improvements
- Add support for multi-user booking.
- Implement advanced error handling and retries.
- Schedule bookings automatically based on user-defined time slots.

## License
This project is open-source and available under the [MIT License](LICENSE).

