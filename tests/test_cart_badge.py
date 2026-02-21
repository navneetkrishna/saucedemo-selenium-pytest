import pytest

pytestmark = pytest.mark.regression


class TestCartBadge:
    """Cart badge and cart page tests — CART-001 through CART-006."""

    ITEM_A = "Sauce Labs Bike Light"
    ITEM_B = "Sauce Labs Bolt T-Shirt"
    ITEM_C = "Sauce Labs Fleece Jacket"
    VALID_ID_A = 0    # Bike Light
    VALID_ID_B = 1    # Bolt T-Shirt


    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_001_badge_reflects_distinct_items(self, inventory_page, clean_cart):
        """Cart badge count equals the number of distinct items added."""
        inventory_page.open()

        assert inventory_page.get_cart_badge_count() == 0, \
            "Badge should be absent (0) before adding any items."

        inventory_page.add_item_to_cart(self.ITEM_A)
        assert inventory_page.get_cart_badge_count() == 1, \
            "Badge should read 1 after adding one item."

        inventory_page.add_item_to_cart(self.ITEM_B)
        assert inventory_page.get_cart_badge_count() == 2, \
            "Badge should read 2 after adding two distinct items."

        inventory_page.add_item_to_cart(self.ITEM_C)
        assert inventory_page.get_cart_badge_count() == 3, \
            "Badge should read 3 after adding three distinct items."

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_002_cart_page_shows_correct_items_names_prices(
        self, inventory_page, cart_page, clean_cart
    ):
        """Clicking the cart navigates to /cart.html showing correct item names and prices."""
        inventory_page.open()

        # Capture tile prices before adding
        tile_price_a = inventory_page.get_item_price(self.ITEM_A)
        tile_price_b = inventory_page.get_item_price(self.ITEM_B)

        inventory_page.add_item_to_cart(self.ITEM_A)
        inventory_page.add_item_to_cart(self.ITEM_B)

        inventory_page.click_cart()

        assert "cart.html" in cart_page.driver.current_url, \
            "Cart icon did not navigate to /cart.html."

        cart_names = cart_page.get_cart_item_names()
        assert self.ITEM_A in cart_names, f"'{self.ITEM_A}' missing from cart."
        assert self.ITEM_B in cart_names, f"'{self.ITEM_B}' missing from cart."

        cart_prices = cart_page.get_cart_item_prices()
        assert tile_price_a in cart_prices, \
            f"Price '{tile_price_a}' for '{self.ITEM_A}' not found in cart."
        assert tile_price_b in cart_prices, \
            f"Price '{tile_price_b}' for '{self.ITEM_B}' not found in cart."


    @pytest.mark.cart
    def test_cart_003_remove_updates_badge_and_tile(
        self, inventory_page, cart_page, clean_cart
    ):
        """Removing an item from the cart updates the badge and resets the inventory tile button."""
        inventory_page.open()
        inventory_page.add_item_to_cart(self.ITEM_A)
        inventory_page.add_item_to_cart(self.ITEM_B)

        assert inventory_page.get_cart_badge_count() == 2

        # Remove from cart page
        cart_page.go_to_cart()
        cart_page.remove_item_from_cart(self.ITEM_A)

        # Badge should now show 1
        assert cart_page.get_cart_badge_count() == 1, \
            "Badge should read 1 after removing one of two items."

        # Go back to inventory and verify tile button reverted
        inventory_page.open()
        tile_btn = inventory_page.get_item_button_text(self.ITEM_A)
        assert tile_btn == "Add to cart", \
            f"Inventory tile for '{self.ITEM_A}' should read 'Add to cart' after cart removal, got '{tile_btn}'."

    @pytest.mark.cart
    def test_cart_004_badge_persists_after_refresh(self, inventory_page, clean_cart):
        """Cart badge count is maintained after refreshing the inventory page."""
        inventory_page.open()
        inventory_page.add_item_to_cart(self.ITEM_A)
        inventory_page.add_item_to_cart(self.ITEM_B)

        badge_before = inventory_page.get_cart_badge_count()

        inventory_page.driver.refresh()

        badge_after = inventory_page.get_cart_badge_count()
        assert badge_before == badge_after, \
            f"Badge changed after refresh: was {badge_before}, now {badge_after}."


    @pytest.mark.cart
    def test_cart_005_pdp_and_inventory_add_deduplicate(
        self, inventory_page, pdp_page, cart_page, clean_cart
    ):
        """Adding the same product via PDP and inventory does not duplicate it in the cart.

        SauceDemo treats each product as a single slot — adding an already-added
        item from a different surface should not create a second cart entry.
        """
        # Add via inventory
        inventory_page.open()
        inventory_page.add_item_to_cart(self.ITEM_A)

        # Attempt to add the same product via its PDP (button will already read Remove)
        inventory_page.click_item_name(self.ITEM_A)
        btn_text = pdp_page.get_add_remove_btn_text()
        assert btn_text == "Remove", \
            "PDP button should already read 'Remove' for an item added via inventory."

        # Verify cart still has exactly 1 entry
        cart_page.go_to_cart()
        assert cart_page.get_cart_item_count() == 1, \
            "Cart should contain exactly 1 entry — same product must not be duplicated."

    @pytest.mark.cart
    def test_cart_006_state_survives_navigation_loop(
        self, inventory_page, pdp_page, cart_page, clean_cart
    ):
        """Cart contents survive a full inventory → PDP → cart → back loop."""
        # Step 1: add two items from inventory
        inventory_page.open()
        inventory_page.add_item_to_cart(self.ITEM_A)
        inventory_page.add_item_to_cart(self.ITEM_B)
        items_added = {self.ITEM_A, self.ITEM_B}

        # Step 2: visit PDP of one item
        inventory_page.click_item_name(self.ITEM_A)
        assert pdp_page.is_on_pdp(), "Expected to be on PDP after clicking item name."

        # Step 3: go to cart from PDP
        pdp_page.click(*pdp_page.CART_BADGE) if pdp_page.ele_exists(pdp_page.CART_BADGE) \
            else cart_page.go_to_cart()
        cart_page.go_to_cart()

        # Step 4: navigate back to inventory
        cart_page.click_continue_shopping()

        # Step 5: verify cart state is intact
        cart_page.go_to_cart()
        cart_names = set(cart_page.get_cart_item_names())
        assert items_added == cart_names, \
            f"Cart contents changed after navigation loop.\nExpected: {items_added}\nGot: {cart_names}"