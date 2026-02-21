# SauceDemo Selenium Pytest Automation 🧪

A professional, maintainable UI automation framework for [SauceDemo](https://www.saucedemo.com) built with **Python**, **Selenium WebDriver**, and **Pytest** following the **Page Object Model (POM)** design pattern.

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Page Objects](#page-objects)
- [Test Suites](#test-suites)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Running Tests](#running-tests)
  - [Run All Tests](#run-all-tests)
  - [Run by Marker](#run-by-marker)
  - [Run by Browser](#run-by-browser)
  - [Run a Specific File](#run-a-specific-file)
- [Test Markers](#test-markers)
- [Framework Design](#framework-design)
  - [BasePage](#basepage)
  - [Fixtures & State Management](#fixtures--state-management)
  - [Screenshots on Failure](#screenshots-on-failure)
  - [Explicit Waits](#explicit-waits)
- [Configuration & Credentials](#configuration--credentials)

---

## About the Project

This repository contains an end-to-end UI automation framework for the SauceDemo e-commerce web application. It was developed as a portfolio/learning project to demonstrate professional-grade test automation practices including:

- Clean separation of page logic and test logic via the **Page Object Model**
- Reliable element interactions with **explicit waits** throughout — no `time.sleep()` calls
- Consistent, predictable test isolation using **Pytest fixtures** for login/logout and cart cleanup
- Centralized configuration for credentials and URLs via **environment variables**
- Timestamped **failure screenshots** saved automatically on errors
- Scalable test organisation with **Pytest markers** for targeted test execution

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11+ | Primary language |
| Selenium WebDriver 4.27 | Browser automation |
| Pytest 8.3 | Test runner and fixture framework |
| python-dotenv 1.0 | Environment variable management |

---

## Project Structure

```
saucedemo-selenium-pytest/
│
├── src/
│   ├── config.py                  # Centralised URLs and credentials
│   ├── pages/
│   │   ├── base_page.py           # Shared WebDriver helpers (click, type, waits)
│   │   ├── login_page.py          # Login / logout actions
│   │   ├── inventory_page.py      # Product listing page
│   │   ├── pdp_page.py            # Product Details Page
│   │   ├── cart_page.py           # Shopping cart page
│   │   ├── checkout_page.py       # Checkout step one, overview, confirmation
│   │   └── nav_page.py            # Hamburger menu / sidebar navigation
│   └── utils/
│       └── waits.py               # Explicit wait helper functions
│
├── tests/
│   ├── conftest.py                # Pytest fixtures (driver, page objects, state)
│   ├── test_login.py              # Login validation tests (AUTH-001 – 007)
│   ├── test_inventory_ui.py       # Inventory page UI tests (INV-001 – 008)
│   ├── test_pdp.py                # Product Details Page tests (PDP-001 – 005)
│   ├── test_cart.py               # Cart page tests (CART-001 – 008)
│   ├── test_cart_badge.py         # Cart badge & state tests (CART-001 – 006)
│   ├── test_checkout.py           # Checkout flow tests (CHK-001 – 006)
│   └── test_navigation.py         # Navigation & menu tests (NAV-001 – 006)
│
├── screenshots/                   # Auto-created; timestamped failure screenshots
├── .env                           # Local credentials (not committed)
├── .gitignore
├── pytest.ini                     # Pytest configuration and marker definitions
├── requirements.txt               # Pinned dependencies
└── README.md
```

---

## Page Objects

Each page object encapsulates all locators and interactions for a specific page. All inherit from `BasePage` which provides shared WebDriver helpers.

| Page Object | URL | Responsibility |
|---|---|---|
| `LoginPage` | `/` | Login, logout, error message validation |
| `InventoryPage` | `/inventory.html` | Product listing, filtering, add/remove to cart |
| `PDPPage` | `/inventory-item.html?id=X` | Product details, add/remove from PDP |
| `CartPage` | `/cart.html` | View cart, remove items, proceed to checkout |
| `CheckoutPage` | `/checkout-step-one.html` | Step one form, overview totals, confirmation |
| `NavPage` | (overlay) | Hamburger menu — all items, logout, reset, about |

---

## Test Suites

### 🔐 Login (`test_login.py`)

| Test ID | Description | Markers |
|---|---|---|
| AUTH-001 | Valid credentials → lands on inventory | smoke, regression |
| AUTH-002 | Invalid credentials → error message | negative, regression |
| AUTH-003 | Direct URL bypass without login → error | regression |
| AUTH-004 | Logout redirects to login page | regression |
| AUTH-005 | Locked out user → error message | negative, regression |
| AUTH-006 | Empty credentials → validation error | negative, regression |
| AUTH-007 | Valid username + empty password → error | negative, regression |

### 🛍️ Inventory UI (`test_inventory_ui.py`)

| Test ID | Description | Markers |
|---|---|---|
| INV-001 | Core UI elements present (logo, title, cart, filter) | smoke, regression, ui |
| INV-002 | 6 products with images, names, prices; add/cart toggle | smoke, regression, ui |
| INV-003 | Default filter is Name (A to Z) | smoke, regression, ui |
| INV-004 | All 4 filter options select correct label (parametrized) | regression, sorting |
| INV-005 | Name A→Z sort order is alphabetically correct | regression, sorting |
| INV-006 | Name Z→A sort order is reverse alphabetical | regression, sorting |
| INV-007 | Price low→high sort order is ascending | regression, sorting |
| INV-008 | Price high→low sort order is descending | regression, sorting |

### 📄 Product Details Page (`test_pdp.py`)

| Test ID | Description | Markers |
|---|---|---|
| PDP-001 | PDP shows correct name, price, description, image | regression, pdp |
| PDP-002 | Back button returns to inventory | regression, pdp |
| PDP-003 | Add from PDP updates badge and inventory tile state | regression, pdp |
| PDP-004 | PDP price and name match inventory tile | regression, pdp |
| PDP-005a | Direct URL with valid ID renders correct product | regression, pdp |
| PDP-005b | Direct URL with invalid ID handled gracefully | regression, pdp |

### 🛒 Cart (`test_cart.py` + `test_cart_badge.py`)

| Test ID | Description | Markers |
|---|---|---|
| CART-001 | Core cart UI elements present | smoke, regression, cart, ui |
| CART-002 | Multiple items added to cart | smoke, regression, cart |
| CART-003 | Item removed from cart; absent from cart view | smoke, regression, cart |
| CART-004 | Cart items persist across navigation | regression, cart |
| CART-005 | Cart items persist after page refresh | regression, cart |
| CART-006 | Empty cart shows 0 items | regression, cart |
| CART-007 | Cart item count matches items added | regression, cart |
| CART-008 | Continue Shopping returns to inventory | regression, cart |
| CART-B001 | Badge count reflects distinct items added | smoke, regression, cart |
| CART-B002 | Cart page shows correct item names and prices | smoke, regression, cart |
| CART-B003 | Remove updates badge and tile button state | regression, cart |
| CART-B004 | Badge persists after inventory page refresh | regression, cart |
| CART-B005 | PDP + inventory adds de-duplicate correctly | regression, cart |
| CART-B006 | State survives inventory → PDP → cart → back loop | regression, cart |

### 💳 Checkout (`test_checkout.py`)

| Test ID | Description | Markers |
|---|---|---|
| CHK-001 | Empty fields on Step One show validation error | smoke, negative, regression, checkout |
| CHK-002 | Step One → Overview shows subtotal, tax, total | smoke, regression, checkout |
| CHK-003 | Finish → confirmation → Back Home; cart cleared | smoke, regression, checkout |
| CHK-004 | Cancel from Overview returns to cart with items | regression, checkout |
| CHK-005 | Subtotal = sum of item prices; total = subtotal + tax | regression, checkout |
| CHK-006 | Inventory buttons reset to "Add to cart" after checkout | regression, checkout |

### 🍔 Navigation (`test_navigation.py`)

| Test ID | Description | Markers |
|---|---|---|
| NAV-001 | Burger menu opens and closes | smoke, regression, nav |
| NAV-002 | All Items returns to inventory | smoke, regression, nav |
| NAV-002b | Logout redirects to login page | smoke, regression, nav |
| NAV-003 | Reset App State clears cart badge and buttons | smoke, regression, nav |
| NAV-004 | About link href points to SauceLabs | regression, nav |
| NAV-005 | Browser back/forward stays on valid pages | regression, nav |
| NAV-006 | Rapid menu toggling doesn't freeze menu | regression, nav |

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Google Chrome **or** Microsoft Edge installed
- Matching ChromeDriver or EdgeDriver on your `PATH` (or use Selenium Manager which handles this automatically with Selenium 4.6+)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/navneetkrishna/saucedemo-selenium-pytest.git
cd saucedemo-selenium-pytest

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

Credentials and the base URL are loaded from environment variables. Create a `.env` file in the project root:

```env
BASE_URL=https://www.saucedemo.com
STANDARD_USER=standard_user
LOCKED_OUT_USER=locked_out_user
PROBLEM_USER=problem_user
STANDARD_PASSWORD=secret_sauce
```

The framework falls back to the SauceDemo defaults if no `.env` file is present, so the project runs out of the box without any configuration.

> ⚠️ `.env` is listed in `.gitignore` and should never be committed.

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run by Marker

```bash
# Smoke tests only
pytest -m smoke

# Regression tests only
pytest -m regression

# Negative / error-path tests
pytest -m negative

# Specific feature areas
pytest -m login_validation
pytest -m cart
pytest -m checkout
pytest -m pdp
pytest -m nav
pytest -m sorting
```

### Run by Browser

The default browser is **Edge**. Pass `--browser chrome` to use Chrome.

```bash
pytest --browser chrome
pytest --browser edge
```

### Run a Specific File

```bash
pytest tests/test_login.py
pytest tests/test_checkout.py
pytest tests/test_pdp.py
```

### Combine Options

```bash
# Smoke tests in Chrome with verbose output
pytest -m smoke --browser chrome -v

# Single test by name
pytest tests/test_checkout.py::TestCheckout::test_chk_005_subtotal_equals_sum_of_item_prices
```

---

## Test Markers

Defined in `pytest.ini`:

| Marker | Description |
|---|---|
| `smoke` | Critical path — run first and fastest |
| `regression` | Full regression suite |
| `negative` | Invalid input and error-handling scenarios |
| `ui` | Visual / structural UI validation |
| `login_validation` | Login and authentication scenarios |
| `inventory_ui` | Inventory page UI scenarios |
| `pdp` | Product Details Page scenarios |
| `cart` | Shopping cart scenarios |
| `checkout` | Checkout flow scenarios |
| `nav` | Hamburger menu and navigation scenarios |
| `sorting` | Product sort/filter scenarios |

---

## Framework Design

### BasePage

`src/pages/base_page.py` is the foundation every page object inherits from. It provides:

- **`click(by, selector)`** — waits for element to be clickable; handles `StaleElementReferenceException` with one automatic retry
- **`type(by, selector, text)`** — clears and types into a field after waiting for visibility
- **`ele_text(by, selector)`** — waits for visibility and returns `.text`
- **`ele_visible(by, selector)`** — returns element or `False` (never raises)
- **`ele_exists(selector)`** — immediate DOM check; returns element or `False`
- **`elements_exists(selector)`** — returns a list or `[]` (never raises)
- **`dropdowns(selector)`** — returns a `Select` object for `<select>` elements
- **`navigate_url(url)`** — direct URL navigation

All methods that can fail save a **timestamped screenshot** to `screenshots/` before raising, making failures self-documenting.

### Fixtures & State Management

`tests/conftest.py` provides three levels of test state:

```
driver (module scope)
└── login_page, inventory_page, cart_page, pdp_page, checkout_page, nav_page (module scope)
    └── app_login (function scope) — logs in before, logs out after each test
        └── clean_cart (function scope) — clears cart before and after each test
```

Tests that interact with the cart use `clean_cart` to guarantee they start and end with an empty cart. Tests that only need a logged-in session use `app_login`. This prevents state from one test leaking into the next.

### Screenshots on Failure

Any `BasePage` method that raises stores a screenshot automatically:

```
screenshots/
  fail_login-button_20250222_143201_482910.png
  fail_inventory_item_20250222_143415_119843.png
```

The timestamp format is `YYYYMMDD_HHMMSS_microseconds` ensuring no screenshot is ever overwritten.

### Explicit Waits

All waits live in `src/utils/waits.py` and use `WebDriverWait` + Selenium expected conditions. The default timeout is **10 seconds**. There are no `time.sleep()` calls anywhere in the framework.

```python
wait_visible(driver, locator)       # Visibility of element
wait_clickable(driver, locator)     # Element to be clickable
wait_all_visible(driver, locator)   # Visibility of all elements
presence_located(driver, locator)   # Presence in DOM
```

---

## Configuration & Credentials

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://www.saucedemo.com` | Base URL for the application |
| `STANDARD_USER` | `standard_user` | Default test user |
| `LOCKED_OUT_USER` | `locked_out_user` | User for locked-out negative tests |
| `PROBLEM_USER` | `problem_user` | User with UI anomalies |
| `STANDARD_PASSWORD` | `secret_sauce` | Shared password for all test users |

All values are loaded via `src/config.py` using `python-dotenv`. Override any value by setting it in your `.env` file or as a shell environment variable.
