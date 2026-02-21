import pytest

pytestmark = pytest.mark.regression


class TestPDP:
    """Product Details Page test suite.

    SauceDemo product IDs (stable):
        0 - Sauce Labs Bike Light
        1 - Sauce Labs Bolt T-Shirt
        2 - Sauce Labs Fleece Jacket
        3 - Sauce Labs Backpack
        4 - Sauce Labs Onesie
        5 - Test.allTheThings() T-Shirt (Red)
    """

    VALID_ID = 4          # Sauce Labs Onesie — arbitrary stable choice
    INVALID_IDS = [-1, 99999, 0]   # 0 maps to Bike Light; -1 / 99999 are invalid


    @pytest.mark.pdp
    def test_pdp_001(self, pdp_page, inventory_page, clean_cart):
        """PDP shows a non-empty name, valid price, non-empty description and visible image."""
        inventory_page.open()
        # Click the first product name to reach its PDP naturally
        first_name = inventory_page.get_product_names()[0]
        inventory_page.click_item_name(first_name)

        assert pdp_page.is_on_pdp(), "Did not navigate to a PDP after clicking product name."
        assert pdp_page.get_product_name(), "PDP product name is empty."
        assert pdp_page.get_product_description(), "PDP product description is empty."
        assert pdp_page.get_product_price().startswith("$"), \
            f"PDP price format unexpected: {pdp_page.get_product_price()}"
        assert pdp_page.is_image_displayed(), "PDP product image is not displayed or has no src."

    @pytest.mark.pdp
    def test_pdp_002(self, pdp_page, inventory_page, clean_cart):
        """Back to Products button returns to the inventory page."""
        inventory_page.open()
        first_name = inventory_page.get_product_names()[0]
        inventory_page.click_item_name(first_name)

        assert pdp_page.is_on_pdp(), "Did not land on PDP."

        pdp_page.click_back()

        assert "inventory.html" in pdp_page.driver.current_url, \
            "Back button did not return to /inventory.html."
        assert inventory_page.get_product_title() == "Products", \
            "Inventory page header not found after clicking Back."


    @pytest.mark.pdp
    def test_pdp_003(self, pdp_page, inventory_page, clean_cart):
        """Adding from PDP increments cart badge; Remove reverts badge and tile button."""
        inventory_page.open()
        first_name = inventory_page.get_product_names()[0]
        inventory_page.click_item_name(first_name)

        assert pdp_page.get_add_remove_btn_text() == "Add to cart", \
            "Button should read 'Add to cart' before adding."

        pdp_page.click_add_to_cart()

        assert pdp_page.get_add_remove_btn_text() == "Remove", \
            "Button should read 'Remove' after adding."
        assert pdp_page.get_cart_badge_count() == 1, \
            "Cart badge should show 1 after adding one item from PDP."

        # Go back to inventory and verify tile button state changed
        pdp_page.click_back()
        tile_btn_text = inventory_page.get_item_button_text(first_name)
        assert tile_btn_text == "Remove", \
            f"Inventory tile button should read 'Remove' after PDP add, got '{tile_btn_text}'."

        # Remove from PDP
        inventory_page.click_item_name(first_name)
        pdp_page.click_remove()

        assert pdp_page.get_add_remove_btn_text() == "Add to cart", \
            "Button should revert to 'Add to cart' after removal."
        assert pdp_page.get_cart_badge_count() == 0, \
            "Cart badge should disappear after removing the only item."

    @pytest.mark.pdp
    def test_pdp_004(self, pdp_page, inventory_page, clean_cart):
        """Price and name on the PDP match what is shown on the inventory tile."""
        inventory_page.open()

        # Capture name + price from the inventory tile first
        first_name = inventory_page.get_product_names()[0]
        tile_price = inventory_page.get_item_price(first_name)

        # Navigate to its PDP and compare
        inventory_page.click_item_name(first_name)

        pdp_name = pdp_page.get_product_name()
        pdp_price = pdp_page.get_product_price()

        assert pdp_name == first_name, \
            f"Name mismatch — tile: '{first_name}', PDP: '{pdp_name}'."
        assert pdp_price == tile_price, \
            f"Price mismatch — tile: '{tile_price}', PDP: '{pdp_price}'."


    @pytest.mark.pdp
    def test_pdp_005_valid_direct_navigation(self, pdp_page, clean_cart):
        """Direct URL navigation to a valid product ID renders the correct product."""
        pdp_page.open(self.VALID_ID)

        assert pdp_page.is_on_pdp(), "Not on a PDP after direct navigation."
        assert pdp_page.get_product_name(), "Product name is empty for a valid direct-nav PDP."
        assert pdp_page.is_image_displayed(), "Product image not displayed for a valid direct-nav PDP."
        assert pdp_page.get_product_price().startswith("$"), \
            "Product price format invalid for a valid direct-nav PDP."

    @pytest.mark.pdp
    def test_pdp_005_invalid_direct_navigation(self, pdp_page, inventory_page, clean_cart):
        """Direct URL navigation with an invalid product ID is handled gracefully.

        SauceDemo does not show an error page — it either shows an empty PDP or
        redirects. We verify the app does not crash (no JS error page) and at
        minimum remains on a navigable SauceDemo page.
        """
        pdp_page.open(99999)

        current_url = pdp_page.driver.current_url
        page_source = pdp_page.driver.page_source.lower()

        # The app should not show a generic browser/server error page
        assert "404" not in page_source, "App returned a 404 for an invalid product ID."
        assert "error" not in pdp_page.driver.title.lower(), \
            "Browser tab title indicates an error for an invalid product ID."
        assert "saucedemo.com" in current_url, \
            "App navigated away from SauceDemo domain on invalid product ID."