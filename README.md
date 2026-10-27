# Automated Web Testing with Selenium: Applying Positive, Negative, and Boundary Test Cases to a Login and Cart System

An end-to-end automated software testing framework developed with **Python 3**, **Selenium WebDriver 4**, **pytest**, and **pytest-html**, targeting the [SauceDemo E-Commerce Application](https://www.saucedemo.com/).

This project was built for a college-level Software Testing and Quality Assurance course to demonstrate industry-standard test automation techniques, including the **Page Object Model (POM)** architecture, **Pytest Fixtures**, **Data-Driven Testing (CSV)**, **Resilient Failure Screenshot Capture**, and comprehensive test categorization across **Positive**, **Negative**, and **Boundary Value** methodologies.

---

## Table of Contents
1. [Project Overview & Objectives](#project-overview--objectives)
2. [Testing Methodologies](#testing-methodologies)
3. [Architecture & Design (Page Object Model)](#architecture--design-page-object-model)
4. [Project Directory Structure](#project-directory-structure)
5. [Prerequisites & Environment Setup](#prerequisites--environment-setup)
6. [How to Run Tests](#how-to-run-tests)
7. [Test Suite Breakdown & Test Matrix](#test-suite-breakdown--test-matrix)
8. [Automated Reporting & Screenshot Capture](#automated-reporting--screenshot-capture)
9. [Viva & Oral Examination Preparation Guide](#viva--oral-examination-preparation-guide)

---

## Project Overview & Objectives

In modern web development, continuous regression testing is essential to guarantee user experience and platform reliability. This project builds an enterprise-grade automated testing suite that validates the primary revenue funnel of an e-commerce website: **Authentication (Login)**, **Product Catalog Browsing**, **Shopping Cart Management**, and **Order Checkout**.

### Key Objectives:
- **Reproducible Execution**: Seamless one-command test runs using `pytest` without manual driver downloads (powered by Selenium Manager).
- **Separation of Concerns**: Decoupling web element locators and page interactions from test assertions via the **Page Object Model (POM)**.
- **Three-Tier Testing Approach**:
  1. **Positive Testing**: Validating expected workflows under normal, valid inputs.
  2. **Negative Testing**: Validating error handling, input validation alerts, and recovery flows under invalid inputs.
  3. **Boundary Value & Robustness Testing**: Stress-testing capacity limits (0 to 6 items in cart), extreme string lengths (250+ characters), special characters, and rapid UI actions.
- **Automated Evidence Collection**: Generating self-contained HTML execution reports and automatically capturing high-resolution browser screenshots upon any test failure.

---

## Testing Methodologies

### 1. Positive Testing
Positive testing validates that the software functions as expected when provided with valid data and standard user actions.
- **Login**: `standard_user` authenticates successfully and reaches `/inventory.html`.
- **Product Catalog**: Verifies visibility of 6 product cards with prices, descriptions, and images.
- **Shopping Cart**: Verifies adding single, dual, and multiple items, badge count increments, and cart retention during navigation.
- **Checkout Flow**: Verifies end-to-end order placement resulting in `"Thank you for your order!"`.

### 2. Negative Testing
Negative testing tests the application’s response to invalid inputs, missing data, and unauthorized access attempts.
- **Authentication Validations**:
  - Invalid username with valid password.
  - Valid username with invalid password.
  - Both username and password invalid.
  - Empty username with populated password (`Epic sadface: Username is required`).
  - Populated username with empty password (`Epic sadface: Password is required`).
  - Completely empty credentials.
  - Locked-out account (`locked_out_user` -> `Epic sadface: Sorry, this user has been locked out.`).
  - Error state recovery (recovering from an invalid login to a valid login).
- **Checkout Information Validations**:
  - Missing first name (`Error: First Name is required`).
  - Missing last name (`Error: Last Name is required`).
  - Missing postal code (`Error: Postal Code is required`).
  - All fields blank.

### 3. Boundary Value Analysis (BVA) & Robustness Testing
Boundary testing examines system behavior at the edges of permissible input domains:
- **Cart Badge Min/Max Capacity**:
  - **Lower Boundary (0 items)**: The cart badge element is absent from the DOM / count = 0.
  - **Minimal Active Boundary (1 item)**: The badge element appears immediately with count `1`.
  - **Upper Catalog Boundary (6 items)**: All available items added, badge correctly displays `6`.
  - **Boundary Cycle (0 -> 6 -> 0)**: Full addition followed by full deletion, verifying badge decrements and disappears at 0.
- **Input Length Boundary**: 255-character strings input into checkout fields to verify absence of buffer overflows or unhandled UI crashes.
- **Special Characters & Injection Robustness**: Form validation handling for symbols (`!@#$%^&*()_+{}|:"<>?~`) and HTML/JS script strings (`<script>alert('test')</script>`).
- **Rapid Toggle Robustness**: Repeated fast alternating Add/Remove actions to verify DOM and state consistency.

---

## Architecture & Design (Page Object Model)

The framework is structured using the **Page Object Model (POM)** pattern. Each web page is represented by a Python class that encapsulates the page's HTML element locators and behavioral actions. Tests interact exclusively with Page Objects and assert expected outcomes.

```
                  +--------------------------+
                  |       Test Layer         |
                  |  (test_*.py with pytest) |
                  +------------+-------------+
                               |
                               v
                  +--------------------------+
                  |     Page Object Layer    |
                  | (login, inventory, cart) |
                  +------------+-------------+
                               |
                               v
                  +--------------------------+
                  |        BasePage          |
                  |  (Explicit Waits / POM)  |
                  +------------+-------------+
                               |
                               v
                  +--------------------------+
                  |    Selenium WebDriver    |
                  |     (Chrome / Edge)      |
                  +--------------------------+
```

### Advantages of this Architecture:
1. **Maintainability**: If a web element's locator changes, only the corresponding Page Object class requires updating. Tests remain unchanged.
2. **Reusability**: Page interaction methods (e.g., `login()`, `add_item_to_cart_by_name()`, `proceed_to_checkout()`) are reused across dozens of test cases.
3. **Readability**: Test files read like business logic specifications rather than low-level Selenium code.
4. **Explicit Waits**: All element interactions utilize `WebDriverWait` with `expected_conditions`, eliminating brittle `time.sleep()` statements.

---

## Project Directory Structure

```
selenium-login-cart-testing/
│
├── tests/                           # Test suite directory
│   ├── test_login.py                # Positive, negative, baseline, and CSV-driven login tests
│   ├── test_cart.py                 # Positive shopping cart operations and navigation tests
│   ├── test_boundary.py             # Boundary value analysis (0, 1, 6 items) and robustness tests
│   └── test_checkout.py             # Positive checkout flow and negative validation tests
│
├── pages/                           # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py                 # Base page with common explicit waits & driver actions
│   ├── login_page.py                # Login page locators and interaction methods
│   ├── inventory_page.py            # Inventory catalog, item selection, and badge methods
│   ├── cart_page.py                 # Cart page review, item removal, and checkout trigger
│   └── checkout_page.py             # Checkout information, overview, and confirmation methods
│
├── utils/                           # Shared utilities and configurations
│   ├── __init__.py
│   └── helpers.py                   # URLs, credentials, error message constants, CSV reader
│
├── test_data/                       # External test datasets
│   └── test_cases.csv               # Data-driven test scenarios for authentication
│
├── reports/                         # Test execution reports
│   ├── .gitkeep
│   └── report.html                  # Generated self-contained HTML report
│
├── screenshots/                     # Automatic test failure screenshots
│   ├── .gitkeep
│   └── *.png                        # Timestamped failure captures
│
├── conftest.py                      # Reusable pytest fixtures, driver lifecycle, screenshot hooks
├── pytest.ini                       # Pytest configuration, CLI defaults, and markers
├── requirements.txt                 # Project dependencies
├── .gitignore                       # Git exclusion rules
├── README.md                        # Framework guide & viva documentation
├── PROJECT_REPORT.md                # Formal academic software testing report
└── PRESENTATION.md                  # Project defense slide deck outline
```

---

## Prerequisites & Environment Setup

### 1. Prerequisites
- **Python**: Version 3.10, 3.11, 3.12, or 3.13 installed.
- **Google Chrome**: Installed on the machine (Selenium 4 Manager automatically matches the appropriate driver).

### 2. Virtual Environment Setup
Open a terminal in the project directory:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Windows (CMD):
.\.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

---

## How to Run Tests

### 1. Execute All Tests
Run the entire 38-test suite with detailed output and HTML report generation:
```bash
pytest -v
```

### 2. Run Tests by Category (Pytest Markers)
The test suite utilizes custom markers declared in `pytest.ini`:

```bash
# Run only Positive tests
pytest -m positive -v

# Run only Negative tests
pytest -m negative -v

# Run only Boundary and Robustness tests
pytest -m boundary -v

# Run critical Smoke tests
pytest -m smoke -v

# Run by Functional Area
pytest -m login -v
pytest -m cart -v
pytest -m checkout -v
```

### 3. Run Specific Test Files
```bash
# Run Login suite
pytest tests/test_login.py -v

# Run Cart suite
pytest tests/test_cart.py -v

# Run Boundary suite
pytest tests/test_boundary.py -v

# Run Checkout suite
pytest tests/test_checkout.py -v
```

### 4. Run in Headless Mode
To run without opening visible browser windows (ideal for CI/CD or background runs):
```bash
pytest --headless -v
```

### 5. Multi-Browser Execution
The framework supports configurable browser selection via CLI flag or environment variable:
```bash
# Chrome (default)
pytest --browser chrome -v

# Microsoft Edge
pytest --browser edge -v

# Mozilla Firefox
pytest --browser firefox -v
```

---

## Test Suite Breakdown & Test Matrix

| Test Module | Test Name | Category | Scope / Objective |
| :--- | :--- | :--- | :--- |
| `test_login.py` | `test_valid_login` | Positive | Baseline working login test verifying standard credentials. |
| `test_login.py` | `test_positive_login_standard_user` | Positive / Smoke | Verifies login navigation to inventory via Page Object Model. |
| `test_login.py` | `test_inventory_visibility_after_login` | Positive | Asserts inventory catalog elements are visible post-login. |
| `test_login.py` | `test_negative_login_invalid_username` | Negative | Asserts error message on unrecognized username. |
| `test_login.py` | `test_negative_login_invalid_password` | Negative | Asserts error message on incorrect password. |
| `test_login.py` | `test_negative_login_both_invalid` | Negative | Asserts error message when both credentials are wrong. |
| `test_login.py` | `test_negative_login_empty_credentials` | Negative | Asserts validation prompt when both fields are empty. |
| `test_login.py` | `test_negative_login_empty_username_populated_password` | Negative | Asserts prompt when username is blank. |
| `test_login.py` | `test_negative_login_populated_username_empty_password` | Negative | Asserts prompt when password is blank. |
| `test_login.py` | `test_negative_login_locked_out_user` | Negative | Asserts error message for locked out user account. |
| `test_login.py` | `test_negative_login_recovery_to_valid_login` | Negative / State | Asserts user can recover from error state and log in. |
| `test_login.py` | `test_login_data_driven[TC_LOGIN_01..08]` | Data-Driven | 8 parameterized test runs driven directly from CSV file. |
| `test_cart.py` | `test_add_single_product_to_cart` | Positive / Smoke | Adds 1 item, verifies badge count = 1 and item present in cart. |
| `test_cart.py` | `test_add_two_different_products` | Positive | Adds 2 different items, verifies badge = 2 and prices match. |
| `test_cart.py` | `test_add_multiple_products_cart_badge` | Positive | Adds 3 items and verifies badge count increment. |
| `test_cart.py` | `test_remove_item_from_inventory_page` | Positive | Removes item directly from inventory page; badge clears. |
| `test_cart.py` | `test_remove_item_from_cart_page` | Positive | Removes item from inside cart; verifies cart updates. |
| `test_cart.py` | `test_continue_shopping_from_cart` | Positive | Verifies navigation back to inventory retains cart items. |
| `test_boundary.py` | `test_cart_badge_zero_items_boundary` | Boundary (0) | Asserts cart badge is not displayed when 0 items added. |
| `test_boundary.py` | `test_cart_badge_single_item_boundary` | Boundary (1) | Asserts boundary transition from 0 to 1 displays badge. |
| `test_boundary.py` | `test_cart_badge_maximum_catalog_boundary` | Boundary (6) | Adds all 6 catalog items; asserts badge count = 6. |
| `test_boundary.py` | `test_cart_add_all_then_remove_all_boundary_transitions` | Boundary Cycle | Adds all 6 items then removes all 6 items; asserts 0 badge. |
| `test_boundary.py` | `test_checkout_input_length_boundary` | Robustness | Enters 255-character input strings in checkout fields. |
| `test_boundary.py` | `test_checkout_special_characters_robustness` | Robustness | Tests script tags and special symbols in form fields. |
| `test_boundary.py` | `test_rapid_toggle_add_remove_robustness` | Robustness | Rapidly toggles item 5 times; asserts consistent final state. |
| `test_checkout.py` | `test_complete_end_to_end_checkout_flow` | Positive / Smoke | Completes entire purchase workflow from cart to confirmation. |
| `test_checkout.py` | `test_checkout_missing_first_name` | Negative | Asserts error: 'Error: First Name is required'. |
| `test_checkout.py` | `test_checkout_missing_last_name` | Negative | Asserts error: 'Error: Last Name is required'. |
| `test_checkout.py` | `test_checkout_missing_postal_code` | Negative | Asserts error: 'Error: Postal Code is required'. |
| `test_checkout.py` | `test_checkout_all_fields_empty` | Negative | Asserts error when all checkout fields are empty. |
| `test_checkout.py` | `test_checkout_cancel_step_one_returns_to_cart` | Positive | Canceling checkout returns user back to cart. |

---

## Automated Reporting & Screenshot Capture

### 1. Self-Contained HTML Reports
By default (`pytest.ini`), every test run automatically compiles an interactive, self-contained report to `reports/report.html`.
- Displays total tests executed, passed, failed, duration, and environment metadata.
- Open `reports/report.html` in any web browser to view the test report.

### 2. Automatic Screenshot on Failure Hook
In `conftest.py`, the `pytest_runtest_makereport` hook monitors test execution:
- If an assertion fails or an exception occurs, the active WebDriver instance captures a full-window screenshot.
- Files are saved to `screenshots/` using unique names: `{test_name}_{timestamp}.png`.
- The screenshot is automatically linked into the pytest-html report.
- The hook is wrapped in defensive try/except handling to ensure screenshot issues never obscure the original test failure.

---

## Viva & Oral Examination Preparation Guide

Use this section to prepare for college project defense, oral exams, and technical viva questions.

### Q1: What is the Page Object Model (POM) and why did you use it?
**Answer**: Page Object Model is an architectural design pattern in test automation where each web page is represented as a dedicated class. Locators and interaction methods are encapsulated within the page class, while test classes focus solely on test logic and assertions. This provides two key benefits:
1. **High Maintainability**: If an element's selector changes, we update it in one place (the Page class) without altering multiple test files.
2. **Reusability and Readability**: Common actions like login or adding products can be called across multiple tests with clean, self-documenting code.

### Q2: What is the difference between Positive, Negative, and Boundary Value Testing?
**Answer**:
- **Positive Testing**: Verifies that the system behaves correctly with valid inputs and normal user paths (e.g., standard login, valid checkout).
- **Negative Testing**: Verifies that the system appropriately handles invalid inputs, detects errors, and displays validation messages without crashing (e.g., wrong password, blank fields).
- **Boundary Value Testing**: Tests the edges of acceptable input ranges where software bugs frequently cluster (e.g., 0 items in cart vs. 1 item vs. maximum 6 items; 255-character input strings).

### Q3: Why did you use Explicit Waits instead of `time.sleep()`?
**Answer**: `time.sleep()` halts the Python process unconditionally for a fixed duration, regardless of whether the element loaded faster or slower. This slows down test execution and can cause random failures if the network lags.
**Explicit Waits** (`WebDriverWait` with `expected_conditions`) poll the DOM dynamically until the specific condition is satisfied (e.g., element visible, clickable, or URL changed) or times out. This makes tests fast, deterministic, and resilient.

### Q4: How does driver management work in Selenium 4 without downloading ChromeDriver?
**Answer**: Selenium 4 includes **Selenium Manager**, a built-in automated driver management tool. When a WebDriver instance (`webdriver.Chrome()`) is created, Selenium Manager automatically inspects the locally installed browser version, downloads the compatible driver binary, caches it, and configures the path seamlessly.

### Q5: What is the role of `conftest.py` in pytest?
**Answer**: `conftest.py` is a special pytest configuration file recognized automatically without explicit imports. It serves as a centralized hub for shared fixtures (like browser initialization and cleanup), command-line option hooks (`pytest_addoption`), and test reporting hooks (`pytest_runtest_makereport`).

### Q6: What is a fixture in pytest and what scopes can it have?
**Answer**: A fixture is a reusable function decorated with `@pytest.fixture` that sets up preconditions (like initializing a browser) and tears down resources (like calling `driver.quit()`) using the `yield` statement. Fixtures can have different scopes:
- `function` (default): Runs before and after each test function (provides complete test isolation).
- `class`: Runs once per test class.
- `module`: Runs once per test file.
- `session`: Runs once across the entire test execution session.

### Q7: How does your framework capture screenshots when a test fails?
**Answer**: We implement the `pytest_runtest_makereport` hook in `conftest.py`. When a test phase completes, the hook inspects `report.when == "call"` and `report.failed`. If the test failed, it retrieves the WebDriver instance, calls `driver.save_screenshot()`, saves the image to `screenshots/` with a timestamped filename, and attaches it to the pytest-html report.

### Q8: What is Data-Driven Testing and how is it used here?
**Answer**: Data-Driven Testing separates test logic from test data. Instead of hardcoding credentials in test functions, scenarios are defined in an external source (`test_data/test_cases.csv`). Using `@pytest.mark.parametrize`, pytest automatically executes the same test logic multiple times, once for each row in the CSV dataset.

### Q9: What locator strategies does Selenium offer, and which did you prioritize?
**Answer**: Selenium supports `ID`, `NAME`, `CLASS_NAME`, `CSS_SELECTOR`, `XPATH`, `TAG_NAME`, and `LINK_TEXT`. We prioritized:
1. `ID` and `CSS_SELECTOR` with data attributes (`data-test`): Fast, reliable, and least prone to layout changes.
2. `CLASS_NAME`: Used for repeated list items and status badges.
3. Complex absolute XPaths were avoided because they are brittle and break easily with UI layout modifications.

### Q10: How do you run tests in headless mode and why is it useful?
**Answer**: Headless mode runs the browser in memory without rendering the visual graphical user interface. We configured a `--headless` CLI flag in `conftest.py` which passes `--headless=new` to Chrome Options. Headless mode executes significantly faster, uses fewer system resources, and is required when running tests on CI/CD build servers (like GitHub Actions) that lack a display server.
