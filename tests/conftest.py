import pytest
from selenium import webdriver
from src.config import BASE_URL, STANDARD_USER, STANDARD_PASSWORD
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage
from src.pages.inventory_page import InventoryPage
from src.pages.login_page import LoginPage
from src.pages.nav_page import NavPage
from src.pages.pdp_page import PDPPage


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="edge", help="Browser: chrome or edge"
    )
    parser.addoption(
        "--base-url", action="store", default=BASE_URL, help="Application base URL"
    )


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getoption("base_url")


@pytest.fixture(scope="module")
def driver(pytestconfig, base_url):
    browser_name = pytestconfig.getoption("browser").lower()

    if browser_name == "chrome":
        _driver = webdriver.Chrome()
    elif browser_name == "edge":
        _driver = webdriver.Edge()
    else:
        raise pytest.UsageError(
            f"--browser '{browser_name}' is not supported. Use 'chrome' or 'edge'."
        )

    _driver.maximize_window()
    _driver.get(base_url)

    yield _driver
    _driver.quit()


# ------------------------------------------------------------------
# Page object fixtures
# ------------------------------------------------------------------

@pytest.fixture(scope="module")
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture(scope="module")
def inventory_page(driver):
    return InventoryPage(driver)


@pytest.fixture(scope="module")
def cart_page(driver):
    return CartPage(driver)


@pytest.fixture(scope="module")
def pdp_page(driver):
    return PDPPage(driver)


@pytest.fixture(scope="module")
def checkout_page(driver):
    return CheckoutPage(driver)


@pytest.fixture(scope="module")
def nav_page(driver):
    return NavPage(driver)


@pytest.fixture(scope="function")
def app_login(login_page):
    """Log in before a test and log out cleanly after."""
    login_page.login(username=STANDARD_USER, password=STANDARD_PASSWORD)
    yield
    login_page.log_out()


@pytest.fixture(scope="function")
def clean_cart(cart_page, app_login):
    """Log in and guarantee an empty cart before and after the test."""
    cart_page.go_to_cart()
    cart_page.clear_cart()
    yield
    cart_page.go_to_cart()
    cart_page.clear_cart()