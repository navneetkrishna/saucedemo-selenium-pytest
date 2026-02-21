import re
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class CartPage(BasePage):
    CART_URL = "https://www.saucedemo.com/cart.html"
    CART_PAGE_TITLE = (By.XPATH, "//span[@class= 'title']")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    CHECKOUT_BTN = (By.ID, "checkout")
    QTY_LABEL = (By.CLASS_NAME, "cart_quantity_label")
    ITEM_DESC = (By.CLASS_NAME, "cart_desc_label")

    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    REMOVE_BUTTON = (By.CSS_SELECTOR, ".btn.btn_secondary.btn_small.cart_button")


    def go_to_cart(self):
        return self.navigate_url(self.CART_URL)


    def cart_page_title(self):
        return self.ele_exists(self.CART_PAGE_TITLE).text


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

    def remove_item_from_cart(self, item_name):
        """Searches for an item by name
         and removes it from the cart (if exists)
         using Case-Insensitive Regex.

         - returns False, if the searched item does not exist"""

        self.go_to_cart()
        items = self.cart_items()

        # Create a case-insensitive regex pattern
        # re.escape handles special characters in item_name safely
        pattern = re.compile(re.escape(item_name), re.IGNORECASE)

        for item in items:
            # 1. Get the name of the current item
            name_element = item.find_element(*self.ITEM_NAME)
            actual_name = name_element.text

            # 2. Use regex for a flexible, case-insensitive match
            if pattern.search(actual_name):
                # 3. Locate and click the button specifically for THIS item
                remove_button = item.find_element(*self.REMOVE_BUTTON)
                remove_button.click()

                # Exit once the item is found and removed
                return True

        return False