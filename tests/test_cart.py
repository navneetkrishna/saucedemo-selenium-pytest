import pytest


class TestCart:

    items = ['Jacket', 'Bike Light', 'Onesie', 'backpack', 'T-Shirt']

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

        inventory_page.navigate_url(inventory_page.INVENTORY_URL)
        assert inventory_page.add_item_to_cart(self.items[0]), "Failed to add item to cart"
        assert inventory_page.add_item_to_cart(self.items[1]), "Failed to add item to cart"
        assert inventory_page.add_item_to_cart(self.items[4]), "Failed to add item to cart"


    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_003(self, inventory_page, cart_page, app_login):

        """Preconditions:
            1. Go to inventory page
            2. Add few random items to cart (jacket/bike light)"""
        cart_page.navigate_url(inventory_page.INVENTORY_URL)
        inventory_page.add_item_to_cart(self.items[0])
        inventory_page.add_item_to_cart(self.items[2])
        inventory_page.add_item_to_cart(self.items[4])

        # validate: remove 3rd item from the cart
        cart_page.go_to_cart()
        assert cart_page.remove_item_from_cart(self.items[2]), "Either item does not exist or remove item from cart failed"


    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_004(self, inventory_page, cart_page, app_login):
        """Ensures item state is maintained during page navigation

        # Preconditions:
            1. Go to inventory page
            2. Add few random items to cart (jacket/bike light)"""

        inventory_page.open()
        inventory_page.add_item_to_cart(self.items[0])
        inventory_page.add_item_to_cart(self.items[2])
        inventory_page.add_item_to_cart(self.items[4])

        # validate: items are maintained
        cart_page.go_to_cart()
        items_before = cart_page.get_cart_item_names()
        cart_page.click_continue_shopping()
        cart_page.go_to_cart()
        items_after = cart_page.get_cart_item_names()
        assert items_before == items_after, "Items are missing from cart after navigation"


    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_005(self, inventory_page, cart_page, app_login):
        """Ensures item state is maintained during after page refresh

        # Preconditions:
            1. Go to inventory page
            2. Add few random items to cart (jacket/bike light)"""

        inventory_page.open()
        inventory_page.add_item_to_cart(self.items[0])
        inventory_page.add_item_to_cart(self.items[2])
        inventory_page.add_item_to_cart(self.items[4])

        # validate: items are maintained
        cart_page.go_to_cart()
        items_before = cart_page.get_cart_item_names()
        cart_page.driver.refresh()
        items_after = cart_page.get_cart_item_names()

        assert items_before == items_after, "Items are missing from cart after page refresh"
