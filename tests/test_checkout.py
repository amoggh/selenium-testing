import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import (
    ERR_CHECKOUT_FIRST_NAME,
    ERR_CHECKOUT_LAST_NAME,
    ERR_CHECKOUT_POSTAL_CODE,
)


@pytest.mark.positive
@pytest.mark.checkout
@pytest.mark.smoke
def test_complete_end_to_end_checkout_flow(logged_in_driver):
    """Positive Test: End-to-end purchase flow from item selection to order dispatch confirmation."""
    inventory = InventoryPage(logged_in_driver)
    product_name = "Sauce Labs Backpack"
    inventory.add_item_to_cart_by_name(product_name)
    inventory.go_to_cart()

    cart = CartPage(logged_in_driver)
    assert cart.is_loaded()
    assert product_name in cart.get_item_names()
    cart.proceed_to_checkout()

    checkout = CheckoutPage(logged_in_driver)
    assert checkout.is_step_one_loaded()

    # Step 1: Fill shipping information
    checkout.fill_checkout_info("John", "Doe", "12345")
    checkout.click_continue()

    # Step 2: Overview validation
    assert checkout.is_step_two_loaded()
    subtotal = checkout.get_subtotal_text()
    assert "29.99" in subtotal

    # Step 3: Complete order
    checkout.click_finish()
    assert checkout.is_complete_loaded()
    assert checkout.get_complete_header() == "Thank you for your order!"
    assert "dispatched" in checkout.get_complete_text().lower()


@pytest.mark.negative
@pytest.mark.checkout
def test_checkout_missing_first_name(logged_in_driver):
    """Negative Test: Verify validation error when First Name is omitted."""
    inventory = InventoryPage(logged_in_driver)
    inventory.add_item_by_index(0)
    inventory.go_to_cart()

    cart = CartPage(logged_in_driver)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(logged_in_driver)
    checkout.fill_checkout_info("", "Doe", "12345")
    checkout.click_continue()

    assert checkout.is_error_displayed()
    assert checkout.get_error_message() == ERR_CHECKOUT_FIRST_NAME


@pytest.mark.negative
@pytest.mark.checkout
def test_checkout_missing_last_name(logged_in_driver):
    """Negative Test: Verify validation error when Last Name is omitted."""
    inventory = InventoryPage(logged_in_driver)
    inventory.add_item_by_index(0)
    inventory.go_to_cart()

    cart = CartPage(logged_in_driver)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(logged_in_driver)
    checkout.fill_checkout_info("John", "", "12345")
    checkout.click_continue()

    assert checkout.is_error_displayed()
    assert checkout.get_error_message() == ERR_CHECKOUT_LAST_NAME


@pytest.mark.negative
@pytest.mark.checkout
def test_checkout_missing_postal_code(logged_in_driver):
    """Negative Test: Verify validation error when Postal Code is omitted."""
    inventory = InventoryPage(logged_in_driver)
    inventory.add_item_by_index(0)
    inventory.go_to_cart()

    cart = CartPage(logged_in_driver)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(logged_in_driver)
    checkout.fill_checkout_info("John", "Doe", "")
    checkout.click_continue()

    assert checkout.is_error_displayed()
    assert checkout.get_error_message() == ERR_CHECKOUT_POSTAL_CODE


@pytest.mark.negative
@pytest.mark.checkout
def test_checkout_all_fields_empty(logged_in_driver):
    """Negative Test: Verify validation error when all checkout fields are empty."""
    inventory = InventoryPage(logged_in_driver)
    inventory.add_item_by_index(0)
    inventory.go_to_cart()

    cart = CartPage(logged_in_driver)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(logged_in_driver)
    checkout.fill_checkout_info("", "", "")
    checkout.click_continue()

    assert checkout.is_error_displayed()
    assert checkout.get_error_message() == ERR_CHECKOUT_FIRST_NAME


@pytest.mark.positive
@pytest.mark.checkout
def test_checkout_cancel_step_one_returns_to_cart(logged_in_driver):
    """Positive Flow: Cancelling checkout from Step One returns the user back to the cart."""
    inventory = InventoryPage(logged_in_driver)
    inventory.add_item_by_index(0)
    inventory.go_to_cart()

    cart = CartPage(logged_in_driver)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(logged_in_driver)
    assert checkout.is_step_one_loaded()

    checkout.click_cancel()
    assert cart.is_loaded()
    assert "/cart.html" in logged_in_driver.current_url
