from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from src.utils.waits import presence_located


class LoginPage(BasePage):
    USERNAME_BOX = (By.ID, "user-name")
    PASSWORD_BOX = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    # LOGIN_ERROR = (By.XPATH, "//h3[contains(text(), 'Epic sadface')]")
    NAVIGATION_MENU = (By.ID, "react-burger-menu-btn")

    # username = "standard_user"
    # password = "secret_sauce"

    def is_logged_in(self):
        # to validate login, verify that the navigation icon is available
        return self.ele_exists(self.NAVIGATION_MENU)

    def login(self, username="standard_user", password="secret_sauce"):
        if self.is_logged_in():
            return

        self.driver.get("https://www.saucedemo.com")
        self.type(*self.USERNAME_BOX, text=username)
        self.type(*self.PASSWORD_BOX, text=password)
        self.click(*self.LOGIN_BTN)
