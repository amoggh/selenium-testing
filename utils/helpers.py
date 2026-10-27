import csv
import os
from datetime import datetime
from pathlib import Path

# Shared Configuration Constants
BASE_URL = os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com/")
DEFAULT_TIMEOUT = int(os.getenv("SELENIUM_DEFAULT_TIMEOUT", "10"))

# SauceDemo Standard Credentials
STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PROBLEM_USER = "problem_user"
PERF_GLITCH_USER = "performance_glitch_user"
PASSWORD = "secret_sauce"

# SauceDemo Known Error Messages
ERR_USERNAME_REQUIRED = "Epic sadface: Username is required"
ERR_PASSWORD_REQUIRED = "Epic sadface: Password is required"
ERR_INVALID_CREDENTIALS = "Epic sadface: Username and password do not match any user in this service"
ERR_LOCKED_OUT = "Epic sadface: Sorry, this user has been locked out."

# Checkout Error Messages
ERR_CHECKOUT_FIRST_NAME = "Error: First Name is required"
ERR_CHECKOUT_LAST_NAME = "Error: Last Name is required"
ERR_CHECKOUT_POSTAL_CODE = "Error: Postal Code is required"

# Project Directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "reports"
TEST_DATA_DIR = PROJECT_ROOT / "test_data"


def load_csv_test_data(filename: str):
    """Load test cases from a CSV file located in test_data directory."""
    file_path = TEST_DATA_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Test data file not found: {file_path}")

    test_cases = []
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_cases.append(row)
    return test_cases


def generate_screenshot_path(test_name: str) -> str:
    """Generate a unique timestamped path for test failure screenshot."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    # Sanitize test name for valid filename across OS
    clean_test_name = test_name.replace("/", "_").replace("\\", "_").replace(":", "_").replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{clean_test_name}_{timestamp}.png"
    return str(SCREENSHOTS_DIR / filename)
