import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from utils.helpers import (
    BASE_URL,
    STANDARD_USER,
    PASSWORD,
    generate_screenshot_path,
)
from pages.login_page import LoginPage


def pytest_addoption(parser):
    """Register custom command-line options for pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default=os.getenv("BROWSER", "chrome").lower(),
        help="Browser type: chrome, firefox, or edge",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes"),
        help="Run browser in headless mode",
    )


@pytest.fixture(scope="function")
def driver(request):
    """Start a fresh browser instance for each independent test."""
    browser_name = request.config.getoption("--browser")
    is_headless = request.config.getoption("--headless")

    driver_instance = None

    if browser_name == "firefox":
        options = FirefoxOptions()
        if is_headless:
            options.add_argument("-headless")
        driver_instance = webdriver.Firefox(options=options)

    elif browser_name == "edge":
        options = EdgeOptions()
        if is_headless:
            options.add_argument("--headless=new")
        driver_instance = webdriver.Edge(options=options)

    else:
        # Default: Google Chrome
        options = ChromeOptions()
        if is_headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        driver_instance = webdriver.Chrome(options=options)

    # Maximize browser window
    driver_instance.maximize_window()

    # Attach driver to pytest node for screenshot hook
    request.node._driver = driver_instance

    yield driver_instance

    # Teardown: reliably close browser after test execution
    try:
        driver_instance.quit()
    except Exception:
        pass


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """Fixture that logs in with standard_user and provides driver on inventory page."""
    login_page = LoginPage(driver)
    login_page.open(BASE_URL)
    login_page.login(STANDARD_USER, PASSWORD)
    assert login_page.is_products_page_loaded(), "Precondition failed: standard user login failed."
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """pytest hook to automatically capture screenshots when tests fail."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Retrieve the driver instance from item or fixtures
        driver_instance = getattr(item, "_driver", None)
        if driver_instance is None and "driver" in item.funcargs:
            driver_instance = item.funcargs["driver"]
        elif driver_instance is None and "logged_in_driver" in item.funcargs:
            driver_instance = item.funcargs["logged_in_driver"]

        if driver_instance:
            try:
                screenshot_file = generate_screenshot_path(item.name)
                driver_instance.save_screenshot(screenshot_file)
                print(f"\n[Test Failure] Saved failure screenshot to: {screenshot_file}")

                # Attach screenshot to pytest-html report if pytest-html is active
                try:
                    import pytest_html
                    extras = getattr(report, "extras", [])
                    extras.append(pytest_html.extras.image(screenshot_file))
                    report.extras = extras
                except Exception:
                    pass
            except Exception as e:
                # Resilient error handling so screenshot issues never mask original failure
                print(f"\n[Warning] Could not capture failure screenshot: {e}")
