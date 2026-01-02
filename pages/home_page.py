from core.base_page import BasePage
from utils.overlay_handler import OverlayHandler


class HomePage(BasePage):

    SEARCH_INPUT = [
        "//input[contains(@id,'search-words')]",
        "//input[@type='search']"
    ]

    SEARCH_BTN = [
        "//input[@type='button']",
        "//button[contains(@class,'search-button')]"
    ]

    def search(self, query):
        self.page.wait_for_load_state("domcontentloaded")
        OverlayHandler.dismiss_overlays(self.page)
        self.find(self.SEARCH_INPUT).fill(query)
        self.find(self.SEARCH_BTN).click()
