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


    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    def test_inv_003(self, inventory_page, app_login):

        """Validates the default filter >>> Name (A to Z)

        Note: - Validating current filter value immediately after login
        """
        assert inventory_page.current_filter() == "Name (A to Z)", "Default filter failed"


    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.sorting
    def test_inv_004(self, inventory_page, app_login):

        """Validates filter >>> Name (A to Z)"""
        desired_filter = 'a_Z'

        # Map shorthand codes to the EXACT visible text in the UI
        filter_map = {
            "a_z": "Name (A to Z)",
            "z_a": "Name (Z to A)",
            "l_h": "Price (low to high)",
            "h_l": "Price (high to low)"
        }

        inventory_page.apply_filter(desired_filter.lower())

        assert inventory_page.current_filter() == filter_map.get(desired_filter.lower())

    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.sorting
    def test_inv_005(self, inventory_page, app_login):
        """Validates filter >>> Name (Z to A)"""

        # Map shorthand codes to the EXACT visible text in the UI
        desired_filter = 'Z_A'

        filter_map = {
            "a_z": "Name (A to Z)",
            "z_a": "Name (Z to A)",
            "l_h": "Price (low to high)",
            "h_l": "Price (high to low)"
        }

        inventory_page.apply_filter(desired_filter.lower())

        assert inventory_page.current_filter() == filter_map.get(desired_filter.lower())


    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.sorting
    def test_inv_006(self, inventory_page, app_login):
        """Validates filter >>> Price (Low to High)"""

        # Map shorthand codes to the EXACT visible text in the UI
        desired_filter = 'l_h'

        filter_map = {
            "a_z": "Name (A to Z)",
            "z_a": "Name (Z to A)",
            "l_h": "Price (low to high)",
            "h_l": "Price (high to low)"
        }

        inventory_page.apply_filter(desired_filter.lower())

        assert inventory_page.current_filter() == filter_map.get(desired_filter.lower())


    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.sorting
    def test_inv_007(self, inventory_page, app_login):
        """Validates filter >>> Price (High to Low)"""

        # Map shorthand codes to the EXACT visible text in the UI
        desired_filter = 'h_l'

        filter_map = {
            "a_z": "Name (A to Z)",
            "z_a": "Name (Z to A)",
            "l_h": "Price (low to high)",
            "h_l": "Price (high to low)"
        }

        inventory_page.apply_filter(desired_filter.lower())

        assert inventory_page.current_filter() == filter_map.get(desired_filter.lower())

