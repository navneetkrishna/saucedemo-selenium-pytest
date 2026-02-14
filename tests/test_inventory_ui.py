import pytest


pytestmark = pytest.mark.inventory_ui

class TestInventoryUI:

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_inv_001(self, home_page, app_login):
        assert home_page.get_page_logo_text() == "Swag Labs", "App logo text missing or did not match."
        assert home_page.get_product_title() == "Products", "Inventory page title missing or did not match."
        assert home_page.get_inventory_count() == 6, "Inventory page did not contain 6 items."
        assert home_page.cart_exists(), "Could not locate cart."
        assert home_page.filter_exists(), "Could not locate filter dropdown."
        assert home_page.all_products_have_images(), "One or more products did not contain images."
