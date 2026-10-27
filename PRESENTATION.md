# Project Defense Presentation: Automated Web Testing with Selenium

**Project Title**: Automated Web Testing with Selenium: Applying Positive, Negative, and Boundary Test Cases to a Login and Cart System  
**Course**: Software Testing & Quality Assurance Lab  
**Application Under Test**: SauceDemo E-Commerce Portal ([https://www.saucedemo.com/](https://www.saucedemo.com/))  
**Technologies**: Python 3, Selenium WebDriver 4, pytest, pytest-html  

---

## Slide 1: Title Slide
### Automated Web Testing with Selenium: Applying Positive, Negative, and Boundary Test Cases to a Login and Cart System
- **Presenter**: Software Test Automation Engineer & Student
- **Course**: Software Testing & Quality Assurance Lab
- **Core Technologies**: Python 3.13 | Selenium 4.51 | pytest 9.1 | pytest-html 4.2
- **Target Application**: SauceDemo E-Commerce Platform

> **Speaker Notes**:  
> "Good morning, respected professors and evaluators. Today, I am presenting my automated software testing project titled 'Automated Web Testing with Selenium: Applying Positive, Negative, and Boundary Test Cases to a Login and Cart System'. In this project, I engineered a complete, industry-standard automated testing suite for an e-commerce platform using Python, Selenium WebDriver 4, and pytest, covering functional positive paths, negative error states, and boundary value edge conditions."

---

## Slide 2: Problem Statement & Objectives
### Why Test Automation Matters in E-Commerce
- **The Challenge**: Manual regression testing is slow, expensive, and error-prone across critical checkout funnels.
- **The Goal**: Build a resilient, reproducible test suite that verifies system behavior before every software deployment.
- **Key Objectives**:
  1. Implement the **Page Object Model (POM)** for maximum code maintainability and reusability.
  2. Implement a **Three-Tier Testing Strategy**: Positive, Negative, and Boundary Value Analysis.
  3. Ensure **Test Isolation**: A clean browser instance per test to prevent cascaded failures.
  4. Collect **Automated Evidence**: Generate self-contained HTML test reports and timestamped screenshots on failures.

> **Speaker Notes**:  
> "In e-commerce, any defect in login or checkout directly impacts business revenue. Manual testing cannot keep up with rapid deployment cycles. The goal of this project was to automate the complete user journey—from authentication to cart management and checkout—while demonstrating how automated testing catches defects, enforces input boundaries, and generates verifiable reports."

---

## Slide 3: Application Under Test (SauceDemo)
### An Industry-Standard E-Commerce Testbed
- **Platform**: [SauceDemo](https://www.saucedemo.com/) by Sauce Labs.
- **Key Modules Tested**:
  - **Authentication**: Multi-persona login (Standard User, Locked-out User, Problem User).
  - **Product Catalog**: Dynamic catalog containing 6 items with prices, descriptions, and images.
  - **Shopping Cart**: Real-time badge counter, item additions, item removals, and state preservation.
  - **Order Checkout**: Multi-step transaction workflow (Customer info, overview calculations, order confirmation).

> **Speaker Notes**:  
> "We selected SauceDemo, an enterprise demo application provided by Sauce Labs. It provides real-world UI dynamics, including real-time cart badge counters, form validation errors, and distinct user personas such as standard users and locked-out security accounts."

---

## Slide 4: Testing Methodologies Applied
### Comprehensive Three-Tier Test Strategy
1. **Positive Testing**:
   - Validates that the system operates correctly under expected valid conditions.
   - *Examples*: Standard user login, catalog browsing, adding single/multiple products, completing checkout.
2. **Negative Testing**:
   - Validates that the system gracefully handles invalid inputs and prevents unauthorized actions.
   - *Examples*: Invalid passwords, missing usernames, empty form fields, locked-out accounts, and error recovery.
3. **Boundary Value Analysis (BVA) & Robustness**:
   - Probes system stability at extreme boundaries and stress conditions.
   - *Examples*: Empty cart (0 items), minimal active cart (1 item), catalog maximum (6 items), full cycle (0->6->0), 255-character inputs, and script injection strings.

> **Speaker Notes**:  
> "Rather than merely testing happy paths, our testing strategy incorporates three key testing disciplines: Positive testing to verify business functionality, Negative testing to ensure proper validation prompts and security boundaries, and Boundary Value Analysis to verify that the edges of input domains behave predictably without crashes."

---

## Slide 5: System Architecture – Page Object Model (POM)
### Decoupling Test Logic from UI Implementation
```
  [Test Layer] (test_login.py, test_cart.py, test_boundary.py, test_checkout.py)
        |
        v
  [Page Layer] (LoginPage, InventoryPage, CartPage, CheckoutPage)
        |
        v
  [Base Layer] (BasePage: Explicit Waits, Driver Wrappers)
        |
        v
  [Browser Layer] (Selenium WebDriver & Chrome / Edge)
```
- **BasePage**: Encapsulates common Selenium actions with dynamic `WebDriverWait` (no brittle `sleep` statements).
- **Page Classes**: Contain web element locators (`By.ID`, `By.CLASS_NAME`, `By.CSS_SELECTOR`) and reusable action methods.
- **Maintainability**: If a web selector changes on the website, only a single locator in the page class is updated.

> **Speaker Notes**:  
> "To prevent brittle tests, we implemented the Page Object Model. Notice the clean separation of concerns: tests never interact with low-level Selenium elements directly. Instead, tests call semantic methods on page objects like `cart.proceed_to_checkout()`. If a UI developer updates an ID or class name, we update the selector in just one page file, and all 38 tests continue to function seamlessly."

---

## Slide 6: Pytest Fixtures & Browser Lifecycle
### Test Isolation & Resilient Driver Management
- **Fresh Session per Test**: Function-scoped `driver` fixture creates and tears down a dedicated browser instance for every test.
- **Selenium 4 Selenium Manager**: Zero manual driver downloads; driver binaries are auto-resolved and cached.
- **`logged_in_driver` Fixture**: High-level fixture providing an authenticated session for cart and checkout tests without duplicating login code.
- **Headless Option**: Run tests visibly on desktop or in background headless mode (`--headless`).

> **Speaker Notes**:  
> "A common pitfall in automated testing is shared state between tests. We solved this using pytest fixtures with function scope in conftest.py. Each test receives a clean, maximized browser instance and quits reliably during teardown. In addition, we take full advantage of Selenium 4's built-in Selenium Manager, eliminating hard-coded local ChromeDriver paths."

---

## Slide 7: Positive Test Highlights
### Smooth End-to-End User Experience
- **Login Verification**: Validates successful authentication, URL redirection to `/inventory.html`, and presence of product catalog.
- **Cart Management**:
  - Adds single and multiple distinct items.
  - Verifies cart badge increments (`1`, `2`, `3`).
  - Verifies item names and prices in cart match catalog data.
- **Full Checkout Flow**:
  - Navigates through Step One (Information) -> Step Two (Overview) -> Step Three (Finish).
  - Asserts final dispatch confirmation: `"Thank you for your order!"`.

> **Speaker Notes**:  
> "In our positive test suite, we verified the complete e-commerce funnel. When items are added, the badge updates dynamically; opening the cart confirms the exact item names and prices; proceeding through checkout calculates subtotal and tax; and finishing displays the final confirmation message."

---

## Slide 8: Negative Test Highlights
### Protecting the Application from Invalid States
- **Authentication Validations**:
  - Empty username / Empty password -> Prompts specific required field messages.
  - Invalid credentials -> Displays `Epic sadface: Username and password do not match any user in this service`.
  - Locked-out account -> Displays `Epic sadface: Sorry, this user has been locked out.`.
- **Error State Recovery**: Verifies that a user encountering an error can simply type valid credentials and successfully proceed without refreshing.
- **Checkout Validations**:
  - Validates sequential error prompts for missing First Name, Last Name, and Postal Code.

> **Speaker Notes**:  
> "Negative testing verified that the website protects itself against bad inputs. We validated that informative error messages are displayed for missing fields, incorrect credentials, and locked-out users. We also verified error recovery, proving that the login form does not get permanently stuck in an error state."

---

## Slide 9: Boundary Value & Robustness Testing
### Pushing the Edges of the System
- **Cart Boundary 0 (Lower Boundary)**: When 0 items are added, the badge element is completely absent from the DOM.
- **Cart Boundary 1 (Minimal Active)**: Adding 1 item immediately mounts the badge with value `1`.
- **Cart Boundary 6 (Upper Boundary)**: Adding all 6 items available in the catalog increments the badge to `6`.
- **Full Boundary Cycle (0 -> 6 -> 0)**: Adding all 6 items and sequentially deleting all 6 items cleanly decrements the counter back to an empty cart without DOM remnants.
- **Input Stress Testing**: Submitting 255-character strings and `<script>` injection tags confirmed system stability without browser crashes.
- **Rapid Toggle Robustness**: Rapidly alternating Add/Remove clicks 5 times confirmed consistent final UI state.

> **Speaker Notes**:  
> "Boundary testing is where the most subtle bugs hide. We tested both boundaries of the shopping cart: 0 items where the badge must not exist, 1 item where it must appear, and 6 items which is the maximum catalog size. We also tested the full cycle: 0 to 6 to 0. Finally, we subjected input fields to 255-character strings and script tags, proving the application's stability."

---

## Slide 10: Automated Reporting & Screenshot Evidence
### Real-Time Diagnostics & Auditability
- **Self-Contained HTML Reports**:
  - Generated automatically via `pytest-html` to `reports/report.html`.
  - Consolidates test metadata, execution durations, and step statuses.
- **Automatic Failure Screenshot Hook**:
  - Integrated via `pytest_runtest_makereport` in `conftest.py`.
  - If any test fails, WebDriver instantly takes a screenshot and saves it to `screenshots/{test_name}_{timestamp}.png`.
  - Resilient design: screenshot capture errors never mask the underlying test failure.

> **Speaker Notes**:  
> "Accountability and traceability are critical in QA. Our framework automatically generates an interactive HTML report after every run. More importantly, we built a custom pytest hook that intercepts test failures, captures an immediate screenshot of the browser window, and links it directly to the HTML report for instant debugging."

---

## Slide 11: Execution Results & Metrics
### 100% Pass Rate Across 38 Automated Tests
| Test Category | Total Tests | Passed | Failed | Pass Rate |
| :--- | :---: | :---: | :---: | :---: |
| **Positive Tests** | 12 | 12 | 0 | 100% |
| **Negative Tests** | 19 | 19 | 0 | 100% |
| **Boundary & Robustness Tests** | 7 | 7 | 0 | 100% |
| **Overall Total** | **38** | **38** | **0** | **100%** |

- **Execution Environment**: Windows 11, Chrome, Python 3.13, pytest 9.1
- **Average Duration**: Fully automated regression cycle executed in ~3 minutes.

> **Speaker Notes**:  
> "As shown in this execution summary table, all 38 automated test cases passed successfully, yielding a 100% pass rate. This includes 12 positive tests, 19 negative tests (incorporating data-driven scenarios from CSV), and 7 boundary and robustness scenarios."

---

## Slide 12: Summary & Conclusion
### Key Takeaways & Future Enhancements
- **Key Takeaways**:
  - Automated testing with Selenium and pytest drastically reduces regression cycle time.
  - Page Object Model provides a clean, enterprise-ready separation of concerns.
  - Explicit waits eliminate flaky tests and ensure deterministic test results.
- **Future Scope**:
  - Integrate with GitHub Actions for automated pull-request validation.
  - Expand cross-browser testing across Firefox and Edge on Selenium Grid.
  - Incorporate API-level test seeding to accelerate setup stages.

**Thank you! Questions and discussions are welcome.**

> **Speaker Notes**:  
> "In conclusion, this project demonstrated how a structured, scalable Selenium testing framework can be built from the ground up, starting from a single working test and evolving into an enterprise-grade automated testing solution with 38 test cases. Thank you for your time, and I am now ready to answer any questions."
