from typing import Literal
from selenium.common.exceptions import *
from selenium.webdriver.support.wait import WebDriverWait
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import re
from src.utils.waits import wait_clickable


class InventoryPage(BasePage):
    # LOCATORS
    PAGE_TITLE = (By.CLASS_NAME, "app_logo")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    FILTER_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    NAVIGATION_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_BTN = (By.ID, "logout_sidebar_link")
    PRODUCT_TITLE = (By.CLASS_NAME, "title")

    # INVENTORIES
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    INVENTORY_IMGS = (By.XPATH, ".//img[@class='inventory_item_img']")
    INVENTORY_NAMES = (By.CLASS_NAME, "inventory_item_name")
    INVENTORY_PRICE = (By.CLASS_NAME, "inventory_item_price")
    INVENTORY_ADDTOCART = (By.XPATH, ".//button[contains(@id, 'add-to-cart') or contains(@id, 'remove')]")


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
            # image = item.find_element(*self.INVENTORY_IMGS)
            
            # Pass the parent_ele 'item' instead of 'driver' to restrict XPath scope to .//
                # - Passing item means the wait will pass that same item as the argument to your callable each poll.
            # Must ignore NoSuchElementException to prevent immediate crash if element isn't present yet
            image = WebDriverWait(item, 5, ignored_exceptions=[NoSuchElementException]).until(
                lambda i: i.find_element(*self.INVENTORY_IMGS).is_displayed() and i.find_element(*self.INVENTORY_IMGS))

            if not image.is_displayed():
                return False

            if not image.get_attribute("src"):
                return False

        return True


    def all_products_have_names(self):

        """
            Validates that each inventory item has a visible and non-empty product name.
            Note:
            - Uses scoped search (element.find_element) within each inventory item.
            """

        items = self.elements_exists(self.INVENTORY_ITEMS)

        if not items:
            return False

        for item in items:
            name = item.find_element(*self.INVENTORY_NAMES)

            if not name.is_displayed():
                return False

            if not name.text.strip():
                return False

        return True


    def all_products_have_prices(self):

        """
            Validates that each inventory item has a visible and non-empty price.
            Note:
            - Uses scoped search (element.find_element) within each inventory item.
            - Uses regular expression to match price
            """

        items = self.elements_exists(self.INVENTORY_ITEMS)

        if not items:
            return False

        for item in items:
            price = item.find_element(*self.INVENTORY_PRICE)

            if not price.is_displayed():
                return False

            if not price.text.strip():
                return False

            price_pattern = r"^\$\d+\.\d{2}$"
            if not re.match(price_pattern, price.text.strip()):
                return False

        return True


    def add_to_cart_button_toggle_works(self):

        """
            Validates that each inventory item has a visible add to cart option.
            Note:
            - Uses scoped search (element.find_element) within each inventory item.
            OR
                -  # Wait for Add / Remove state
                    WebDriverWait(self.driver, 5)
                        .until(lambda d: item.find_element(*self.INVENTORY_ADDTOCART).text.strip() == "Remove"
        )
            - Refetches the Add To Cart/Remove button, to avoid stale element exception
            """

        items = self.elements_exists(self.INVENTORY_ITEMS)

        if not items:
            return False

        for item in items:
            button = item.find_element(*self.INVENTORY_ADDTOCART)

            # Initial state
            if button.text.strip() != "Add to cart":
                return False
            # Click → should change to Remove
            button.click()

            # refetch the button
            remove_button = item.find_element(*self.INVENTORY_ADDTOCART)
            if remove_button.text.strip() != "Remove":
                return False
            # Click again → should revert back
            remove_button.click()


            # refetch the button
            add_button = item.find_element(*self.INVENTORY_ADDTOCART)
            if add_button.text.strip() != "Add to cart":
                return False

        return True


    def default_filter(self):
        # Returns the default filter object or raises the Exception from base_page
        dropdown = self.dropdowns(self.FILTER_DROPDOWN)
        return dropdown.first_selected_option.text
    
