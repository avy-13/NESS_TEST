class OverlayHandler:
    CLOSE_BUTTONS = [
        "//button[contains(text(),'Accept')]",
        "//button[contains(text(),'Agree')]",
        "//button[contains(text(),'Got it')]",
        "//button[contains(@class,'close')]",
        "//span[contains(text(),'×')]",
        "//img[@class='pop-close-btn']",
        ".pop-close-btn",
        "._24EHh",
        ".baxia-dialog-mask",
        "[class*='dialog-mask']",
        "[class*='overlay']",
        "iframe[src*='captcha']"
    ]

    @staticmethod
    def dismiss_overlays(page):
        for locator in OverlayHandler.CLOSE_BUTTONS:
            try:
                if page.locator(locator).is_visible(timeout=2000):
                    page.locator(locator).click()
            except:
                pass
