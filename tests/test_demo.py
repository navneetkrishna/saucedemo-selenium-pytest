# def test_is_login(driver, login_page, app_login):
#     login_page.login()
#

def test_app_logo_text(driver, home_page):
    app_txt = home_page.get_page_logo_text()
    print(app_txt)
    assert app_txt == "Swag Labs"


def test_click_cart(driver, home_page):
    home_page.click_cart()