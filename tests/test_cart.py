import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.mark.positive
@pytest.mark.cart
@pytest.mark.smoke
def test_add_single_product_to_cart(logged_in_driver):
    """Verify adding a single item updates the cart badge and displays in the cart."""
    inventory = InventoryPage(logged_in_driver)
    product_name = "Sauce Labs Backpack"

    inventory.add_item_to_cart_by_name(product_name)
    assert inventory.get_cart_badge_count() == 1, "Cart badge count should be 1"

    inventory.go_to_cart()
    cart = CartPage(logged_in_driver)
    assert cart.is_loaded(), "Cart page should be loaded"
    cart_items = cart.get_item_names()
    assert product_name in cart_items, f"'{product_name}' should be in cart"
    assert cart.get_item_count() == 1


@pytest.mark.positive
@pytest.mark.cart
def test_add_two_different_products(logged_in_driver):
    """Verify adding two distinct products reflects in both badge count and cart list."""
    inventory = InventoryPage(logged_in_driver)
    item_1 = "Sauce Labs Backpack"
    item_2 = "Sauce Labs Bike Light"

    price_1 = inventory.get_product_price(item_1)
    price_2 = inventory.get_product_price(item_2)

    inventory.add_item_to_cart_by_name(item_1)
    inventory.add_item_to_cart_by_name(item_2)

    assert inventory.get_cart_badge_count() == 2, "Cart badge count should be 2"

    inventory.go_to_cart()
    cart = CartPage(logged_in_driver)
    assert cart.is_loaded()

    cart_names = cart.get_item_names()
    cart_prices = cart.get_item_prices()

    assert item_1 in cart_names
    assert item_2 in cart_names
    assert price_1 in cart_prices
    assert price_2 in cart_prices
    assert cart.get_item_count() == 2


@pytest.mark.positive
@pytest.mark.cart
def test_add_multiple_products_cart_badge(logged_in_driver):
    """Verify adding three products accurately increments the badge count."""
    inventory = InventoryPage(logged_in_driver)
    products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie",
    ]

    for p in products:
        inventory.add_item_to_cart_by_name(p)

    assert inventory.get_cart_badge_count() == len(products)


@pytest.mark.positive
@pytest.mark.cart
def test_remove_item_from_inventory_page(logged_in_driver):
    """Verify removing an added item directly from the inventory page removes it from the cart."""
    inventory = InventoryPage(logged_in_driver)
    product_name = "Sauce Labs Backpack"

    inventory.add_item_to_cart_by_name(product_name)
    assert inventory.get_cart_badge_count() == 1

    inventory.remove_item_from_cart_by_name(product_name)
    assert inventory.get_cart_badge_count() == 0, "Cart badge should be cleared after removal"
    assert not inventory.is_cart_badge_present(), "Cart badge element should not be displayed"


@pytest.mark.positive
@pytest.mark.cart
def test_remove_item_from_cart_page(logged_in_driver):
    """Verify removing an item from the cart page updates the cart contents and badge count."""
    inventory = InventoryPage(logged_in_driver)
    item_1 = "Sauce Labs Backpack"
    item_2 = "Sauce Labs Bike Light"

    inventory.add_item_to_cart_by_name(item_1)
    inventory.add_item_to_cart_by_name(item_2)
    assert inventory.get_cart_badge_count() == 2

    inventory.go_to_cart()
    cart = CartPage(logged_in_driver)
    assert cart.get_item_count() == 2

    # Remove item_1 from inside cart
    cart.remove_item_by_name(item_1)

    remaining_items = cart.get_item_names()
    assert item_1 not in remaining_items
    assert item_2 in remaining_items
    assert cart.get_item_count() == 1


@pytest.mark.positive
@pytest.mark.cart
def test_continue_shopping_from_cart(logged_in_driver):
    """Verify navigating back to inventory via 'Continue Shopping' preserves cart state."""
    inventory = InventoryPage(logged_in_driver)
    product_name = "Sauce Labs Backpack"

    inventory.add_item_to_cart_by_name(product_name)
    inventory.go_to_cart()

    cart = CartPage(logged_in_driver)
    assert cart.is_loaded()

    cart.continue_shopping()
    assert inventory.is_loaded(), "Should navigate back to products page"
    assert inventory.get_cart_badge_count() == 1, "Cart state should be preserved"
