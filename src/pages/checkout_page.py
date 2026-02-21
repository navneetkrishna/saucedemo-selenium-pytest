from selenium.webdriver.common.by import By

from src.config import BASE_URL
from src.pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page object covering Step One, Overview, and Confirmation of SauceDemo checkout."""

    CHECKOUT_STEP1_URL    = f"{BASE_URL}/checkout-step-one.html"
    CHECKOUT_STEP2_URL    = f"{BASE_URL}/checkout-step-two.html"
    CHECKOUT_COMPLETE_URL = f"{BASE_URL}/checkout-complete.html"

    # --- Step One locators ---
    FIRST_NAME_INPUT  = (By.ID, "first-name")
    LAST_NAME_INPUT   = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BTN      = (By.ID, "continue")
    CANCEL_BTN        = (By.ID, "cancel")
    ERROR_MESSAGE     = (By.XPATH, "//h3[@data-test='error']")

    # --- Overview locators ---
    OVERVIEW_TITLE    = (By.XPATH, "//span[@class='title']")
    OVERVIEW_ITEMS    = (By.CLASS_NAME, "cart_item")
    ITEM_NAME         = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE        = (By.CLASS_NAME, "inventory_item_price")
    SUBTOTAL_LABEL    = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL         = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL       = (By.CLASS_NAME, "summary_total_label")
    FINISH_BTN        = (By.ID, "finish")
    OVERVIEW_CANCEL   = (By.ID, "cancel")

    # --- Confirmation locators ---
    CONFIRM_HEADER    = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BTN     = (By.ID, "back-to-products")


    def is_on_step_one(self) -> bool:
        return "checkout-step-one" in self.driver.current_url

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        """Fill in all Step One fields."""
        self.type(*self.FIRST_NAME_INPUT, text=first_name)
        self.type(*self.LAST_NAME_INPUT, text=last_name)
        self.type(*self.POSTAL_CODE_INPUT, text=postal_code)

    def click_continue(self):
        self.click(*self.CONTINUE_BTN)

    def click_cancel_step_one(self):
        self.click(*self.CANCEL_BTN)

    def get_error_message(self) -> str:
        el = self.ele_visible(*self.ERROR_MESSAGE)
        return el.text if el else ""


    def is_on_overview(self) -> bool:
        return "checkout-step-two" in self.driver.current_url

    def get_overview_title(self) -> str:
        el = self.ele_exists(self.OVERVIEW_TITLE)
        return el.text if el else ""

    def get_overview_item_names(self) -> list[str]:
        items = self.elements_exists(self.OVERVIEW_ITEMS)
        return [item.find_element(*self.ITEM_NAME).text for item in items]

    def get_subtotal(self) -> float:
        """Return subtotal as a float by stripping the label prefix."""
        text = self.ele_text(*self.SUBTOTAL_LABEL)
        # text is like "Item total: $29.99"
        return float(text.split("$")[-1])

    def get_tax(self) -> float:
        text = self.ele_text(*self.TAX_LABEL)
        return float(text.split("$")[-1])

    def get_total(self) -> float:
        text = self.ele_text(*self.TOTAL_LABEL)
        return float(text.split("$")[-1])

    def click_finish(self):
        self.click(*self.FINISH_BTN)

    def click_cancel_overview(self):
        self.click(*self.OVERVIEW_CANCEL)


    def is_on_confirmation(self) -> bool:
        return "checkout-complete" in self.driver.current_url

    def get_confirmation_header(self) -> str:
        el = self.ele_exists(self.CONFIRM_HEADER)
        return el.text if el else ""

    def click_back_home(self):
        self.click(*self.BACK_HOME_BTN)