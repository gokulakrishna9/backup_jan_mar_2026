"""Clean headless test: setup → check redirect → verify login page."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    responses = []
    page.on("response", lambda r: responses.append((r.url, r.status)))

    # 1. Load setup page
    resp = page.goto("http://localhost:8081/setup", wait_until="networkidle")
    print(f"1. GET /setup: {resp.status}, URL: {page.url}")

    # 2. Fill form
    page.fill('input[name="username"]', 'superadmin')
    page.fill('input[name="email"]', 'super@jobportal.com')
    page.fill('input[name="password"]', 'SuperAdmin123!')
    page.fill('input[name="confirmPassword"]', 'SuperAdmin123!')

    # 3. Submit
    responses.clear()
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")
    
    print(f"\n2. After submit: URL={page.url}")
    print(f"   Title: {page.title()}")
    
    # Show all responses during submit
    print(f"\n3. Network responses during submit:")
    for url, status in responses:
        print(f"   {status} {url}")

    body = page.inner_text("body")
    print(f"\n4. Body (first 200): {body[:200]}")

    page.screenshot(path="app_def_manager/tmp/setup_clean.png")
    browser.close()
