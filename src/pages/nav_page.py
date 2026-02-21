from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from src.pages.base_page import BasePage



class NavPage(BasePage):
    """Page object for the hamburger / sidebar navigation menu."""

    # Locators
    BURGER_BTN       = (By.ID, "react-burger-menu-btn")
    CLOSE_BTN        = (By.ID, "react-burger-cross-btn")
    MENU_WRAPPER     = (By.CLASS_NAME, "bm-menu-wrap")
    ALL_ITEMS_LINK   = (By.ID, "inventory_sidebar_link")
    ABOUT_LINK       = (By.ID, "about_sidebar_link")
    LOGOUT_LINK      = (By.ID, "logout_sidebar_link")
    RESET_LINK       = (By.ID, "reset_sidebar_link")
    CART_BADGE       = (By.CLASS_NAME, "shopping_cart_badge")
    FILTER_DROPDOWN  = (By.CLASS_NAME, "product_sort_container")


    def is_menu_open(self) -> bool:
        """Return True when the sidebar wrapper is aria-hidden=false."""
        el = self.ele_exists(self.MENU_WRAPPER)
        if not el:
            return False
        return el.get_attribute("aria-hidden") == "false"

    def _wait_menu_open(self, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*self.MENU_WRAPPER).get_attribute("aria-hidden") == "false"
        )

    def _wait_menu_closed(self, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*self.MENU_WRAPPER).get_attribute("aria-hidden") == "true"
        )


    def open_menu(self):
        if not self.is_menu_open():
            self.click(*self.BURGER_BTN)
            self._wait_menu_open()

    def close_menu(self):
        if self.is_menu_open():
            self.click(*self.CLOSE_BTN)
            self._wait_menu_closed()

    def click_all_items(self):
        self.open_menu()
        self.click(*self.ALL_ITEMS_LINK)

    def click_logout(self):
        self.open_menu()
        self.click(*self.LOGOUT_LINK)

    def click_about(self):
        self.open_menu()
        self.click(*self.ABOUT_LINK)

    def click_reset_app_state(self):
        self.open_menu()
        self.click(*self.RESET_LINK)
        self.close_menu()


    def get_cart_badge_count(self) -> int:
        el = self.ele_exists(self.CART_BADGE)
        return int(el.text.strip()) if el else 0

    def get_about_link_href(self) -> str:
        self.open_menu()
        el = self.ele_exists(self.ABOUT_LINK)
        href = el.get_attribute("href") if el else ""
        self.close_menu()
        return href