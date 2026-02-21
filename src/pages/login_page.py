from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.config import BASE_URL, STANDARD_USER, STANDARD_PASSWORD
from src.pages.base_page import BasePage
from src.pages.inventory_page import InventoryPage
from src.utils.waits import wait_clickable


class LoginPage(BasePage):

    LOGIN_URL = BASE_URL

    # Locators
    USERNAME_BOX = (By.ID, "user-name")
    PASSWORD_BOX = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test='error']")

    def is_logged_in(self) -> bool:
        return bool(self.ele_exists(InventoryPage.NAVIGATION_MENU))

    def login(self, username=STANDARD_USER, password=STANDARD_PASSWORD) -> bool:
        """Attempt to log in. Returns True on success, False on failure."""
        if self.is_logged_in():
            return True

        self.navigate_url(self.LOGIN_URL)
        self.type(*self.USERNAME_BOX, text=username)
        self.type(*self.PASSWORD_BOX, text=password)
        self.click(*self.LOGIN_BTN)

        try:
            WebDriverWait(self.driver, 5).until(
                EC.any_of(
                    EC.visibility_of_element_located(self.ERROR_MESSAGE),
                    EC.visibility_of_element_located(InventoryPage.NAVIGATION_MENU),
                )
            )
            return self.is_logged_in()

        except Exception:
            # Neither success nor error appeared within timeout
            return False

    def get_error_message(self) -> str:
        """Return the visible error message text, or an empty string."""
        el = self.ele_visible(*self.ERROR_MESSAGE)
        return el.text if el else ""

    def log_out(self) -> bool:
        """Log out the current user. Returns True if redirected to login page."""
        if not self.is_logged_in():
            return True

        try:
            wait_clickable(self.driver, InventoryPage.NAVIGATION_MENU).click()
            wait_clickable(self.driver, InventoryPage.LOGOUT_BTN).click()

            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.LOGIN_BTN)
            )
            return bool(self.ele_exists(self.LOGIN_BTN))

        except Exception as e:
            print(f"[log_out] Exception: {e}")
            return False