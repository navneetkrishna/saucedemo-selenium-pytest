from typing import Literal
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    # LOCATORS
    PAGE_TITLE = (By.CLASS_NAME, "app_logo")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    FILTER_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    NAVIGATION_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_BTN = (By.ID, "logout_sidebar_link")

    def get_page_logo_text(self):
        return self.ele_text(*self.PAGE_TITLE)

    def click_cart(self):
        self.click(*self.CART_LINK)

    def apply_filter(self, short_filter: Literal["a_z", "z_a", "l_h", "h_l"] = "a_z"):
        """used typing.Literal lib to show method param suggestion
            filter: a_z -> A to Z
                    z_a -> Z to A
                    l_h -> Low to High
                    h_l -> High ti Low

                default: A to Z
        """
        pass
