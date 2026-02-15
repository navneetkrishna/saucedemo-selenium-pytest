import pytest

pytestmark = pytest.mark.demo


def test_inv_002(inventory_page, app_login):
    assert inventory_page.all_products_have_names(), "One or more products have invalid name"
    assert inventory_page.all_products_have_prices(), "One or more products have invalid price"
