"""Debug Playwright POST — intercept the actual request to see what's different."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Intercept requests
    def on_request(request):
        if '/setup' in request.url and request.method == 'POST':
            print(f"\n=== Intercepted POST /setup ===")
            print(f"URL: {request.url}")
            print(f"Method: {request.method}")
            print(f"Headers: {dict(request.headers)}")
            print(f"Post data: {request.post_data}")

    page.on("request", on_request)

    def on_response(response):
        if '/setup' in response.url:
            print(f"\n=== Response from {response.url} ===")
            print(f"Status: {response.status}")
            print(f"Headers: {dict(response.headers)}")

    page.on("response", on_response)

    # Load and fill
    page.goto("http://localhost:8081/setup", wait_until="networkidle")
    page.fill('input[name="username"]', 'admin2')
    page.fill('input[name="email"]', 'admin2@test.com')
    page.fill('input[name="password"]', 'Admin123!')
    page.fill('input[name="confirmPassword"]', 'Admin123!')

    # Submit
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")

    print(f"\nFinal URL: {page.url}")
    browser.close()
