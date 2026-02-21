import re
from typing import Literal
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from src.config import INVENTORY_URL
from src.pages.base_page import BasePage


class InventoryPage(BasePage):

    INVENTORY_URL = INVENTORY_URL

    # Locators
    PAGE_TITLE      = (By.CLASS_NAME, "app_logo")
    CART_LINK       = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE      = (By.CLASS_NAME, "shopping_cart_badge")
    FILTER_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    NAVIGATION_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_BTN      = (By.ID, "logout_sidebar_link")
    PRODUCT_TITLE   = (By.CLASS_NAME, "title")

    # Inventory item child locators
    INVENTORY_ITEMS   = (By.CLASS_NAME, "inventory_item")
    INVENTORY_IMGS    = (By.XPATH, ".//img[@class='inventory_item_img']")
    INVENTORY_NAMES   = (By.CLASS_NAME, "inventory_item_name")
    INVENTORY_PRICE   = (By.CLASS_NAME, "inventory_item_price")
    INVENTORY_ADDTOCART = (By.XPATH, ".//button[contains(@id,'add-to-cart') or contains(@id,'remove')]")

    # Filter map shared across the class
    FILTER_MAP = {
        "a_z": "Name (A to Z)",
        "z_a": "Name (Z to A)",
        "l_h": "Price (low to high)",
        "h_l": "Price (high to low)",
    }

    def open(self):
        self.navigate_url(self.INVENTORY_URL)
        return self

    def get_page_logo_text(self) -> str:
        return self.ele_text(*self.PAGE_TITLE)

    def get_product_title(self) -> str:
        return self.ele_text(*self.PRODUCT_TITLE)

    def click_cart(self):
        self.click(*self.CART_LINK)

    def cart_exists(self):
        return self.ele_visible(*self.CART_LINK)

    def filter_exists(self):
        return self.ele_visible(*self.FILTER_DROPDOWN)

    def get_inventory_items(self):
        return self.elements_exists(self.INVENTORY_ITEMS)

    def get_inventory_count(self) -> int:
        return len(self.elements_exists(self.INVENTORY_ITEMS))

    def apply_filter(self, short_filter: Literal["a_z", "z_a", "l_h", "h_l"] = "a_z"):
        """Select a sort filter by shorthand key.

        Keys:
            a_z -> Name (A to Z)
            z_a -> Name (Z to A)
            l_h -> Price (low to high)
            h_l -> Price (high to low)
        """
        target_text = self.FILTER_MAP.get(short_filter.lower())
        if not target_text:
            raise ValueError(
                f"Invalid filter key: '{short_filter}'. Valid keys: {list(self.FILTER_MAP.keys())}"
            )
        dropdown = self.dropdowns(self.FILTER_DROPDOWN)
        dropdown.select_by_visible_text(target_text)

    def current_filter(self) -> str:
        """Return the currently selected filter label."""
        dropdown = self.dropdowns(self.FILTER_DROPDOWN)
        return dropdown.first_selected_option.text

    def get_cart_badge_count(self) -> int:
        """Return cart badge number, or 0 if badge is absent."""
        el = self.ele_exists(self.CART_BADGE)
        return int(el.text.strip()) if el else 0

    def all_products_have_images(self) -> bool:
        """Validate that each inventory item has a visible image with a src attribute."""
        items = self.elements_exists(self.INVENTORY_ITEMS)
        if not items:
            return False

        for item in items:
            image = WebDriverWait(item, 5, ignored_exceptions=[NoSuchElementException]).until(
                lambda i: i.find_element(*self.INVENTORY_IMGS).is_displayed()
                and i.find_element(*self.INVENTORY_IMGS)
            )
            if not image.is_displayed() or not image.get_attribute("src"):
                return False

        return True

    def all_products_have_names(self) -> bool:
        """Validate that each inventory item has a visible, non-empty name."""
        items = self.elements_exists(self.INVENTORY_ITEMS)
        if not items:
            return False

        for item in items:
            name = item.find_element(*self.INVENTORY_NAMES)
            if not name.is_displayed() or not name.text.strip():
                return False

        return True

    def all_products_have_prices(self) -> bool:
        """Validate that each inventory item has a visible price matching $X.XX format."""
        items = self.elements_exists(self.INVENTORY_ITEMS)
        if not items:
            return False

        price_pattern = re.compile(r"^\$\d+\.\d{2}$")

        for item in items:
            price = item.find_element(*self.INVENTORY_PRICE)
            if not price.is_displayed() or not price.text.strip():
                return False
            if not price_pattern.match(price.text.strip()):
                return False

        return True

    def add_to_cart_button_toggle_works(self) -> bool:
        """Validate Add to Cart ↔ Remove button toggle for every inventory item."""
        items = self.elements_exists(self.INVENTORY_ITEMS)
        if not items:
            return False

        for item in items:
            button = item.find_element(*self.INVENTORY_ADDTOCART)
            if button.text.strip() != "Add to cart":
                return False

            button.click()
            remove_button = item.find_element(*self.INVENTORY_ADDTOCART)
            if remove_button.text.strip() != "Remove":
                return False

            remove_button.click()
            add_button = item.find_element(*self.INVENTORY_ADDTOCART)
            if add_button.text.strip() != "Add to cart":
                return False

        return True

    def add_item_to_cart(self, item_name: str) -> bool:
        """Find an item by name (case-insensitive) and add it to the cart.

        Returns:
            True  — item found and added.
            False — item already in cart or not found.
        """
        items = self.get_inventory_items()
        pattern = re.compile(re.escape(item_name), re.IGNORECASE)

        for item in items:
            name_element = item.find_element(*self.INVENTORY_NAMES)
            if pattern.search(name_element.text):
                add_button = item.find_element(*self.INVENTORY_ADDTOCART)
                if add_button.text.strip() != "Add to cart":
                    return False
                add_button.click()
                return True

        return False

    def get_item_button_text(self, item_name: str) -> str:
        """Return the Add/Remove button text for a specific item by name."""
        items = self.get_inventory_items()
        pattern = re.compile(re.escape(item_name), re.IGNORECASE)

        for item in items:
            name_element = item.find_element(*self.INVENTORY_NAMES)
            if pattern.search(name_element.text):
                btn = item.find_element(*self.INVENTORY_ADDTOCART)
                return btn.text.strip()

        return ""

    def click_item_name(self, item_name: str) -> bool:
        """Click a product name link to navigate to its PDP.

        Returns True if the item was found and clicked, False otherwise.
        """
        items = self.get_inventory_items()
        pattern = re.compile(re.escape(item_name), re.IGNORECASE)

        for item in items:
            name_element = item.find_element(*self.INVENTORY_NAMES)
            if pattern.search(name_element.text):
                name_element.click()
                return True

        return False

    def get_item_price(self, item_name: str) -> str:
        """Return the raw price string (e.g. '$9.99') for a named item."""
        items = self.get_inventory_items()
        pattern = re.compile(re.escape(item_name), re.IGNORECASE)

        for item in items:
            name_element = item.find_element(*self.INVENTORY_NAMES)
            if pattern.search(name_element.text):
                return item.find_element(*self.INVENTORY_PRICE).text.strip()

        return ""

    def get_product_names(self) -> list[str]:
        """Return a list of all displayed product names."""
        items = self.elements_exists(self.INVENTORY_ITEMS)
        return [item.find_element(*self.INVENTORY_NAMES).text for item in items]

    def get_product_prices(self) -> list[float]:
        """Return a list of all displayed product prices as floats."""
        items = self.elements_exists(self.INVENTORY_ITEMS)
        return [
            float(item.find_element(*self.INVENTORY_PRICE).text.replace("$", ""))
            for item in items
        ]

    def all_buttons_say_add_to_cart(self) -> bool:
        """Return True if every inventory item button reads 'Add to cart'."""
        items = self.get_inventory_items()
        if not items:
            return False
        return all(
            item.find_element(*self.INVENTORY_ADDTOCART).text.strip() == "Add to cart"
            for item in items
        )