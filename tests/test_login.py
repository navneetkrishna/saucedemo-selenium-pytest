import pytest

from src.config import STANDARD_USER, LOCKED_OUT_USER, STANDARD_PASSWORD

pytestmark = pytest.mark.login_validation


class TestLogin:

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_auth_001(self, login_page, inventory_page):
        """Login with valid credentials and verify landing on inventory page."""
        assert login_page.login(STANDARD_USER, STANDARD_PASSWORD), \
            f"Login failed for user: {STANDARD_USER}"
        assert inventory_page.get_page_logo_text() == "Swag Labs", \
            "App logo text missing or did not match after login."

    @pytest.mark.negative
    @pytest.mark.regression
    def test_auth_002(self, login_page):
        """Login with incorrect credentials and validate error message."""
        login_page.log_out()

        result = login_page.login("fake_user", "fake_pass")

        assert result is False, "login() should return False for invalid credentials"
        assert login_page.get_error_message() == \
            "Epic sadface: Username and password do not match any user in this service"

    @pytest.mark.regression
    def test_auth_003(self, login_page):
        """Bypass login by navigating directly to inventory URL — expect error."""
        login_page.log_out()
        login_page.navigate_url("https://www.saucedemo.com/inventory.html")

        assert login_page.get_error_message() == \
            "Epic sadface: You can only access '/inventory.html' when you are logged in."

    @pytest.mark.regression
    def test_auth_004(self, login_page, app_login):
        """Validate that logout redirects back to the login page."""
        assert login_page.log_out(), "Logout did not redirect to the login page"

    @pytest.mark.negative
    @pytest.mark.regression
    def test_auth_005(self, login_page):
        """Login with locked-out user credentials and validate error message."""
        login_page.log_out()
        login_page.login(LOCKED_OUT_USER, STANDARD_PASSWORD)

        assert login_page.get_error_message() == \
            "Epic sadface: Sorry, this user has been locked out."

    @pytest.mark.negative
    @pytest.mark.regression
    def test_auth_006(self, login_page):
        """Login with empty username and password — validate error message."""
        login_page.log_out()
        login_page.navigate_url(login_page.LOGIN_URL)
        result = login_page.login("", "")

        assert result is False, "login() should return False for empty credentials"
        assert login_page.get_error_message() == "Epic sadface: Username is required"

    @pytest.mark.negative
    @pytest.mark.regression
    def test_auth_007(self, login_page):
        """Login with valid username but empty password — validate error message."""
        login_page.log_out()
        result = login_page.login(STANDARD_USER, "")

        assert result is False, "login() should return False for missing password"
        assert login_page.get_error_message() == "Epic sadface: Password is required"