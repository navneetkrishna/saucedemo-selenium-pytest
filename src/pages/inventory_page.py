from typing import Literal
from selenium.common.exceptions import *
from selenium.webdriver.support.wait import WebDriverWait
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import re
from src.utils.waits import wait_clickable


class InventoryPage(BasePage):
    # LOCATORS
    INVENTORY_URL = "https://www.saucedemo.com/inventory.html"
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
            filter: a_z -> Name (A to Z)
                    z_a -> Name (Z to A)
                    l_h -> Price (low to high)
                    h_l -> Price (high to low)

                default: A to Z
        """

        # 1. Map shorthand codes to the EXACT visible text in the UI
        filter_map = {
            "a_z": "Name (A to Z)",
            "z_a": "Name (Z to A)",
            "l_h": "Price (low to high)",
            "h_l": "Price (high to low)"
        }

        # 2. Get the Select object from your base_page method
        dropdown = self.dropdowns(self.FILTER_DROPDOWN)

        # 3. Validation
        target_text = filter_map.get(short_filter.lower())
        if not target_text:
            raise ValueError(f"Invalid filter key: {short_filter}. Use: {list(filter_map.keys())}")

            # 4. Perform the action
        dropdown.select_by_visible_text(target_text)

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


    def current_filter(self):
        # Returns the default filter object or raises the Exception from base_page
        dropdown = self.dropdowns(self.FILTER_DROPDOWN)
        return dropdown.first_selected_option.text


    def add_item_to_cart(self, item_name):
        """Searches for an item by name and adds it to the cart using Case-Insensitive Regex."""
        # navigate to Inventory page
        self.navigate_url(self.INVENTORY_URL)
        items = self.get_inventory_items()

        # Create a case-insensitive regex pattern
        # re.escape handles special characters in item_name safely
        pattern = re.compile(re.escape(item_name), re.IGNORECASE)

        for item in items:
            # 1. Get the name of the current item
            name_element = item.find_element(*self.INVENTORY_NAMES)
            actual_name = name_element.text

            # 2. Use regex for a flexible, case-insensitive match
            if pattern.search(actual_name):
                # 3. Locate and click the button specifically for THIS item
                add_button = item.find_element(*self.INVENTORY_ADDTOCART)

                # click only if the item is not already added
                if add_button.text.strip() != "Add to cart":
                    # print(f"{actual_name} item already present in cart")
                    return False
                add_button.click()

                # Exit once the item is found and clicked
                return True

        return False