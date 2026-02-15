import pytest


pytestmark = pytest.mark.inventory_ui

class TestInventoryUI:

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    def test_inv_001(self, inventory_page, app_login):
        assert inventory_page.get_page_logo_text() == "Swag Labs", "App logo text missing or did not match."
        assert inventory_page.get_product_title() == "Products", "Inventory page title missing or did not match."
        assert inventory_page.cart_exists(), "Could not locate cart."
        assert inventory_page.filter_exists(), "Could not locate filter dropdown."


    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    def test_inv_002(self, inventory_page, app_login):
        assert inventory_page.get_inventory_count() == 6, "Inventory page did not contain 6 items."
        assert inventory_page.all_products_have_images(), "One or more products did not contain images."
        assert inventory_page.all_products_have_names(), "One or more products have invalid name"
        assert inventory_page.all_products_have_prices(), "One or more products have invalid price"
        assert inventory_page.add_to_cart_button_toggle_works(), "Add to cart button toggle failed"
