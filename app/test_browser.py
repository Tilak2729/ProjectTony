from playwright.sync_api import sync_playwright


with sync_playwright() as p:

    print("Starting browser...")

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto("https://www.google.com")

    print("Browser opened successfully.")
    print("Page title:", page.title())

    input("Press Enter to close...")

    browser.close()