from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.utils.waits import wait_visible, wait_clickable


class CartPage(BasePage):
    CART_URL = "https://www.saucedemo.com/cart.html"
    CART_PAGE_TITLE = (By.XPATH, "//span[@class= 'title']")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    CHECKOUT_BTN = (By.ID, "checkout")
    QTY_LABEL = (By.CLASS_NAME, "cart_quantity_label")
    ITEM_DESC = (By.CLASS_NAME, "cart_desc_label")


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