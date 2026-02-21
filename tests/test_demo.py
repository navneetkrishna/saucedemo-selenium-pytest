import time

import pytest

pytestmark = pytest.mark.demo

#
# def test_cart_002(cart_page, inventory_page, app_login):
#     inventory_page.add_item_to_cart('jacket')
#     inventory_page.add_item_to_cart('bike')
#     time.sleep(2)
#     inventory_page.add_item_to_cart('bike')
#     time.sleep(2)
#
#     # cart_page.remove_item_from_cart('jaaaaaket')
#     # remove Jacket from the cart
#     assert cart_page.remove_item_from_cart('Jacket'), "Either item does not exist or remove item from cart failed"
#
#     time.sleep(2)
