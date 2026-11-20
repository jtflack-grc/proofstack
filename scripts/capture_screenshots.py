from pathlib import Path
import time

from playwright.sync_api import sync_playwright

OUT = Path("docs/images")
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1050}, device_scale_factor=1)

    page.goto("http://127.0.0.1:8501", wait_until="networkidle", timeout=120000)
    page.get_by_text("ProofStack", exact=True).first.wait_for(timeout=30000)

    # Clean reviewer view before model assessment.
    page.screenshot(path=str(OUT / "proofstack-reviewer-workflow.png"), full_page=True)

    # Run the deterministic local advisory on the default synthetic evidence case.
    page.get_by_role("button", name="Assess this evidence").click()
    page.get_by_text("AI assessment:", exact=False).wait_for(timeout=30000)
    time.sleep(1)

    page.screenshot(path=str(OUT / "proofstack-advisory-grounding.png"), full_page=True)
    browser.close()
