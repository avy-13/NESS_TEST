import pytest
import yaml
import os
import time
from playwright.sync_api import sync_playwright
from utils.overlay_handler import OverlayHandler
from playwright.sync_api import Error as PlaywrightError


@pytest.fixture(scope="session")
def config():
    with open("config/env.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="function")
def page(config):
    with sync_playwright() as p:
        browser_type = config.get("browser", "chromium")

        if config.get("grid", {}).get("enabled"):
            try:
                browser = p.chromium.connect_over_cdp(
                    config["grid"]["url"]
                )
            except PlaywrightError:
                print("⚠️ Grid not available – falling back to local browser")
                browser = getattr(p, browser_type).launch(
                    headless=config.get("headless", True)
                )
        else:
            browser = getattr(p, browser_type).launch(
                headless=config.get("headless", True)
            )

        run_id = os.environ.get(
            "PYTEST_XDIST_WORKER",
            f"local-{int(time.time())}"
        )

        context = browser.new_context(
            storage_state=config.get("auth", {}).get("storage_state")
        )

        # context.set_default_timeout(
        #     config.get("timeout", 5000)
        # )

        context.tracing.start(
            screenshots=True,
            snapshots=True
        )

        page = context.new_page()
        page.goto(config["base_url"],
                  wait_until="domcontentloaded",
                  timeout=config.get("navigation_timeout", 30000)
                  )
        OverlayHandler.dismiss_overlays(page)

        yield page

        context.tracing.stop(
            path=f"artifacts/traces/trace-{run_id}.zip"
        )

        context.close()
        browser.close()
