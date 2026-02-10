from selenium.common.exceptions import *

from src.utils.waits import *


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def click(self, by, selector):
        try:
            el = wait_clickable(self.driver, (by, selector))
            el.click()

        except StaleElementReferenceException:
            # Re-find and try one more time if the DOM refreshed
            el = wait_clickable(self.driver, (by, selector))
            el.click()

        except TimeoutException:
            self.driver.save_screenshot(f"fail_{selector}.png")
            raise Exception(f"Failed to find element with locator: ({by}, {selector}) within timeout.")

    def type(self, by, selector, text):
        try:
            el = wait_visible(self.driver, (by, selector))
            el.clear()
            el.send_keys(text)
            return el

        except TimeoutException:
            self.driver.save_screenshot(f"fail_{selector}.png")
            raise Exception(f"Failed to find element with locator: ({by}, {selector}) within timeout.")

    def ele_text(self, by, selector):
        try:
            el = wait_visible(self.driver, (by, selector))
            return el.text

        except TimeoutException:
            self.driver.save_screenshot(f"fail_{selector}.png")
            raise Exception(f"Failed to find element with locator: ({by}, {selector}) within timeout.")

    def ele_visible(self, by, selector):
        try:
            wait_visible(self.driver, (by, selector), timeout=5)
            return True

        except TimeoutException:
            self.driver.save_screenshot(f"fail_{selector}.png")
            raise Exception(f"Failed to find element with locator: ({by}, {selector}) within timeout.")

    def ele_exists(self, selector):

        try:
            el = self.driver.find_element(*selector)
            return el

        except NoSuchElementException:
            self.driver.save_screenshot(f"fail_{selector}.png")
            # raise Exception(f"Failed to find element with locator: ({by}, {selector}) within timeout.")
            return False