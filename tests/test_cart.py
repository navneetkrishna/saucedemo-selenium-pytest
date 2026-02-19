import pytest

class TestCart:

    @pytest.mark.demo
    def test_cart_001(self, cart_page, app_login):
        cart_page.go_to_cart()
        assert cart_page.cart_page_title() == "Your Cart", "Cart page title is either incorrect or missing"
        assert cart_page.continue_shopping_btn_exist(), "Continue shopping button is not available"
        assert cart_page.checkout_btn_exist(), "Checkout button is not available"
        assert cart_page.qty_label_exist(), "Quantity label does not exist"
        assert cart_page.item_desc_exist(), "Item Description does not exist"
        assert cart_page.qty_label_exist().text == "QTY", "Quantity label does not exist"
        assert cart_page.item_desc_exist().text == "Description", "Item Description does not exist"



