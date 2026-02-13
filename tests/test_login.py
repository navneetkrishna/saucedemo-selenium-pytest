import pytest

pytestmark = pytest.mark.login_validation


class TestLogin:

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_auth_001(self, login_page, home_page):
        """Login with valid credentials
        Verify App Logo text"""
        username = 'standard_user'
        password = 'secret_sauce'

        login_page.login(username, password)

        assert home_page.get_page_logo_text() == "Swag Labs", f"Login failed using {username}"

    @pytest.mark.negative
    @pytest.mark.regression
    def test_auth_002(self, login_page, home_page):
        """Login with incorrect credentials
            validate error message
        """
        login_page.log_out()
        username = 'fake_user'
        password = 'fake_pass'

        result = login_page.login(username, password)
        assert result == "False", "Login method should return False for Exception"
        # print(login_page.get_error_message())
        assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"


    @pytest.mark.regression
    def test_auth_003(self, login_page):
        """Navigate to home page without login,
        by passing URL"""

        url = "https://www.saucedemo.com/inventory.html"
        login_page.navigate_url(url)

        error_msg = login_page.get_error_message()
        assert error_msg == "Epic sadface: You can only access '/inventory.html' when you are logged in.",\
            "Error occurred during failed login validation"

    @pytest.mark.regression
    def test_auth_004(self, login_page, app_login):
        """Validate Logout redirects to login page"""

        # ensure user is logged in
        if not login_page.is_logged_in():
            login_page.login()

        assert login_page.log_out()

    @pytest.mark.negative
    @pytest.mark.regression
    def test_auth_005(self, login_page, home_page):
        """Login with locked out user credentials"""

        username = 'locked_out_user'
        password = 'secret_sauce'
        login_page.login(username, password)

        error_msg = login_page.get_error_message()
        # print(error_msg)
        assert error_msg == "Epic sadface: Sorry, this user has been locked out.", \
            "Error occurred during locked user login validation"