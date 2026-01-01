from core.base_page import BasePage
from utils.price_parser import parse_price
from utils.normalize_url import normalize_url


class SearchResultsPage(BasePage):
    SORT_PRICE = [
        "//div[contains(@ae_object_value,'price')]",
        "//span[contains(text(),'Price')]"
    ]

    ITEM = [
        "//a[contains(@class,'search-card-item')]",
        "//div[contains(@class,'product-container')]//a"
    ]

    NEXT = [
        "//button[contains(@class,'next-btn')]",
        "//a[contains(text(),'Next')]"
    ]

    def sort_price_low_to_high(self):
        price_sort = self.find(self.SORT_PRICE)
        price_sort.click()
        self.page.wait_for_timeout(500)
        price_sort.click()
        self.page.wait_for_load_state("domcontentloaded")

    def collect_items_under_price(self, max_price: float, limit: int):
        urls = []

        while len(urls) < limit:
            items = self.page.locator(self.ITEM[0]).all()

            for item in items:
                if len(urls) == limit:
                    break
                price_text = item.inner_text()
                price = parse_price(price_text)
                if price and price <= max_price:
                    urls.append(normalize_url(item.get_attribute("href"),"https://www.aliexpress.com"))

            if self.page.locator(self.NEXT[0]).count() == 0:
                break

            self.page.click(self.NEXT[0])
            self.page.wait_for_load_state("domcontentloaded")

        return urls
