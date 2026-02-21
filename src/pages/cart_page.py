import re
from selenium.webdriver.common.by import By
from src.config import CART_URL
from src.pages.base_page import BasePage


class CartPage(BasePage):

    CART_URL = CART_URL

    # Locators
    CART_PAGE_TITLE     = (By.XPATH, "//span[@class='title']")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    CHECKOUT_BTN        = (By.ID, "checkout")
    QTY_LABEL           = (By.CLASS_NAME, "cart_quantity_label")
    ITEM_DESC           = (By.CLASS_NAME, "cart_desc_label")
    CART_ITEMS          = (By.CLASS_NAME, "cart_item")
    ITEM_NAME           = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE          = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTON       = (By.CSS_SELECTOR, ".btn.btn_secondary.btn_small.cart_button")
    CART_BADGE          = (By.CLASS_NAME, "shopping_cart_badge")

    def go_to_cart(self):
        self.navigate_url(self.CART_URL)

    def cart_page_title(self) -> str:
        el = self.ele_exists(self.CART_PAGE_TITLE)
        return el.text if el else ""

    def continue_shopping_btn_exist(self):
        return self.ele_exists(self.CONTINUE_SHOPPING_BTN)

    def checkout_btn_exist(self):
        return self.ele_exists(self.CHECKOUT_BTN)

    def qty_label_exist(self):
        return self.ele_exists(self.QTY_LABEL)

    def item_desc_exist(self):
        return self.ele_exists(self.ITEM_DESC)

    def click_continue_shopping(self):
        self.click(*self.CONTINUE_SHOPPING_BTN)

    def checkout(self):
        self.click(*self.CHECKOUT_BTN)

    def cart_items(self):
        return self.elements_exists(self.CART_ITEMS)

    def get_cart_item_names(self) -> list[str]:
        return [
            item.find_element(*self.ITEM_NAME).text
            for item in self.cart_items()
        ]

    def get_cart_item_prices(self) -> list[str]:
        """Return raw price strings for all cart items e.g. ['$9.99', '$15.99']."""
        return [
            item.find_element(*self.ITEM_PRICE).text
            for item in self.cart_items()
        ]

    def get_cart_item_prices_float(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.get_cart_item_prices()]

    def get_cart_item_count(self) -> int:
        return len(self.cart_items())

    def get_cart_badge_count(self) -> int:
        """Return cart badge number, or 0 if badge is absent."""
        el = self.ele_exists(self.CART_BADGE)
        return int(el.text.strip()) if el else 0

    def remove_item_from_cart(self, item_name: str) -> bool:
        """Find an item by name (case-insensitive) and remove it from the cart.

        Returns:
            True  — item found and removed.
            False — item not found in cart.
        """
        pattern = re.compile(re.escape(item_name), re.IGNORECASE)

        for item in self.cart_items():
            name_element = item.find_element(*self.ITEM_NAME)
            if pattern.search(name_element.text):
                item.find_element(*self.REMOVE_BUTTON).click()
                return True

        return False

    def clear_cart(self):
        """Remove all items currently in the cart."""
        for item in self.cart_items():
            item.find_element(*self.REMOVE_BUTTON).click()