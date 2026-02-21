import pytest

pytestmark = pytest.mark.regression


class TestNavigation:
    """Hamburger menu and navigation tests — NAV-001 through NAV-006."""

    SAUCEDEMO_ABOUT_URL = "https://saucelabs.com"


    @pytest.mark.smoke
    @pytest.mark.nav
    def test_nav_001_burger_menu_opens_and_closes(self, nav_page, app_login, inventory_page):
        """Burger menu opens on click and closes on the X button click."""
        inventory_page.open()

        # Open
        nav_page.open_menu()
        assert nav_page.is_menu_open(), "Menu should be open after clicking burger button."

        # Close
        nav_page.close_menu()
        assert not nav_page.is_menu_open(), "Menu should be closed after clicking close button."

    @pytest.mark.smoke
    @pytest.mark.nav
    def test_nav_002_all_items_returns_to_inventory(self, nav_page, inventory_page, app_login):
        """'All Items' menu link navigates to /inventory.html."""
        # Start somewhere else — go to cart
        nav_page.navigate_url("https://www.saucedemo.com/cart.html")

        nav_page.click_all_items()

        assert "inventory.html" in nav_page.driver.current_url, \
            "All Items link did not navigate to /inventory.html."
        assert inventory_page.get_product_title() == "Products", \
            "Inventory page title not found after clicking All Items."

    @pytest.mark.smoke
    @pytest.mark.nav
    def test_nav_002_logout_redirects_to_login(self, nav_page, login_page, app_login):
        """Logout menu option logs out and redirects to the login page."""
        nav_page.click_logout()

        assert bool(login_page.ele_exists(login_page.LOGIN_BTN)), \
            "Login button not found after logout — did not land on the login page."

    @pytest.mark.smoke
    @pytest.mark.nav
    def test_nav_003_reset_app_state_clears_cart_and_buttons(
        self, nav_page, inventory_page, app_login
    ):
        """Reset App State clears the cart badge and resets all Add to cart buttons."""
        inventory_page.open()
        inventory_page.add_item_to_cart("Sauce Labs Bike Light")
        inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

        assert inventory_page.get_cart_badge_count() > 0, \
            "Precondition failed: badge should be > 0 before reset."

        nav_page.click_reset_app_state()

        assert inventory_page.get_cart_badge_count() == 0, \
            "Cart badge should be gone after Reset App State."
        assert inventory_page.all_buttons_say_add_to_cart(), \
            "All inventory buttons should read 'Add to cart' after Reset App State."


    @pytest.mark.nav
    def test_nav_004_about_link_points_to_saucelabs(self, nav_page, app_login, inventory_page):
        """About link href points to the SauceLabs website.

        We verify the href attribute rather than following the link to avoid
        leaving the SauceDemo domain mid-test and dealing with new-tab handling.
        """
        inventory_page.open()

        href = nav_page.get_about_link_href()
        assert href, "About link has no href."
        assert self.SAUCEDEMO_ABOUT_URL in href, \
            f"About link href '{href}' does not point to '{self.SAUCEDEMO_ABOUT_URL}'."


    @pytest.mark.nav
    def test_nav_005_browser_back_forward_stays_valid(
        self, nav_page, inventory_page, cart_page, app_login
    ):
        """Browser back and forward buttons keep the app on valid, rendered SauceDemo pages."""
        inventory_page.open()
        cart_page.go_to_cart()

        # Back → inventory
        nav_page.driver.back()
        assert "saucedemo.com" in nav_page.driver.current_url, \
            "Back button left SauceDemo domain."
        assert "error" not in nav_page.driver.page_source.lower()[:500], \
            "Page contains error text after browser back."

        # Forward → cart
        nav_page.driver.forward()
        assert "saucedemo.com" in nav_page.driver.current_url, \
            "Forward button left SauceDemo domain."
        assert "error" not in nav_page.driver.page_source.lower()[:500], \
            "Page contains error text after browser forward."

    @pytest.mark.nav
    def test_nav_006_rapid_toggle_does_not_freeze_menu(
        self, nav_page, inventory_page, app_login
    ):
        """Rapidly toggling the menu open and closed leaves it in a usable closed state."""
        inventory_page.open()

        # Rapidly open and close several times
        for _ in range(5):
            nav_page.open_menu()
            nav_page.close_menu()

        # Final state: menu must be closed and burger button must be clickable
        assert not nav_page.is_menu_open(), \
            "Menu is stuck open after rapid toggling."

        # Verify menu is still functional after rapid toggling
        nav_page.open_menu()
        assert nav_page.is_menu_open(), \
            "Menu failed to open after rapid toggling — it may be stuck."
        nav_page.close_menu()