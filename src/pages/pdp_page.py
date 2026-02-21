from selenium.webdriver.common.by import By

from src.config import BASE_URL
from src.pages.base_page import BasePage


class PDPPage(BasePage):
    """Page object for the Product Details Page (/inventory-item.html?id=X)."""

    PDP_BASE_URL = f"{BASE_URL}/inventory-item.html"

    # Locators
    BACK_BUTTON    = (By.ID, "back-to-products")
    PRODUCT_NAME   = (By.CLASS_NAME, "inventory_details_name")
    PRODUCT_DESC   = (By.CLASS_NAME, "inventory_details_desc")
    PRODUCT_PRICE  = (By.CLASS_NAME, "inventory_details_price")
    PRODUCT_IMAGE  = (By.CLASS_NAME, "inventory_details_img")
    ADD_REMOVE_BTN = (By.XPATH, "//button[contains(@id,'add-to-cart') or contains(@id,'remove')]")
    CART_BADGE     = (By.CLASS_NAME, "shopping_cart_badge")

    def open(self, product_id: int):
        """Navigate directly to a PDP by product ID."""
        self.navigate_url(f"{self.PDP_BASE_URL}?id={product_id}")
        return self


    def get_product_name(self) -> str:
        return self.ele_text(*self.PRODUCT_NAME)

    def get_product_description(self) -> str:
        return self.ele_text(*self.PRODUCT_DESC)

    def get_product_price(self) -> str:
        """Return raw price string e.g. '$29.99'."""
        return self.ele_text(*self.PRODUCT_PRICE)

    def get_product_price_float(self) -> float:
        return float(self.get_product_price().replace("$", ""))

    def is_image_displayed(self) -> bool:
        el = self.ele_visible(*self.PRODUCT_IMAGE)
        return bool(el) and bool(el.get_attribute("src"))

    def get_add_remove_btn_text(self) -> str:
        el = self.ele_exists(self.ADD_REMOVE_BTN)
        return el.text.strip() if el else ""

    def get_cart_badge_count(self) -> int:
        """Return cart badge number, or 0 if badge is absent."""
        el = self.ele_exists(self.CART_BADGE)
        return int(el.text.strip()) if el else 0

    def is_on_pdp(self) -> bool:
        return "inventory-item.html" in self.driver.current_url


    def click_add_to_cart(self):
        self.click(*self.ADD_REMOVE_BTN)

    def click_remove(self):
        self.click(*self.ADD_REMOVE_BTN)

    def click_back(self):
        self.click(*self.BACK_BUTTON)