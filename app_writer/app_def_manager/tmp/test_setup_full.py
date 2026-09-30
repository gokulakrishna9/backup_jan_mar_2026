"""Full headless test: setup → login → swagger."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    errors = []
    page.on("console", lambda msg: errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)

    # 1. Load setup page
    print("=== GET /setup ===")
    resp = page.goto("http://localhost:8081/setup", wait_until="networkidle")
    print(f"Status: {resp.status}, URL: {page.url}")

    # 2. Fill and submit
    page.fill('input[name="username"]', 'superadmin')
    page.fill('input[name="email"]', 'super@jobportal.com')
    page.fill('input[name="password"]', 'SuperAdmin123!')
    page.fill('input[name="confirmPassword"]', 'SuperAdmin123!')
    print("Form filled")

    # Submit — don't wait for navigation, just click and wait for response
    page.click('button[type="submit"]')
    page.wait_for_timeout(3000)
    print(f"After submit: URL={page.url}")
    print(f"Page title: {page.title()}")
    body = page.inner_text("body")
    print(f"Body (first 300): {body[:300]}")

    # Screenshot
    page.screenshot(path="app_def_manager/tmp/setup_after_submit.png")

    if errors:
        print(f"\nConsole errors ({len(errors)}):")
        for e in errors[:5]:
            print(f"  {e}")

    browser.close()
