from core.base_page import BasePage
from utils.overlay_handler import OverlayHandler


class ProductPage(BasePage):
    ADD_TO_CART = [
        "button[class*='add-to-cart']",
        "//button[contains(text(),'Add to Cart')]",
        "//button[contains(text(),'Add to cart')]",
        "//button[contains(@class, 'add-to-cart')]"
    ]

    def add_to_cart(self):
        OverlayHandler.dismiss_overlays(self.page)
        self.find(self.ADD_TO_CART).click()
        self.page.screenshot(path="artifacts/item_added.png")
