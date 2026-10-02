from pathlib import Path

from playwright.sync_api import sync_playwright


MOCK_WEB_PATH = Path(__file__).resolve().parents[2] / "mock_web" / "index.html"
EVIDENCE_DIR = Path(__file__).resolve().parents[2] / "evidence"


def update_ticket_priority(
    ticket_id: str,
    priority: str,
) -> dict:

    EVIDENCE_DIR.mkdir(exist_ok=True)

    screenshot_path = EVIDENCE_DIR / f"{ticket_id}_browser.png"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(MOCK_WEB_PATH.as_uri())

        page.locator("#ticket_id").fill(ticket_id)

        page.locator("#priority").select_option(priority)

        page.locator("button[type='submit']").click()

        result = page.locator("#result").inner_text()

        page.screenshot(
            path=str(screenshot_path),
            full_page=True,
        )

        browser.close()

    return {
        "resultado": result,
        "evidencia": str(screenshot_path),
    }