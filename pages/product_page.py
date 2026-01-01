from core.base_page import BasePage


class ProductPage(BasePage):
    ADD_TO_CART = [
        "//button[contains(text(),'Add to Cart')]",
        "//button[contains(text(),'Add to cart')]",
        "//button[contains(@class, 'add-to-cart')]"
    ]

    def add_to_cart(self):
        self.find(self.ADD_TO_CART).click()
        self.page.screenshot(path="artifacts/item_added.png")
