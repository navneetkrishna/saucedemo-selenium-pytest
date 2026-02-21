import time

import pytest

pytestmark = pytest.mark.demo
#
#
# def test_cart_002(cart_page, inventory_page, app_login):
#
#     inventory_page.add_item_to_cart('jacket')
#     inventory_page.add_item_to_cart('bike')
#     inventory_page.add_item_to_cart('backpack')
#
#     time.sleep(2)
#
#     items_before = cart_page.get_cart_item_names()
#     cart_page.click_continue_shopping()
#     cart_page.go_to_cart()
#     items_after = cart_page.get_cart_item_names()
#
#     assert items_before == items_after
