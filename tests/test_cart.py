import pytest


class TestCart:

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.cart
    def test_cart_001(self, cart_page, app_login):
        cart_page.go_to_cart()
        assert cart_page.cart_page_title() == "Your Cart", "Cart page title is either incorrect or missing"
        assert cart_page.continue_shopping_btn_exist(), "Continue shopping button is not available"
        assert cart_page.checkout_btn_exist(), "Checkout button is not available"
        assert cart_page.qty_label_exist(), "Quantity label does not exist"
        assert cart_page.item_desc_exist(), "Item Description does not exist"
        assert cart_page.qty_label_exist().text == "QTY", "Quantity label does not exist"
        assert cart_page.item_desc_exist().text == "Description", "Item Description does not exist"


    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_002(self, cart_page, inventory_page, app_login):
        inventory_page.add_item_to_cart('Jacket')


    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_003(self, inventory_page, cart_page, app_login):

        # precondition: Add items to cart (jacket/bike light)
        inventory_page.add_item_to_cart('Jacket')
        inventory_page.add_item_to_cart('Bike')
        inventory_page.add_item_to_cart('Onesie')

        # remove Jacket from the cart
        assert cart_page.remove_item_from_cart('Bike'), "Either item does not exist or remove item from cart failed"
