import os
from datetime import datetime
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException,
)
from selenium.webdriver.support.select import Select
from src.utils.waits import wait_clickable, wait_visible


class BasePage:

    SCREENSHOTS_DIR = "screenshots"

    def __init__(self, driver):
        self.driver = driver
        os.makedirs(self.SCREENSHOTS_DIR, exist_ok=True)


    def _screenshot(self, label: str) -> str:
        """Save a failure screenshot with a timestamp and return its path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{self.SCREENSHOTS_DIR}/fail_{label}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        return filename


    def click(self, by, selector):
        try:
            el = wait_clickable(self.driver, (by, selector))
            el.click()

        except StaleElementReferenceException:
            # Re-find and try once more if the DOM refreshed
            el = wait_clickable(self.driver, (by, selector))
            el.click()

        except TimeoutException:
            self._screenshot(selector)
            raise TimeoutException(
                f"Element not clickable with locator: ({by}, {selector})"
            )

    def type(self, by, selector, text):
        try:
            el = wait_visible(self.driver, (by, selector))
            el.clear()
            el.send_keys(text)
            return el

        except TimeoutException:
            self._screenshot(selector)
            raise TimeoutException(
                f"Element not visible with locator: ({by}, {selector})"
            )

    def navigate_url(self, url):
        self.driver.get(url)


    def ele_text(self, by, selector) -> str:
        """Return element text, or raise TimeoutException on failure."""
        try:
            el = wait_visible(self.driver, (by, selector))
            return el.text

        except TimeoutException:
            self._screenshot(selector)
            raise TimeoutException(
                f"Element not visible with locator: ({by}, {selector})"
            )

    def ele_visible(self, by, selector, timeout=5):
        """Return the element if visible within timeout, otherwise False."""
        try:
            return wait_visible(self.driver, (by, selector), timeout=timeout)

        except TimeoutException:
            return False

    def ele_exists(self, selector):
        """Return the element if it exists in the DOM, otherwise False."""
        try:
            return self.driver.find_element(*selector)

        except NoSuchElementException:
            return False

    def elements_exists(self, selector):
        """Return a list of elements, or an empty list if none found."""
        elements = self.driver.find_elements(*selector)
        return elements if elements else []

    def dropdowns(self, selector):
        """Return a Select object for the given dropdown locator."""
        try:
            el = wait_visible(self.driver, selector)
            return Select(el)

        except TimeoutException:
            self._screenshot(selector[1])
            raise TimeoutException(f"Dropdown not found: {selector}")