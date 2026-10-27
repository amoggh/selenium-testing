from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.helpers import DEFAULT_TIMEOUT


class BasePage:
    """Base Page Object class containing common browser actions and explicit waits."""

    def __init__(self, driver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def navigate(self, url: str):
        """Navigate browser to the given URL."""
        self.driver.get(url)

    def find(self, locator):
        """Wait for element to be visible and return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """Wait for elements to be present and return list of elements."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """Wait for element to be clickable and click it."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def type_text(self, locator, text: str, clear_first: bool = True):
        """Type text into an input field with optional clearing."""
        element = self.find(locator)
        if clear_first:
            element.clear()
        if text:
            element.send_keys(text)
        return element

    def get_text(self, locator) -> str:
        """Get visible text from an element."""
        return self.find(locator).text.strip()

    def is_displayed(self, locator, timeout: int = 3) -> bool:
        """Check if an element is visible within a custom short timeout."""
        try:
            custom_wait = WebDriverWait(self.driver, timeout)
            element = custom_wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.driver.current_url

    def wait_for_url_contains(self, fragment: str) -> bool:
        """Wait until the URL contains the specified substring."""
        return self.wait.until(EC.url_contains(fragment))

    def get_title(self) -> str:
        """Return the document title."""
        return self.driver.title
