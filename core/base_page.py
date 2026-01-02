from playwright.sync_api import TimeoutError
import time


class BasePage:
    def __init__(self, page):
        self.page = page

    def find(self, locators, timeout=5000, retry_delay=1):
        last_error = None

        for attempt, locator in enumerate(locators, start=1):
            try:
                print(f"[TRY {attempt}] Locator: {locator}")

                el = self.page.locator(locator)
                el.wait_for(state="visible", timeout=timeout)

                return el

            except TimeoutError as e:
                print(f"[FAIL] {locator}")
                last_error = e
                time.sleep(retry_delay)

        self.page.screenshot(path="artifacts/locator_failure.png")
        raise last_error
