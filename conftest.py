import allure
import pytest
import yaml
import os
import time
from playwright.sync_api import sync_playwright
from utils.overlay_handler import OverlayHandler
from playwright.sync_api import Error as PlaywrightError


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser to run tests against: chromium, firefox, webkit"
    )


@pytest.fixture(scope="session")
def config():
    with open("config/env.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="function")
def page(request, config):
    browser_cli = request.config.getoption("--browser")
    browser_name = browser_cli or config.get("browser", "chromium")

    os.makedirs("artifacts/traces", exist_ok=True)
    os.makedirs("artifacts/screenshots", exist_ok=True)

    with sync_playwright() as p:

        try:
            if config.get("grid", {}).get("enabled"):
                browser = p.chromium.connect_over_cdp(
                    config["grid"]["url"]
                )
            else:
                browser = getattr(p, browser_name).launch(
                    headless=config.get("headless", True)
                )
        except PlaywrightError:
            browser = getattr(p, browser_name).launch(
                headless=True
            )

        run_id = os.environ.get(
            "PYTEST_XDIST_WORKER",
            f"local-{int(time.time())}"
        )

        context = browser.new_context(
            storage_state=config.get("auth", {}).get("storage_state"),
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="UTC"
        )

        context.tracing.start(
            screenshots=True,
            snapshots=True
        )

        page = context.new_page()
        page.goto(
            config["base_url"],
            wait_until="domcontentloaded",
            timeout=config.get("navigation_timeout", 30000)
        )

        page.wait_for_load_state("networkidle")

        OverlayHandler.dismiss_overlays(page)

        yield page

        context.tracing.stop(
            path=f"artifacts/traces/trace-{run_id}.zip"
        )

        context.close()
        browser.close()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        outcome = yield
        result = outcome.get_result()

        if result.when == "call" and result.failed:
            page = item.funcargs.get("page")
            if page:
                screenshot_path = f"artifacts/screenshots/{item.name}.png"
                page.screenshot(path=screenshot_path)

                allure.attach.file(
                    screenshot_path,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
