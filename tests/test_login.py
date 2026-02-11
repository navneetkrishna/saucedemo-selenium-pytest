import pytest

pytestmark = pytest.mark.login_validation


class TestLogin:

    @pytest.mark.smoke
    def test_auth_001(self, login_page, home_page):
        """Login with valid credentials
        Verify App Logo text"""
        username = 'standard_user'
        password = 'secret_sauce'

        login_page.login(username, password)

        assert home_page.get_page_logo_text() == "Swag Labs", f"Login failed using {username}"

    # @pytest.mark.negative
    # def test_auth_002(self, login_page, home_page):
    #     """Login with incorrect credentials
    #         validate error message
    #     """
    #     username = 'fake_user'
    #     password = 'fake_pass'
    #
    #     result = login_page.login(username, password)
    #     assert result == "False", "Login method should return False for Exception"
    #     # print(login_page.get_error_message())
    #     assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"
