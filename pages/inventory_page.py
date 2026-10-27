from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page Object for SauceDemo Products/Inventory Page."""

    # Locators
    TITLE = (By.CLASS_NAME, "title")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ITEM_DESC = (By.CLASS_NAME, "inventory_item_desc")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    # Menu Locators
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    RESET_APP_STATE_LINK = (By.ID, "reset_sidebar_link")

    def is_loaded(self) -> bool:
        """Verify inventory page is loaded."""
        try:
            return ("/inventory.html" in self.get_current_url()) and self.is_displayed(self.INVENTORY_LIST)
        except Exception:
            return False

    def get_header_title(self) -> str:
        """Return the header title text (e.g., 'Products')."""
        return self.get_text(self.TITLE)

    def get_all_product_names(self) -> list[str]:
        """Return list of all product names visible on the inventory page."""
        items = self.find_all(self.ITEM_NAME)
        return [item.text.strip() for item in items]

    def get_product_element_by_name(self, product_name: str):
        """Locate the inventory item parent container for a given product name."""
        items = self.find_all(self.INVENTORY_ITEM)
        for item in items:
            name_elem = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_elem.text.strip().lower() == product_name.strip().lower():
                return item
        raise ValueError(f"Product '{product_name}' not found on inventory page.")

    def get_product_price(self, product_name: str) -> str:
        """Get the price string of a specific product."""
        item = self.get_product_element_by_name(product_name)
        price_elem = item.find_element(By.CLASS_NAME, "inventory_item_price")
        return price_elem.text.strip()

    def add_item_to_cart_by_name(self, product_name: str):
        """Click 'Add to cart' button for a given product name."""
        item = self.get_product_element_by_name(product_name)
        button = item.find_element(By.CSS_SELECTOR, "button.btn_inventory")
        button.click()
        return self

    def remove_item_from_cart_by_name(self, product_name: str):
        """Click 'Remove' button for a given product name on inventory page."""
        item = self.get_product_element_by_name(product_name)
        button = item.find_element(By.CSS_SELECTOR, "button.btn_inventory")
        button.click()
        return self

    def add_item_by_index(self, index: int):
        """Add product by index (0-based) to cart."""
        items = self.find_all(self.INVENTORY_ITEM)
        if 0 <= index < len(items):
            button = items[index].find_element(By.CSS_SELECTOR, "button.btn_inventory")
            button.click()
            return self
        raise IndexError(f"Product index {index} out of range (0-{len(items)-1}).")

    def remove_item_by_index(self, index: int):
        """Remove product by index (0-based) from cart on inventory page."""
        items = self.find_all(self.INVENTORY_ITEM)
        if 0 <= index < len(items):
            button = items[index].find_element(By.CSS_SELECTOR, "button.btn_inventory")
            button.click()
            return self
        raise IndexError(f"Product index {index} out of range (0-{len(items)-1}).")

    def is_cart_badge_present(self) -> bool:
        """Check if cart badge element is currently displayed."""
        return self.is_displayed(self.CART_BADGE, timeout=1)

    def get_cart_badge_count(self) -> int:
        """Return the numeric cart count from badge, or 0 if badge is absent."""
        if not self.is_cart_badge_present():
            return 0
        text = self.get_text(self.CART_BADGE)
        return int(text) if text.isdigit() else 0

    def go_to_cart(self):
        """Click the shopping cart link to navigate to cart page."""
        self.click(self.CART_LINK)
        return self

    def open_menu(self):
        """Click burger menu icon."""
        self.click(self.BURGER_MENU_BUTTON)
        return self

    def logout(self):
        """Open sidebar menu and click logout link."""
        self.open_menu()
        self.click(self.LOGOUT_LINK)
        return self
