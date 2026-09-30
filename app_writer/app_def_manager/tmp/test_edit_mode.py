"""Test edit mode on a master entity page."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    errors = []
    page.on("console", lambda msg: errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)

    # Go to login first
    page.goto("http://localhost:5173/login", wait_until="networkidle")
    print(f"Login page: {page.url}")

    # Check if there's a login form
    inputs = page.query_selector_all("input")
    print(f"Login inputs: {[i.get_attribute('name') or i.get_attribute('type') for i in inputs]}")

    # Try to navigate to a master page directly
    page.goto("http://localhost:5173/masters/education-levels", wait_until="networkidle")
    print(f"\nAfter nav: {page.url}")
    print(f"Page content length: {len(page.inner_text('body'))}")

    # Check if form is visible
    form = page.query_selector("form")
    print(f"Form present: {form is not None}")

    # Check for disabled inputs
    disabled_inputs = page.query_selector_all("input[disabled]")
    enabled_inputs = page.query_selector_all("input:not([disabled])")
    print(f"Disabled inputs: {len(disabled_inputs)}")
    print(f"Enabled inputs: {len(enabled_inputs)}")

    # Check for Edit button
    edit_btn = page.query_selector("button:has-text('Edit')")
    print(f"Edit button present: {edit_btn is not None}")

    if errors:
        print(f"\nErrors: {errors[:3]}")

    page.screenshot(path="app_def_manager/tmp/edit_mode_test.png")
    browser.close()
