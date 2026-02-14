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
    PRODUCT_TITLE = (By.CLASS_NAME, "title")

    # INVENTORIES
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    INVENTORY_IMGS = (By.XPATH, "//img[@class='inventory_item_img']")


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

    def get_inventory_items(self):
        return self.elements_exists(self.INVENTORY_ITEMS)


    def get_inventory_count(self):
        return len(self.elements_exists(self.INVENTORY_ITEMS))


    def get_product_title(self):
        return self.ele_text(*self.PRODUCT_TITLE)


    def cart_exists(self):
        return self.ele_visible(*self.CART_LINK)


    def filter_exists(self):
        return self.ele_visible(*self.FILTER_DROPDOWN)


    def all_products_have_images(self):

        """
            Validates that each inventory item has a visible product image.

            Notes:
            - Avoids global image search to prevent false positives.
            - Uses scoped search (element.find_element) within each inventory item.
            - Ensures image is displayed and has a valid src attribute.
            """
        items = self.elements_exists(self.INVENTORY_ITEMS)

        if not items:
            return False

        for item in items:
            # item scope image search
            image = item.find_element(*self.INVENTORY_IMGS)

            if not image.is_displayed():
                return False

            if not image.get_attribute("src"):
                return False

        return True