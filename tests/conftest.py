import pytest
from selenium import webdriver
from src.pages.login_page import LoginPage
from src.pages.home_page import HomePage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="edge", help="Browser: chrome or edge")
    parser.addoption("--base-url", action="store", default="https://www.saucedemo.com", help="Application URL")


@pytest.fixture(scope='session')
def base_url(pytestconfig):
    """Returns the base URL from CLI or default."""
    return pytestconfig.getoption("base_url")


# modify scope to "session" if there is just one test suite
@pytest.fixture(scope="module")
def driver(pytestconfig, base_url):
    browser_name = pytestconfig.getoption("browser").lower()

    if browser_name == "chrome":
        driver = webdriver.Chrome()
    elif browser_name == "edge":
        driver = webdriver.Edge()
    else:
        # Raise an error immediately if the browser is invalid
        raise pytest.UsageError(f"--browser '{browser_name}' is not supported. Use 'chrome' or 'edge'.")

    driver.maximize_window()

    if base_url:
        driver.get(base_url)

    yield driver
    driver.quit()


@pytest.fixture(scope='module')
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture(scope='module')
def home_page(driver):
    return HomePage(driver)


@pytest.fixture(scope='function')
def app_login(driver, login_page):
    username = "standard_user"
    password = "secret_sauce"

    login_page.login(username=username, password=password)
    yield
