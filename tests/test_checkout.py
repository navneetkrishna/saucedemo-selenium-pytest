import pytest

pytestmark = pytest.mark.regression

# Standard checkout info used across tests
FIRST_NAME  = "John"
LAST_NAME   = "Doe"
POSTAL_CODE = "10001"


class TestCheckout:
    """Checkout integration tests — CHK-001 through CHK-006."""

    ITEM_A = "Sauce Labs Bike Light"
    ITEM_B = "Sauce Labs Bolt T-Shirt"

    def _add_items_and_go_to_cart(self, inventory_page, cart_page):
        """Helper: add two standard items then navigate to cart."""
        inventory_page.open()
        inventory_page.add_item_to_cart(self.ITEM_A)
        inventory_page.add_item_to_cart(self.ITEM_B)
        cart_page.go_to_cart()


    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_chk_001_step_one_empty_fields_show_errors(
        self, inventory_page, cart_page, checkout_page, clean_cart
    ):
        """Attempting to continue with all fields empty shows a validation error."""
        self._add_items_and_go_to_cart(inventory_page, cart_page)
        cart_page.checkout()

        assert checkout_page.is_on_step_one(), "Did not reach checkout step one."

        # Submit without filling any field
        checkout_page.click_continue()

        error = checkout_page.get_error_message()
        assert error, "Expected a validation error message, got none."
        assert "First Name is required" in error, \
            f"Expected 'First Name is required' in error, got: '{error}'"

    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_chk_002_overview_shows_subtotal_tax_total(
        self, inventory_page, cart_page, checkout_page, clean_cart
    ):
        """Completing Step One reaches the Overview page with subtotal, tax and total visible."""
        self._add_items_and_go_to_cart(inventory_page, cart_page)
        cart_page.checkout()

        checkout_page.fill_checkout_info(FIRST_NAME, LAST_NAME, POSTAL_CODE)
        checkout_page.click_continue()

        assert checkout_page.is_on_overview(), "Did not reach checkout overview."
        assert checkout_page.get_overview_title() == "Checkout: Overview", \
            "Overview page title is incorrect."

        subtotal = checkout_page.get_subtotal()
        tax = checkout_page.get_tax()
        total = checkout_page.get_total()

        assert subtotal > 0, "Subtotal should be greater than 0."
        assert tax >= 0, "Tax should be non-negative."
        assert total > 0, "Total should be greater than 0."


    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_chk_003_finish_shows_confirmation_and_clears_cart(
        self, inventory_page, cart_page, checkout_page, clean_cart
    ):
        """Finishing checkout shows confirmation page; Back Home returns to inventory with empty cart."""
        self._add_items_and_go_to_cart(inventory_page, cart_page)
        cart_page.checkout()

        checkout_page.fill_checkout_info(FIRST_NAME, LAST_NAME, POSTAL_CODE)
        checkout_page.click_continue()
        checkout_page.click_finish()

        assert checkout_page.is_on_confirmation(), "Did not reach checkout confirmation page."
        assert "Thank you for your order!" in checkout_page.get_confirmation_header(), \
            "Confirmation header text is unexpected."

        checkout_page.click_back_home()

        assert "inventory.html" in checkout_page.driver.current_url, \
            "Back Home did not navigate to inventory."

        cart_page.go_to_cart()
        assert cart_page.get_cart_item_count() == 0, \
            "Cart should be empty after completing checkout."

    @pytest.mark.checkout
    def test_chk_004_cancel_overview_returns_to_cart(
        self, inventory_page, cart_page, checkout_page, clean_cart
    ):
        """Cancelling from the Overview page returns to cart with items still present."""
        self._add_items_and_go_to_cart(inventory_page, cart_page)
        items_before = cart_page.get_cart_item_names()

        cart_page.checkout()
        checkout_page.fill_checkout_info(FIRST_NAME, LAST_NAME, POSTAL_CODE)
        checkout_page.click_continue()

        assert checkout_page.is_on_overview(), "Did not reach overview to test cancel."

        checkout_page.click_cancel_overview()

        assert "cart.html" in checkout_page.driver.current_url, \
            "Cancel from Overview did not return to /cart.html."

        items_after = cart_page.get_cart_item_names()
        assert items_before == items_after, \
            f"Cart items changed after cancelling from overview.\nBefore: {items_before}\nAfter: {items_after}"


    @pytest.mark.checkout
    def test_chk_005_subtotal_equals_sum_of_item_prices(
        self, inventory_page, cart_page, checkout_page, clean_cart
    ):
        """Subtotal on the Overview page equals the sum of individual item prices; total = subtotal + tax."""
        self._add_items_and_go_to_cart(inventory_page, cart_page)

        # Capture individual prices from cart before proceeding
        item_prices = cart_page.get_cart_item_prices_float()
        expected_subtotal = round(sum(item_prices), 2)

        cart_page.checkout()
        checkout_page.fill_checkout_info(FIRST_NAME, LAST_NAME, POSTAL_CODE)
        checkout_page.click_continue()

        actual_subtotal = checkout_page.get_subtotal()
        actual_tax = checkout_page.get_tax()
        actual_total = checkout_page.get_total()

        assert actual_subtotal == expected_subtotal, \
            f"Subtotal mismatch — expected ${expected_subtotal}, got ${actual_subtotal}."

        expected_total = round(actual_subtotal + actual_tax, 2)
        assert actual_total == expected_total, \
            f"Total mismatch — expected ${expected_total} (subtotal + tax), got ${actual_total}."

    @pytest.mark.checkout
    def test_chk_006_inventory_buttons_reset_after_checkout(
        self, inventory_page, cart_page, checkout_page, clean_cart
    ):
        """After completing checkout, all inventory tile buttons read 'Add to cart'."""
        self._add_items_and_go_to_cart(inventory_page, cart_page)
        cart_page.checkout()

        checkout_page.fill_checkout_info(FIRST_NAME, LAST_NAME, POSTAL_CODE)
        checkout_page.click_continue()
        checkout_page.click_finish()
        checkout_page.click_back_home()

        assert inventory_page.all_buttons_say_add_to_cart(), \
            "One or more inventory buttons still read 'Remove' after checkout completion."