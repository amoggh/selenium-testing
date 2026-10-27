# Software Testing Project Report

## Automated Web Testing with Selenium: Applying Positive, Negative, and Boundary Test Cases to a Login and Cart System

**Course**: Software Testing and Quality Assurance  
**Application Under Test**: SauceDemo E-Commerce ([https://www.saucedemo.com/](https://www.saucedemo.com/))  
**Automation Stack**: Python 3.13, Selenium WebDriver 4.51, pytest 9.1, pytest-html 4.2  
**Date of Submission**: October 2026  

---

## 1. Executive Summary

Software automation testing has become the backbone of modern Continuous Integration and Delivery (CI/CD) pipelines. This project demonstrates the design, implementation, and execution of a robust, modular automated testing suite for an e-commerce platform using Python, Selenium WebDriver 4, and the pytest framework.

Testing was focused on the primary end-user journey: **User Authentication (Login)**, **Product Catalog Browsing**, **Shopping Cart Management**, and **Order Checkout**. By applying **Positive Testing**, **Negative Testing**, and **Boundary Value Analysis (BVA)** across 38 distinct automated test scenarios, the project validates functional correctness, user error handling, input robustness, and boundary stability.

The framework implements the **Page Object Model (POM)** architectural design pattern, completely decoupling test logic from DOM element locators, ensuring maintainability, readability, and resistance to UI modifications. Execution results are captured in an interactive, self-contained HTML report with automated screenshot capture for failure analysis.

---

## 2. Introduction & Problem Statement

### 2.1 Background
Web applications are increasingly dynamic and complex. Manual regression testing of web portals before each software release is time-consuming, expensive, and susceptible to human error. Repetitive tasks such as verifying form validations, cart additions, and authentication flows require automation to provide fast, reliable, and continuous feedback.

### 2.2 Application Under Test (AUT)
The target application is **SauceDemo**, an enterprise e-commerce demo application developed by Sauce Labs. SauceDemo emulates a full retail web platform, featuring:
- Authentication credentials representing diverse user profiles (Standard User, Locked-out User, Problem User, Performance Glitch User).
- An interactive catalog of products with varying descriptions and price tags.
- A shopping cart with real-time badge count updates.
- A multi-step checkout workflow with customer information inputs, tax calculations, and final order confirmations.

### 2.3 Problem Statement
The objective is to develop a complete, reproducible automated testing framework that:
1. Preserves existing working login functionality and extends it into an enterprise POM structure.
2. Formulates test scenarios covering normal operational paths (positive tests).
3. Systematically probes failure modes and validation states (negative tests).
4. Evaluates system boundaries (empty cart, single item, maximum catalog capacity, character limit stress).
5. Provides reliable test execution, detailed HTML logging, and automated failure diagnostic screenshots.

---

## 3. System Architecture & Testing Methodology

### 3.1 Page Object Model (POM) Design Pattern
The framework adopts the industry-standard Page Object Model (POM). In POM:
- Every web page corresponds to a Python class in the `pages/` directory.
- Web element locators (e.g., By.ID, By.CLASS_NAME, By.CSS_SELECTOR) and page-specific actions (e.g., clicking login, typing credentials, adding products) reside inside the Page Object.
- Test files located in `tests/` contain only business assertions and test logic, interacting with the application solely through Page Object methods.

#### Architectural Layers:
1. **BasePage (`pages/base_page.py`)**: Centralizes the WebDriver instance and wraps Selenium commands in explicit waits (`WebDriverWait` + `expected_conditions`), providing safe wrappers for `find()`, `click()`, `type_text()`, and `is_displayed()`.
2. **Specialized Page Objects**:
   - `LoginPage` (`pages/login_page.py`): Handles input of username and password, login button interactions, and error banner extractions.
   - `InventoryPage` (`pages/inventory_page.py`): Handles product discovery, item-specific cart additions/removals, cart badge monitoring, and menu logout.
   - `CartPage` (`pages/cart_page.py`): Manages item verification in the shopping cart, item deletion, and navigation to checkout.
   - `CheckoutPage` (`pages/checkout_page.py`): Handles Step One (Customer Information), Step Two (Summary Overview), and Step Three (Order Dispatch Confirmation).

### 3.2 Pytest Fixture Lifecycle & Session Isolation
Test isolation is a vital requirement in automated testing. If tests share state or browser sessions, a failure in one test can cascade and cause false failures in subsequent tests.
- **`driver` fixture (`conftest.py`)**: Declared with `scope="function"`. A completely new, clean Chrome browser instance is initialized and maximized before each test function starts and reliably terminated (`driver.quit()`) in teardown.
- **`logged_in_driver` fixture**: A composite fixture that invokes `driver`, navigates to the login page, authenticates with standard credentials, verifies successful landing on the inventory page, and provides an authenticated session to dependent tests.

### 3.3 Dynamic Synchronization vs Fixed Delays
To avoid flaky tests, the framework strictly avoids `time.sleep()`. Instead, `WebDriverWait` with explicit conditions (`visibility_of_element_located`, `element_to_be_clickable`, `url_contains`) dynamically waits up to a 10-second threshold. Elements are acted upon the exact millisecond they become ready in the DOM.

### 3.4 Automated Diagnostic Evidence Collection
Using the pytest hook `pytest_runtest_makereport` in `conftest.py`:
- The hook inspects the execution outcome of each test call.
- Upon an assertion failure or uncaught exception, the hook automatically extracts the current browser view and saves a high-resolution PNG file into `screenshots/{test_name}_{timestamp}.png`.
- The screenshot file path is embedded directly into the self-contained HTML execution report generated by `pytest-html`.

---

## 4. Test Case Matrix & Specifications

The test suite contains 38 automated test cases divided into distinct testing methodologies:

### 4.1 Positive Testing Suite (12 Tests)
| Test ID | Test Method | Module | Description / Objective | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| `TC_POS_01` | `test_valid_login` | `test_login.py` | Baseline login test with valid credentials | Redirects to `/inventory.html`, product list visible |
| `TC_POS_02` | `test_positive_login_standard_user` | `test_login.py` | POM-based standard login | Navigates to inventory; header displays "Products" |
| `TC_POS_03` | `test_inventory_visibility_after_login` | `test_login.py` | Product catalog inspection | At least 6 product cards visible with valid names |
| `TC_POS_04` | `test_add_single_product_to_cart` | `test_cart.py` | Adding single item (Backpack) | Cart badge shows "1"; item visible in cart |
| `TC_POS_05` | `test_add_two_different_products` | `test_cart.py` | Adding dual items (Backpack + Bike Light) | Cart badge shows "2"; both items and prices verified |
| `TC_POS_06` | `test_add_multiple_products_cart_badge`| `test_cart.py` | Adding 3 distinct items | Cart badge reflects exact count of 3 |
| `TC_POS_07` | `test_remove_item_from_inventory_page` | `test_cart.py` | Removing item directly from catalog | Button toggles; cart badge disappears |
| `TC_POS_08` | `test_remove_item_from_cart_page` | `test_cart.py` | Removing item inside cart page | Cart count decrements to 1; remaining item intact |
| `TC_POS_09` | `test_continue_shopping_from_cart` | `test_cart.py` | Cart navigation retention | Returns to inventory; cart state preserved |
| `TC_POS_10` | `test_complete_end_to_end_checkout_flow`| `test_checkout.py`| Full purchase lifecycle | Order finishes with "Thank you for your order!" |
| `TC_POS_11` | `test_checkout_cancel_step_one_returns_to_cart`| `test_checkout.py`| Cancel button on checkout form | Navigates back to cart without losing cart items |
| `TC_POS_12` | `test_login_data_driven[TC_LOGIN_01]` | `test_login.py` | CSV-driven positive login | Redirects to inventory page |

### 4.2 Negative Testing Suite (19 Tests)
| Test ID | Test Method | Module | Description / Input Condition | Expected Error / Verification |
| :--- | :--- | :--- | :--- | :--- |
| `TC_NEG_01` | `test_negative_login_invalid_username` | `test_login.py` | Invalid username, valid password | `Epic sadface: Username and password do not match any user in this service` |
| `TC_NEG_02` | `test_negative_login_invalid_password` | `test_login.py` | Valid username, incorrect password | `Epic sadface: Username and password do not match any user in this service` |
| `TC_NEG_03` | `test_negative_login_both_invalid` | `test_login.py` | Both credentials incorrect | `Epic sadface: Username and password do not match any user in this service` |
| `TC_NEG_04` | `test_negative_login_empty_credentials` | `test_login.py` | Blank username and blank password | `Epic sadface: Username is required` |
| `TC_NEG_05` | `test_negative_login_empty_username_populated_password` | `test_login.py` | Blank username, valid password | `Epic sadface: Username is required` |
| `TC_NEG_06` | `test_negative_login_populated_username_empty_password` | `test_login.py` | Valid username, blank password | `Epic sadface: Password is required` |
| `TC_NEG_07` | `test_negative_login_locked_out_user` | `test_login.py` | User account locked out | `Epic sadface: Sorry, this user has been locked out.` |
| `TC_NEG_08` | `test_negative_login_recovery_to_valid_login` | `test_login.py` | Failed attempt followed by valid attempt | Recovers from error state and reaches inventory |
| `TC_NEG_09` | `test_checkout_missing_first_name` | `test_checkout.py` | Checkout form: First name empty | `Error: First Name is required` |
| `TC_NEG_10` | `test_checkout_missing_last_name` | `test_checkout.py` | Checkout form: Last name empty | `Error: Last Name is required` |
| `TC_NEG_11` | `test_checkout_missing_postal_code` | `test_checkout.py` | Checkout form: Postal code empty | `Error: Postal Code is required` |
| `TC_NEG_12` | `test_checkout_all_fields_empty` | `test_checkout.py` | Checkout form: All fields empty | `Error: First Name is required` |
| `TC_NEG_13` | `test_login_data_driven[TC_LOGIN_02]` | `test_login.py` | CSV: Invalid username | Credentials mismatch error |
| `TC_NEG_14` | `test_login_data_driven[TC_LOGIN_03]` | `test_login.py` | CSV: Invalid password | Credentials mismatch error |
| `TC_NEG_15` | `test_login_data_driven[TC_LOGIN_04]` | `test_login.py` | CSV: Both invalid | Credentials mismatch error |
| `TC_NEG_16` | `test_login_data_driven[TC_LOGIN_05]` | `test_login.py` | CSV: Blank credentials | Username is required error |
| `TC_NEG_17` | `test_login_data_driven[TC_LOGIN_06]` | `test_login.py` | CSV: Blank username | Username is required error |
| `TC_NEG_18` | `test_login_data_driven[TC_LOGIN_07]` | `test_login.py` | CSV: Blank password | Password is required error |
| `TC_NEG_19` | `test_login_data_driven[TC_LOGIN_08]` | `test_login.py` | CSV: Locked-out user | Locked out user error |

### 4.3 Boundary Value Analysis & Robustness Suite (7 Tests)
| Test ID | Test Method | Module | Boundary Condition / Stressor | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| `TC_BVA_01` | `test_cart_badge_zero_items_boundary` | `test_boundary.py` | Lower boundary: 0 items in cart | Cart badge element is absent (count = 0) |
| `TC_BVA_02` | `test_cart_badge_single_item_boundary` | `test_boundary.py` | Minimal active boundary: 1 item | Cart badge element appears with count `1` |
| `TC_BVA_03` | `test_cart_badge_maximum_catalog_boundary` | `test_boundary.py` | Upper boundary: All 6 catalog items added | Cart badge correctly reflects `6`; cart displays 6 rows |
| `TC_BVA_04` | `test_cart_add_all_then_remove_all_boundary_transitions` | `test_boundary.py` | Full cycle: 0 -> 6 -> 0 items | Badge cleanly increments to 6, decrements down to 0, disappears |
| `TC_BVA_05` | `test_checkout_input_length_boundary` | `test_boundary.py` | 255-character input strings in checkout form | No application crash or HTTP 500 error; form handles length |
| `TC_BVA_06` | `test_checkout_special_characters_robustness`| `test_boundary.py` | HTML/JS tags & special characters in form | System sanitizes/accepts without DOM break or script execution |
| `TC_BVA_07` | `test_rapid_toggle_add_remove_robustness` | `test_boundary.py` | 5 rapid alternating Add/Remove clicks | Final state strictly matches odd/even parity (badge = 1) |

---

## 5. Execution Results & Metrics

### 5.1 Summary Statistics
- **Total Test Cases Executed**: 38
- **Tests Passed**: 38
- **Tests Failed**: 0
- **Pass Rate**: 100%
- **Execution Platform**: Windows 11 (64-bit), Google Chrome (Version 133+) via Selenium Manager
- **Test Runner**: pytest 9.1.1 with pytest-html 4.2.0

### 5.2 Category Breakdown
| Test Category | Total Tests | Passed | Failed | Success Rate |
| :--- | :---: | :---: | :---: | :---: |
| Positive Testing | 12 | 12 | 0 | 100% |
| Negative Testing | 19 | 19 | 0 | 100% |
| Boundary & Robustness | 7 | 7 | 0 | 100% |
| **Total** | **38** | **38** | **0** | **100%** |

### 5.3 Observations on Application Behavior
1. **Cart Badge DOM Rendering**: The SauceDemo application dynamically injects the `.shopping_cart_badge` element into the DOM only when the item count is greater than zero. When the cart is empty (0 items), the badge element is completely unmounted. Our test implementation handles this via safe visibility checks rather than throwing `NoSuchElementException`.
2. **Error Banner Persistence**: When validation fails on the login page, the error banner persists until closed by the user or refreshed. Tests proved that attempting a valid login immediately overwrites and clears the error state without requiring a manual page refresh.
3. **Form Sanitization and Input Boundaries**: Extreme character lengths (255 characters) and script injection strings (`<script>alert('test')</script>`) were processed safely by the client-side React components without crashing the browser or triggering unhandled script exceptions.

---

## 6. Defect Analysis & Quality Insights

During the development and testing cycle, the following behavioral insights were documented:
- **Locked-Out User Experience**: SauceDemo provides clear feedback (`Epic sadface: Sorry, this user has been locked out.`) preventing brute-force access while informing legitimate users of security lockouts.
- **Sequential Checkout Step Validation**: Checkout validation operates sequentially. If all three fields are empty, SauceDemo displays `Error: First Name is required`. Only after First Name is filled will it check and notify that `Last Name is required`, followed by `Postal Code is required`. Our negative checkout tests accurately model this sequential validation priority.
- **State Preservation**: Navigating away from the cart back to the products catalog via the "Continue Shopping" button preserves all previously selected items and their corresponding button states ("Remove").

---

## 7. Conclusion & Future Scope

### 7.1 Conclusion
The project successfully delivered a complete, enterprise-grade automated testing solution for SauceDemo. By adhering to the Page Object Model, utilizing pytest fixtures, leveraging Selenium 4 Selenium Manager, and implementing thorough positive, negative, and boundary test cases, the framework achieved 100% pass rate across 38 automated scenarios. The resulting test suite guarantees high reliability, complete reproducibility, and clear diagnostic reporting.

### 7.2 Future Scope
1. **CI/CD Pipeline Integration**: Integrating the test suite with GitHub Actions to run headless regression tests automatically on every Git push or pull request.
2. **Cross-Browser Grid Execution**: Running tests concurrently across Chrome, Firefox, and Edge using Selenium Grid or Dockerized Selenium nodes.
3. **API Integration Testing**: Combining Selenium UI tests with backend REST API calls (using the `requests` library) to seed cart data and validate backend database records directly.
4. **Visual Regression Testing**: Incorporating image comparison tools (such as Applitools or open-source pixelmatch) to catch visual layout shifts alongside functional assertions.

---

## 8. References
1. Selenium WebDriver Official Documentation: [https://www.selenium.dev/documentation/](https://www.selenium.dev/documentation/)
2. Pytest Documentation: [https://docs.pytest.org/](https://docs.pytest.org/)
3. Martin Fowler, *Page Object Model Pattern*: [https://martinfowler.com/bliki/PageObject.html](https://martinfowler.com/bliki/PageObject.html)
4. Cem Kaner, Jack Falk, Hung Q. Nguyen, *Testing Computer Software*, 2nd Edition.
5. SauceDemo E-Commerce Demonstration Web Portal: [https://www.saucedemo.com/](https://www.saucedemo.com/)
