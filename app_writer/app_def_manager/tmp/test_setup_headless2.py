"""Headless browser test for /setup — with confirm password field."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    errors = []
    page.on("console", lambda msg: errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)

    # Load setup page
    resp = page.goto("http://localhost:8081/setup", wait_until="networkidle")
    print(f"GET /setup: {resp.status}")

    # Dump all input fields
    inputs = page.query_selector_all("input")
    print(f"\nForm inputs ({len(inputs)}):")
    for inp in inputs:
        name = inp.get_attribute("name") or "?"
        type_ = inp.get_attribute("type") or "text"
        placeholder = inp.get_attribute("placeholder") or ""
        print(f"  name={name}, type={type_}, placeholder={placeholder}")

    # Fill all fields
    page.fill('input[name="username"]', 'admin')
    page.fill('input[name="email"]', 'admin@jobportal.com')
    page.fill('input[name="password"]', 'Admin123!')

    # Check for confirmPassword field
    confirm = page.query_selector('input[name="confirmPassword"]')
    if confirm:
        page.fill('input[name="confirmPassword"]', 'Admin123!')
        print("\nFilled confirmPassword field")

    # Submit
    print("\nSubmitting form...")
    try:
        with page.expect_navigation(wait_until="networkidle", timeout=15000) as nav:
            page.click('button[type="submit"]')
        print(f"Post-submit status: {nav.value.status}")
        print(f"Post-submit URL: {page.url}")
    except Exception as e:
        print(f"Navigation error: {e}")
        print(f"Current URL: {page.url}")

    # Result
    body = page.inner_text("body")
    print(f"\nResult body (first 500):\n{body[:500]}")

    page.screenshot(path="app_def_manager/tmp/setup_result2.png")

    if errors:
        print(f"\nConsole errors: {errors}")

    browser.close()
