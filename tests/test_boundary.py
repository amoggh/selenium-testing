import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.boundary
@pytest.mark.cart
def test_cart_badge_zero_items_boundary(logged_in_driver):
    """Boundary Value Analysis: Lower boundary (0 items in cart).
    Validates that the cart badge element is completely absent when 0 items are selected.
    """
    inventory = InventoryPage(logged_in_driver)
    assert not inventory.is_cart_badge_present(), "Badge element must not be visible at 0 items"
    assert inventory.get_cart_badge_count() == 0, "Cart badge count must evaluate to 0"


@pytest.mark.boundary
@pytest.mark.cart
def test_cart_badge_single_item_boundary(logged_in_driver):
    """Boundary Value Analysis: Minimal active boundary (1 item).
    Validates that the cart badge appears immediately upon crossing from 0 to 1 item.
    """
    inventory = InventoryPage(logged_in_driver)
    inventory.add_item_by_index(0)

    assert inventory.is_cart_badge_present(), "Badge should become visible when 1 item is added"
    assert inventory.get_cart_badge_count() == 1


@pytest.mark.boundary
@pytest.mark.cart
def test_cart_badge_maximum_catalog_boundary(logged_in_driver):
    """Boundary Value Analysis: Upper boundary (all 6 catalog items added).
    Validates that the cart badge correctly increments up to maximum catalog capacity.
    """
    inventory = InventoryPage(logged_in_driver)
    product_names = inventory.get_all_product_names()
    total_products = len(product_names)

    # Add every available product in the catalog
    for name in product_names:
        inventory.add_item_to_cart_by_name(name)

    assert inventory.get_cart_badge_count() == total_products, f"Expected badge count {total_products}"

    # Navigate to cart to verify all 6 are reflected
    inventory.go_to_cart()
    cart = CartPage(logged_in_driver)
    assert cart.get_item_count() == total_products


@pytest.mark.boundary
@pytest.mark.cart
def test_cart_add_all_then_remove_all_boundary_transitions(logged_in_driver):
    """Boundary Value Analysis: Full lifecycle boundary transition.
    0 -> Max (6) -> 0. Validates clean decrement and absence of badge when emptied.
    """
    inventory = InventoryPage(logged_in_driver)
    product_names = inventory.get_all_product_names()
    total = len(product_names)

    # Add all products
    for name in product_names:
        inventory.add_item_to_cart_by_name(name)
    assert inventory.get_cart_badge_count() == total

    # Sequentially remove all products
    for i, name in enumerate(product_names, 1):
        inventory.remove_item_from_cart_by_name(name)
        expected_remaining = total - i
        assert inventory.get_cart_badge_count() == expected_remaining

    # Verify boundary 0 reached again
    assert not inventory.is_cart_badge_present()
    assert inventory.get_cart_badge_count() == 0


@pytest.mark.boundary
@pytest.mark.checkout
def test_checkout_input_length_boundary(logged_in_driver):
    """Robustness & Boundary Testing: Extreme input length (250+ characters).
    Ensures that very long strings do not trigger unhandled browser crashes or HTTP 500s.
    """
    inventory = InventoryPage(logged_in_driver)
    inventory.add_item_by_index(0)
    inventory.go_to_cart()

    cart = CartPage(logged_in_driver)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(logged_in_driver)
    assert checkout.is_step_one_loaded()

    long_first_name = "A" * 255
    long_last_name = "B" * 255
    long_postal_code = "9" * 50

    checkout.fill_checkout_info(long_first_name, long_last_name, long_postal_code)
    checkout.click_continue()

    # The application should either navigate to step two or remain stable without crash
    assert checkout.is_step_two_loaded() or checkout.is_step_one_loaded(), "Application crashed on long input"


@pytest.mark.boundary
@pytest.mark.checkout
def test_checkout_special_characters_robustness(logged_in_driver):
    """Robustness Testing: Special characters and injection patterns in form fields.
    Validates system resilience against special symbols without breaking DOM or throwing uncaught JS errors.
    """
    inventory = InventoryPage(logged_in_driver)
    inventory.add_item_by_index(0)
    inventory.go_to_cart()

    cart = CartPage(logged_in_driver)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(logged_in_driver)
    assert checkout.is_step_one_loaded()

    special_chars = "<script>alert('test')</script> !@#$%^&*()_+-={}|[]:;<>?,./"
    checkout.fill_checkout_info(special_chars, "O'Connor-Smith", "90210-!#")
    checkout.click_continue()

    # Verify application handles gracefully without crashing
    assert checkout.is_step_two_loaded() or checkout.is_step_one_loaded()


@pytest.mark.boundary
@pytest.mark.cart
def test_rapid_toggle_add_remove_robustness(logged_in_driver):
    """Robustness Testing: Rapid alternating click actions on the same item.
    Ensures that fast sequential state changes maintain consistent UI state.
    """
    inventory = InventoryPage(logged_in_driver)
    item_name = "Sauce Labs Backpack"

    # Rapid toggle 5 times: Add -> Remove -> Add -> Remove -> Add
    for i in range(5):
        if i % 2 == 0:
            inventory.add_item_to_cart_by_name(item_name)
            assert inventory.get_cart_badge_count() == 1
        else:
            inventory.remove_item_from_cart_by_name(item_name)
            assert inventory.get_cart_badge_count() == 0

    # Final state after 5 iterations (0,1,2,3,4) must be Added (badge = 1)
    assert inventory.get_cart_badge_count() == 1
