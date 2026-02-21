import pytest

pytestmark = pytest.mark.inventory_ui


class TestInventoryUI:

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    def test_inv_001(self, inventory_page, app_login):
        """Validate core UI elements are present on the inventory page."""
        assert inventory_page.get_page_logo_text() == "Swag Labs", \
            "App logo text missing or did not match."
        assert inventory_page.get_product_title() == "Products", \
            "Inventory page title missing or did not match."
        assert inventory_page.cart_exists(), "Could not locate cart icon."
        assert inventory_page.filter_exists(), "Could not locate filter dropdown."

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    def test_inv_002(self, inventory_page, app_login):
        """Validate all 6 products display images, names, prices and working Add to Cart toggle."""
        assert inventory_page.get_inventory_count() == 6, \
            "Inventory page did not contain 6 items."
        assert inventory_page.all_products_have_images(), \
            "One or more products did not contain a valid image."
        assert inventory_page.all_products_have_names(), \
            "One or more products have an invalid or missing name."
        assert inventory_page.all_products_have_prices(), \
            "One or more products have an invalid or missing price."
        assert inventory_page.add_to_cart_button_toggle_works(), \
            "Add to cart button toggle failed for one or more products."

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    def test_inv_003(self, inventory_page, app_login):
        """Validate default filter is Name (A to Z) immediately after login."""
        assert inventory_page.current_filter() == "Name (A to Z)", \
            "Default filter value is incorrect."

    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.sorting
    @pytest.mark.parametrize("short_filter, expected_label", [
        ("a_z", "Name (A to Z)"),
        ("z_a", "Name (Z to A)"),
        ("l_h", "Price (low to high)"),
        ("h_l", "Price (high to low)"),
    ])
    def test_inv_004_filter_options(self, inventory_page, app_login, short_filter, expected_label):
        """Validate each filter option can be selected and reflects the correct label."""
        inventory_page.apply_filter(short_filter)
        assert inventory_page.current_filter() == expected_label, \
            f"Filter '{short_filter}' did not display expected label: '{expected_label}'"

    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.sorting
    def test_inv_005_sort_name_asc(self, inventory_page, app_login):
        """Validate Name (A to Z) filter sorts products alphabetically ascending."""
        inventory_page.apply_filter("a_z")
        names = inventory_page.get_product_names()
        assert names == sorted(names), \
            f"Products not sorted A→Z. Got: {names}"

    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.sorting
    def test_inv_006_sort_name_desc(self, inventory_page, app_login):
        """Validate Name (Z to A) filter sorts products alphabetically descending."""
        inventory_page.apply_filter("z_a")
        names = inventory_page.get_product_names()
        assert names == sorted(names, reverse=True), \
            f"Products not sorted Z→A. Got: {names}"

    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.sorting
    def test_inv_007_sort_price_asc(self, inventory_page, app_login):
        """Validate Price (low to high) filter sorts products by price ascending."""
        inventory_page.apply_filter("l_h")
        prices = inventory_page.get_product_prices()
        assert prices == sorted(prices), \
            f"Products not sorted low→high. Got: {prices}"

    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.sorting
    def test_inv_008_sort_price_desc(self, inventory_page, app_login):
        """Validate Price (high to low) filter sorts products by price descending."""
        inventory_page.apply_filter("h_l")
        prices = inventory_page.get_product_prices()
        assert prices == sorted(prices, reverse=True), \
            f"Products not sorted high→low. Got: {prices}"