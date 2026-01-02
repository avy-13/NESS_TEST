from core.base_page import BasePage
from utils.overlay_handler import OverlayHandler
from utils.price_parser import parse_price


class CartPage(BasePage):
    SHOP_CART = [
        "//div[contains(@class, 'shop-cart--menu')]",
        "//a[contains(@href, 'shoppingcart')]"
    ]

    CHECKBOX_ALL = [
        "//div[@class='cart-header-checkbox']//label",
        ".cart-header-checkbox label"
    ]

    IS_CHECKED = [
        "//div[@class='cart-header-checkbox']//input[contains(@aria-label,'select product')]",
        ".cart-header-checkbox input"
    ]

    TOTAL = [
        "//span[contains(@class,'total-price')]",
        "//span[contains(text(),'Total')]",
        "(//div[@class='cart-summary-item-wrapStyle-content'])[5]"
    ]

    REMOVE_ITEM = [
        "//span[@aria-label='delete product']",
        ".cart-product-name-ope-trashCan"
    ]

    def assert_total_not_exceeds(self, budget, count):
        self.find(self.SHOP_CART).click()
        self.page.wait_for_load_state("domcontentloaded")
        if not self.checkbox_is_checked():
            self.find(self.CHECKBOX_ALL).click()
        text = self.find(self.TOTAL).inner_text()
        total = parse_price(text)

        assert total <= budget * count, f"the budget: {budget} * count: {count} is < total: {total}"

    def remove_all(self):
        remove_locator = self._get_remove_locator()

        if not remove_locator:
            return

        while remove_locator.count() > 1:
            OverlayHandler.dismiss_overlays(self.page)
            remove_locator.first.click()
            modal = self.page.locator(".comet-v2-modal-content")
            modal.wait_for(state="visible")
            modal.locator(".comet-v2-modal-footer button").first.click()
            remove_locator = self._get_remove_locator()

    def _get_remove_locator(self):
        for selector in self.REMOVE_ITEM:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                return locator
        return None

    def _get_checkbox_locator(self):
        for selector in self.IS_CHECKED:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                return locator.first
        return None

    def checkbox_is_checked(self):
        checkbox = self._get_checkbox_locator()
        return checkbox.is_checked() if checkbox else False
