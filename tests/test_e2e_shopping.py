import json

import pytest

from pages.LoginPage import LoginPage
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

with open("config/test_data.json") as f:
    test_cases = json.load(f)


@pytest.mark.parametrize("case", test_cases, ids=lambda c: c["name"])
def test_e2e_shopping(page, case):
    if case["login"] is True:
        login = LoginPage(page)
        login.login(case["email"], case["password"])
    home = HomePage(page)
    home.search(case["query"])

    results = SearchResultsPage(page)
    results.sort_price_low_to_high()

    urls = results.collect_items_under_price(
        case["max_price"],
        case["limit"]
    )

    for url in urls:
        page.goto(url)
        ProductPage(page).add_to_cart()

    CartPage(page).assert_total_not_exceeds(
        case["max_price"],
        len(urls)
    )

    CartPage(page).remove_all()
