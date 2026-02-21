import pytest


class TestCart:

    ITEMS = ["Jacket", "Bike Light", "Onesie", "Backpack", "T-Shirt"]

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.cart
    def test_cart_001(self, cart_page, clean_cart):
        """Validate core UI elements are present on the cart page."""
        cart_page.go_to_cart()

        assert cart_page.cart_page_title() == "Your Cart", \
            "Cart page title is incorrect or missing."
        assert cart_page.continue_shopping_btn_exist(), \
            "Continue Shopping button is not present."
        assert cart_page.checkout_btn_exist(), \
            "Checkout button is not present."

        qty_label = cart_page.qty_label_exist()
        item_desc = cart_page.item_desc_exist()

        assert qty_label, "QTY label does not exist."
        assert item_desc, "Description label does not exist."
        assert qty_label.text == "QTY", "QTY label text is incorrect."
        assert item_desc.text == "Description", "Description label text is incorrect."

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_002(self, inventory_page, cart_page, clean_cart):
        """Validate multiple items can be added to the cart from the inventory page."""
        inventory_page.open()

        assert inventory_page.add_item_to_cart(self.ITEMS[0]), \
            f"Failed to add '{self.ITEMS[0]}' to cart."
        assert inventory_page.add_item_to_cart(self.ITEMS[1]), \
            f"Failed to add '{self.ITEMS[1]}' to cart."
        assert inventory_page.add_item_to_cart(self.ITEMS[4]), \
            f"Failed to add '{self.ITEMS[4]}' to cart."

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_003(self, inventory_page, cart_page, clean_cart):
        """Validate an item can be removed from the cart."""
        inventory_page.open()
        inventory_page.add_item_to_cart(self.ITEMS[0])
        inventory_page.add_item_to_cart(self.ITEMS[2])
        inventory_page.add_item_to_cart(self.ITEMS[4])

        cart_page.go_to_cart()

        assert cart_page.remove_item_from_cart(self.ITEMS[2]), \
            f"Failed to remove '{self.ITEMS[2]}' from cart."
        assert self.ITEMS[2] not in cart_page.get_cart_item_names(), \
            f"'{self.ITEMS[2]}' is still in the cart after removal."

    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_004(self, inventory_page, cart_page, clean_cart):
        """Validate cart items are preserved after navigating away and back."""
        inventory_page.open()
        inventory_page.add_item_to_cart(self.ITEMS[0])
        inventory_page.add_item_to_cart(self.ITEMS[2])
        inventory_page.add_item_to_cart(self.ITEMS[4])

        cart_page.go_to_cart()
        items_before = cart_page.get_cart_item_names()

        cart_page.click_continue_shopping()
        cart_page.go_to_cart()
        items_after = cart_page.get_cart_item_names()

        assert items_before == items_after, \
            "Cart items changed after navigating away and returning."

    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_005(self, inventory_page, cart_page, clean_cart):
        """Validate cart items are preserved after a page refresh."""
        inventory_page.open()
        inventory_page.add_item_to_cart(self.ITEMS[0])
        inventory_page.add_item_to_cart(self.ITEMS[2])
        inventory_page.add_item_to_cart(self.ITEMS[4])

        cart_page.go_to_cart()
        items_before = cart_page.get_cart_item_names()

        cart_page.driver.refresh()
        items_after = cart_page.get_cart_item_names()

        assert items_before == items_after, \
            "Cart items changed after page refresh."

    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_006(self, inventory_page, cart_page, clean_cart):
        """Validate cart is empty when no items have been added."""
        cart_page.go_to_cart()

        assert cart_page.get_cart_item_count() == 0, \
            "Cart should be empty but contains items."

    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_007(self, inventory_page, cart_page, clean_cart):
        """Validate item count in cart matches the number of items added."""
        inventory_page.open()
        items_to_add = [self.ITEMS[0], self.ITEMS[1], self.ITEMS[2]]

        for item in items_to_add:
            inventory_page.add_item_to_cart(item)

        cart_page.go_to_cart()

        assert cart_page.get_cart_item_count() == len(items_to_add), \
            f"Expected {len(items_to_add)} items in cart, got {cart_page.get_cart_item_count()}."

    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_008(self, inventory_page, cart_page, clean_cart):
        """Validate Continue Shopping button navigates back to the inventory page."""
        cart_page.go_to_cart()
        cart_page.click_continue_shopping()

        assert inventory_page.get_product_title() == "Products", \
            "Continue Shopping did not navigate to the inventory page."