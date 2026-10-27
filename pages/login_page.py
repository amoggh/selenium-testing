from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.helpers import BASE_URL


class LoginPage(BasePage):
    """Page Object for SauceDemo Login Page."""

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_CLOSE_BUTTON = (By.CLASS_NAME, "error-button")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")

    def open(self, url: str = BASE_URL):
        """Navigate to the login page."""
        self.navigate(url)
        self.wait.until(lambda d: self.is_at_login_page())
        return self

    def is_at_login_page(self) -> bool:
        """Verify that the login fields and login button are present."""
        return self.is_displayed(self.LOGIN_BUTTON)

    def enter_username(self, username: str):
        """Enter username into input field."""
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        """Enter password into input field."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """Click the login submit button."""
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str = "", password: str = ""):
        """Convenience method to fill credentials and click login."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self) -> str:
        """Get the text of the displayed error notification."""
        return self.get_text(self.ERROR_CONTAINER)

    def is_error_displayed(self) -> bool:
        """Check if the error banner is displayed."""
        return self.is_displayed(self.ERROR_CONTAINER)

    def is_products_page_loaded(self) -> bool:
        """Check whether the user was redirected to the inventory/products page."""
        try:
            return ("/inventory.html" in self.get_current_url()) and self.is_displayed(self.INVENTORY_LIST)
        except Exception:
            return False

    def clear_inputs(self):
        """Clear both username and password input fields."""
        u_elem = self.find(self.USERNAME_INPUT)
        p_elem = self.find(self.PASSWORD_INPUT)
        u_elem.clear()
        p_elem.clear()
        return self
