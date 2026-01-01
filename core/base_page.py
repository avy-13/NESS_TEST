from playwright.sync_api import TimeoutError
import time


class BasePage:
    def __init__(self, page):
        self.page = page

    def dismiss_overlays(self):
        possible_buttons = [
            "button:has-text('Accept')",
            "button:has-text('Agree')",
            "button:has-text('I agree')",
            "#onetrust-accept-btn-handler",
            "button[aria-label*='accept']"
        ]

        for btn in possible_buttons:
            try:
                locator = self.page.locator(btn)
                if locator.is_visible(timeout=2000):
                    locator.click()
                    print(f"🟢 Dismissed overlay with: {btn}")
                    return
            except:
                pass

    def find(self, locators, timeout=3000, retry_delay=1):
        last_error = None

        for attempt, locator in enumerate(locators, start=1):
            try:
                print(f"[TRY {attempt}] Locator: {locator}")

                el = self.page.locator(locator)
                el.wait_for(state="visible", timeout=timeout)  # ✅ FIX

                return el

            except TimeoutError as e:
                print(f"[FAIL] {locator}")
                last_error = e
                time.sleep(retry_delay)

        self.page.screenshot(path="artifacts/locator_failure.png")
        raise last_error
