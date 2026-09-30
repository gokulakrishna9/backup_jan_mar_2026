"""Headless browser test for /setup page — load, fill form, submit, capture results."""
from playwright.sync_api import sync_playwright
import sys

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Collect console errors
    errors = []
    page.on("console", lambda msg: errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
    page.on("pageerror", lambda err: errors.append(f"[pageerror] {err}"))

    # 1. Load the setup page
    print("=== Step 1: GET /setup ===")
    resp = page.goto("http://localhost:8081/setup", wait_until="networkidle")
    print(f"Status: {resp.status}")
    print(f"URL: {page.url}")
    title = page.title()
    print(f"Title: {title}")

    # Check if page has content
    body_text = page.inner_text("body")
    print(f"Body length: {len(body_text)} chars")
    print(f"Has form: {'<form' in page.content()}")

    # 2. Fill the form
    print("\n=== Step 2: Fill form ===")
    try:
        page.fill('input[name="username"]', 'admin')
        page.fill('input[name="password"]', 'Admin123!')
        page.fill('input[name="email"]', 'admin@jobportal.com')
        print("Form filled successfully")
    except Exception as e:
        print(f"Error filling form: {e}")

    # 3. Submit the form
    print("\n=== Step 3: Submit form ===")
    try:
        # Click submit and wait for navigation
        with page.expect_navigation(wait_until="networkidle", timeout=10000) as nav_info:
            page.click('button[type="submit"], input[type="submit"]')
        nav_resp = nav_info.value
        print(f"Post-submit status: {nav_resp.status}")
        print(f"Post-submit URL: {page.url}")
    except Exception as e:
        print(f"Submit error: {e}")
        print(f"Current URL: {page.url}")

    # 4. Check result
    print("\n=== Step 4: Result ===")
    result_text = page.inner_text("body")
    print(f"Body text (first 500 chars): {result_text[:500]}")

    # 5. Screenshot
    page.screenshot(path="app_def_manager/tmp/setup_result.png")
    print("\nScreenshot saved to app_def_manager/tmp/setup_result.png")

    # 6. Console errors
    if errors:
        print(f"\n=== Console Errors ({len(errors)}) ===")
        for e in errors:
            print(f"  {e}")
    else:
        print("\nNo console errors.")

    browser.close()
