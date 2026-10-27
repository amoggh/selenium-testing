from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for SauceDemo Checkout flow (Information, Overview, and Confirmation)."""

    # Step One: Information Locators
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "h3[data-test='error']")

    # Step Two: Overview Locators
    SUMMARY_INFO = (By.CLASS_NAME, "summary_info")
    SUMMARY_SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX = (By.CLASS_NAME, "summary_tax_label")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    # Step Three: Complete Locators
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    # --- Step One Methods ---
    def is_step_one_loaded(self) -> bool:
        """Verify checkout step one page is loaded."""
        try:
            return ("/checkout-step-one.html" in self.get_current_url()) and self.is_displayed(self.FIRST_NAME_INPUT)
        except Exception:
            return False

    def enter_first_name(self, first_name: str):
        """Enter first name in checkout form."""
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        return self

    def enter_last_name(self, last_name: str):
        """Enter last name in checkout form."""
        self.type_text(self.LAST_NAME_INPUT, last_name)
        return self

    def enter_postal_code(self, postal_code: str):
        """Enter postal code in checkout form."""
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def fill_checkout_info(self, first_name: str = "", last_name: str = "", postal_code: str = ""):
        """Fill all checkout step one fields."""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self

    def click_continue(self):
        """Click continue to proceed to step two."""
        self.click(self.CONTINUE_BUTTON)
        return self

    def click_cancel(self):
        """Click cancel to return to cart."""
        self.click(self.CANCEL_BUTTON)
        return self

    def get_error_message(self) -> str:
        """Get error text displayed on checkout step one."""
        return self.get_text(self.ERROR_CONTAINER)

    def is_error_displayed(self) -> bool:
        """Check if error banner is displayed on checkout step one."""
        return self.is_displayed(self.ERROR_CONTAINER)

    # --- Step Two Methods ---
    def is_step_two_loaded(self) -> bool:
        """Verify checkout overview step two is loaded."""
        try:
            return ("/checkout-step-two.html" in self.get_current_url()) and self.is_displayed(self.FINISH_BUTTON)
        except Exception:
            return False

    def get_subtotal_text(self) -> str:
        """Get subtotal label text."""
        return self.get_text(self.SUMMARY_SUBTOTAL)

    def get_total_text(self) -> str:
        """Get total label text."""
        return self.get_text(self.SUMMARY_TOTAL)

    def click_finish(self):
        """Click finish button to complete order."""
        self.click(self.FINISH_BUTTON)
        return self

    # --- Complete Methods ---
    def is_complete_loaded(self) -> bool:
        """Verify checkout complete page is loaded."""
        try:
            return ("/checkout-complete.html" in self.get_current_url()) and self.is_displayed(self.COMPLETE_HEADER)
        except Exception:
            return False

    def get_complete_header(self) -> str:
        """Get thank you confirmation header."""
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        """Get secondary confirmation message text."""
        return self.get_text(self.COMPLETE_TEXT)
