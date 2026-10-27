import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.helpers import (
    BASE_URL,
    STANDARD_USER,
    LOCKED_OUT_USER,
    PASSWORD,
    ERR_USERNAME_REQUIRED,
    ERR_PASSWORD_REQUIRED,
    ERR_INVALID_CREDENTIALS,
    ERR_LOCKED_OUT,
    load_csv_test_data,
)


# ============================================================================
# Original Working Test (Preserved directly as requested)
# ============================================================================

def test_valid_login(driver):
    """Original working baseline login test verifying standard login flow."""
    # Step 1: Open the website
    driver.get(BASE_URL)

    wait = WebDriverWait(driver, 10)

    # Step 2: Locate the login fields
    username_field = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "user-name")
        )
    )

    password_field = driver.find_element(
        By.ID, "password"
    )

    # Step 3: Enter valid credentials
    username_field.send_keys(STANDARD_USER)
    password_field.send_keys(PASSWORD)

    # Step 4: Click the login button
    driver.find_element(
        By.ID, "login-button"
    ).click()

    # Step 5: Wait for the products page
    wait.until(
        EC.url_contains("/inventory.html")
    )

    # Step 6: Verify the expected result
    assert "/inventory.html" in driver.current_url

    assert wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_list")
        )
    ).is_displayed()


# ============================================================================
# Positive Login Tests (Page Object Model)
# ============================================================================

@pytest.mark.positive
@pytest.mark.login
@pytest.mark.smoke
def test_positive_login_standard_user(driver):
    """Verify that a standard user can successfully log in and reach inventory."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(STANDARD_USER, PASSWORD)

    inventory_page = InventoryPage(driver)
    assert inventory_page.is_loaded(), "Expected inventory page to load after valid login"
    assert "inventory.html" in driver.current_url
    assert inventory_page.get_header_title() == "Products"


@pytest.mark.positive
@pytest.mark.login
def test_inventory_visibility_after_login(driver):
    """Verify inventory products and catalog are visible after valid login."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(STANDARD_USER, PASSWORD)

    inventory_page = InventoryPage(driver)
    product_names = inventory_page.get_all_product_names()
    assert len(product_names) > 0, "Expected at least one product in catalog"
    assert "Sauce Labs Backpack" in product_names


# ============================================================================
# Negative Login Tests (Authentication Edge Cases & Validations)
# ============================================================================

@pytest.mark.negative
@pytest.mark.login
def test_negative_login_invalid_username(driver):
    """Verify error message when logging in with invalid username."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("invalid_user_name", PASSWORD)

    assert login_page.is_error_displayed()
    assert login_page.get_error_message() == ERR_INVALID_CREDENTIALS


@pytest.mark.negative
@pytest.mark.login
def test_negative_login_invalid_password(driver):
    """Verify error message when logging in with invalid password."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(STANDARD_USER, "wrong_password_123")

    assert login_page.is_error_displayed()
    assert login_page.get_error_message() == ERR_INVALID_CREDENTIALS


@pytest.mark.negative
@pytest.mark.login
def test_negative_login_both_invalid(driver):
    """Verify error message when both username and password are invalid."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("invalid_user", "invalid_pass")

    assert login_page.is_error_displayed()
    assert login_page.get_error_message() == ERR_INVALID_CREDENTIALS


@pytest.mark.negative
@pytest.mark.login
def test_negative_login_empty_credentials(driver):
    """Verify validation error when both fields are left empty."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("", "")

    assert login_page.is_error_displayed()
    assert login_page.get_error_message() == ERR_USERNAME_REQUIRED


@pytest.mark.negative
@pytest.mark.login
def test_negative_login_empty_username_populated_password(driver):
    """Verify error when username is empty and password is populated."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("", PASSWORD)

    assert login_page.is_error_displayed()
    assert login_page.get_error_message() == ERR_USERNAME_REQUIRED


@pytest.mark.negative
@pytest.mark.login
def test_negative_login_populated_username_empty_password(driver):
    """Verify error when username is populated and password is empty."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(STANDARD_USER, "")

    assert login_page.is_error_displayed()
    assert login_page.get_error_message() == ERR_PASSWORD_REQUIRED


@pytest.mark.negative
@pytest.mark.login
def test_negative_login_locked_out_user(driver):
    """Verify error message for locked out user."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(LOCKED_OUT_USER, PASSWORD)

    assert login_page.is_error_displayed()
    assert login_page.get_error_message() == ERR_LOCKED_OUT


@pytest.mark.negative
@pytest.mark.login
def test_negative_login_recovery_to_valid_login(driver):
    """Verify that user can recover from an invalid login attempt and log in successfully."""
    login_page = LoginPage(driver)
    login_page.open()

    # Step 1: Attempt invalid login and verify error
    login_page.login("invalid_user", "wrong_pass")
    assert login_page.is_error_displayed()
    assert login_page.get_error_message() == ERR_INVALID_CREDENTIALS

    # Step 2: Clear fields, enter valid credentials, and verify successful login
    login_page.login(STANDARD_USER, PASSWORD)

    inventory_page = InventoryPage(driver)
    assert inventory_page.is_loaded()
    assert "inventory.html" in driver.current_url


# ============================================================================
# Data-Driven Login Tests (CSV-driven)
# ============================================================================

CSV_LOGIN_CASES = load_csv_test_data("test_cases.csv")

@pytest.mark.parametrize("case", CSV_LOGIN_CASES, ids=[c["test_id"] for c in CSV_LOGIN_CASES])
def test_login_data_driven(driver, case):
    """Data-driven test executing scenarios loaded from test_data/test_cases.csv."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(case["username"], case["password"])

    if case["expected_status"] == "success":
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()
        assert "inventory.html" in driver.current_url
    else:
        assert login_page.is_error_displayed()
        assert login_page.get_error_message() == case["expected_error"]
