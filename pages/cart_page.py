from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object for SauceDemo Shopping Cart Page."""

    # Locators
    TITLE = (By.CLASS_NAME, "title")
    CART_LIST = (By.CLASS_NAME, "cart_list")
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ITEM_QUANTITY = (By.CLASS_NAME, "cart_quantity")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def is_loaded(self) -> bool:
        """Verify cart page is loaded."""
        try:
            return ("/cart.html" in self.get_current_url()) and self.is_displayed(self.CART_LIST)
        except Exception:
            return False

    def get_header_title(self) -> str:
        """Return cart header title text (e.g. 'Your Cart')."""
        return self.get_text(self.TITLE)

    def get_item_count(self) -> int:
        """Return count of item rows in the cart."""
        try:
            items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
            return len(items)
        except Exception:
            return 0

    def get_item_names(self) -> list[str]:
        """Return list of item names present in the cart."""
        elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        return [el.text.strip() for el in elements]

    def get_item_prices(self) -> list[str]:
        """Return list of item prices present in the cart."""
        elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        return [el.text.strip() for el in elements]

    def get_item_row_by_name(self, product_name: str):
        """Locate cart item row containing given product name."""
        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        for item in items:
            name_el = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_el.text.strip().lower() == product_name.strip().lower():
                return item
        raise ValueError(f"Product '{product_name}' not found in cart.")

    def remove_item_by_name(self, product_name: str):
        """Remove a product from the cart by its name."""
        row = self.get_item_row_by_name(product_name)
        remove_button = row.find_element(By.CSS_SELECTOR, "button.cart_button")
        remove_button.click()
        return self

    def continue_shopping(self):
        """Click 'Continue Shopping' button to return to inventory."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        return self

    def proceed_to_checkout(self):
        """Click 'Checkout' button to begin checkout process."""
        self.click(self.CHECKOUT_BUTTON)
        return self
