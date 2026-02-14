from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.pages.home_page import HomePage
from src.utils.waits import presence_located, wait_clickable


class LoginPage(BasePage):
    USERNAME_BOX = (By.ID, "user-name")
    PASSWORD_BOX = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    LOGIN_FAIL_ERROR = (By.CSS_SELECTOR, ".error-message-container.error")
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test= 'error']")


    def is_logged_in(self):
        # to validate login, verify that the navigation icon is available
        return self.ele_exists(HomePage.NAVIGATION_MENU)


    def login(self, username="standard_user", password="secret_sauce"):
        if self.is_logged_in():
            return "Success"

        self.driver.get("https://www.saucedemo.com")
        self.type(*self.USERNAME_BOX, text=username)
        self.type(*self.PASSWORD_BOX, text=password)
        self.click(*self.LOGIN_BTN)

        try:
            # 1. Wait for EITHER the error message OR the inventory URL
            WebDriverWait(self.driver, 5).until(
                EC.any_of(
                    EC.visibility_of_element_located(self.LOGIN_FAIL_ERROR),
                    EC.visibility_of_element_located(HomePage.NAVIGATION_MENU)
                    # EC.url_contains("inventory.html")
                )
            )
            # 2. Check which condition actually happened
            if self.ele_exists(HomePage.NAVIGATION_MENU):
                return "Success"
            return "False"

        except Exception:
            # 3. Neither happened within 5 seconds (e.g., app crashed or slow network)
            return "TIMEOUT"


    def get_error_message(self):
        """Helper to verify WHY the login failed"""
        error_el = self.ele_visible(*self.LOGIN_FAIL_ERROR)
        if error_el:
            return error_el.text

        return ""


    def log_out(self):

        if not self.is_logged_in():
            return True

        try:

            wait_clickable(self.driver, HomePage.NAVIGATION_MENU).click()
            wait_clickable(self.driver, HomePage.LOGOUT_BTN).click()

            # 1. Wait for EITHER the LOGIN PAGE OR the NAVIGATION MENU
            WebDriverWait(self.driver, 5).until(
                EC.any_of(
                    EC.visibility_of_element_located(self.LOGIN_BTN),
                    EC.visibility_of_element_located(HomePage.NAVIGATION_MENU)
                )
            )

            # success if Login button is found
            return self.ele_exists(self.LOGIN_BTN)

        except Exception as e:
            # 3. Neither happened within 5 seconds (e.g., app crashed or slow network)
            print(e)
            return False
